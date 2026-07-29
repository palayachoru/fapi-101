import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from models import Todo, User
from routers.auth import bcrypt_hasher

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
def add_user_to_db():
  user = User(
            email = "user@user.com",
            username = "usera",
            name = "UserA",
            hashed_passwd = bcrypt_hasher.hash("usera"),
            is_active = True,
            is_admin = True
          )

  db = TestSessionLocal()
  db.add(user)
  db.commit()
  yield user

  # delete the takes from the DB
  with test_engine.connect() as conn:
    conn.execute(text("DELETE FROM user;"))
    conn.commit()



@pytest.fixture
def clean_db():
  with test_engine.connect() as conn:
    conn.execute(text("DELETE FROM todo;"))
    conn.commit()
