import pytest

from fastapi.testclient import TestClient
from starlette import status
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from routers.todo import get_db, get_user
from database import Base
from models import Todo


# ===== TEST DATABASE SETUP ================================================== #
TEST_DATABASE_URL = 'sqlite:///./test_todo_app.db'
test_engine = create_engine(
                  TEST_DATABASE_URL,
                  connect_args = {'check_same_thread': False},
                  poolclass = StaticPool,
              )
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def get_testdb():
  testdb = TestSessionLocal()

  try:
    yield testdb
  finally:
    testdb.close()



# ===== MOCKING DEPENDENCY INJECTION ========================================= #
def get_testuser():
  return {"username": 'userA', "id": 1, "is_admin": False}

app.dependency_overrides[get_db] = get_testdb
app.dependency_overrides[get_user] = get_testuser



# ===== ADDING SOME FIXTURES ================================================= #
@pytest.fixture
def add_task_to_db():
  task1 = Todo(
          title="taskA",
          description="taskAA",
          priority=3,
          is_completed=False,
          user_id=1
        )

  db = TestSessionLocal()
  db.add(task1)
  db.commit()
  yield task1

  # delete the takes from the DB
  with test_engine.connect() as conn:
    conn.execute(text("DELETE FROM todo;"))
    conn.commit()


@pytest.fixture
def clean_db():
  with test_engine.connect() as conn:
    conn.execute(text("DELETE FROM todo;"))
    conn.commit()



# ===== TETSING BEGINS HERE ================================================== #
client = TestClient(app)

def test_get_task_db_empty(clean_db):
  response = client.get("/todo/")

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == []


def test_get_task(add_task_to_db):
  response = client.get("/todo/")

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == [{'title': 'taskA', 'description': 'taskAA',
                              'is_completed': False, 'user_id': 1,
                                'priority': 3, 'id': 1}]


def test_get_task_by_id(add_task_to_db):
  response = client.get("/todo/1")

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'title': 'taskA', 'description': 'taskAA',
                              'is_completed': False, 'user_id': 1,
                              'priority': 3, 'id': 1}


def test_get_task_by_id_invalid(add_task_to_db):
  response = client.get("/todo/999")

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'Task not found'}


def test_add_task(add_task_to_db):
  request_data = {'title':'taskB', 'description':'taskBB', 'priority':3, 'is_completed':False}
  response = client.post("/todo/add", json=request_data)

  assert response.status_code == status.HTTP_200_OK

  # test if the data is updated in the db
  db = TestSessionLocal()
  task = db.query(Todo).filter(Todo.id == 2).first()
  assert task.title == request_data.get('title')
  assert task.description == request_data.get('description')
  assert task.priority == request_data.get('priority')
  assert task.is_completed == request_data.get('is_completed')


def test_update_task(add_task_to_db):
  request_data = {'title':'taskA_updated', 'description':'taskAA_updated', 'priority':1, 'is_completed':False}
  response = client.put("/todo/update/1", json=request_data)

  assert response.status_code == status.HTTP_200_OK

  # check the test db to see if the data is updated
  tdb = TestSessionLocal()
  task = tdb.query(Todo).filter(Todo.id == 1).first()
  assert task.title == request_data.get('title')
  assert task.description == request_data.get('description')
  assert task.priority == request_data.get('priority')
  assert task.is_completed == request_data.get('is_completed')


def test_update_task_not_found(add_task_to_db):
  request_data = {'title':'taskA_updated', 'description':'taskAA_updated', 'priority':1, 'is_completed':False}
  response = client.put("/todo/update/999", json=request_data)

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'Task not found'}


def test_delete_task(add_task_to_db):
  response = client.delete("/todo/delete/1")

  assert response.status_code == status.HTTP_200_OK

  # check if the db entry is deleted
  tdb = TestSessionLocal()
  task = tdb.query(Todo).all()
  assert task == []


def test_delete_task_not_found(add_task_to_db):
  response = client.delete("/todo/delete/99")

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'Task not found'}
