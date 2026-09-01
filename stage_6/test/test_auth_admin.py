import pytest

from fastapi.testclient import TestClient
from starlette import status

from main import app
from routers.auth import get_db, get_user, authenticate_user
from .util import *


# ===== MOCKING DEPENDENCY INJECTION ========================================= #
def get_testuser():
  return {"username": 'userA', "id": 1, "is_admin": True}

# Override dependency as a fixture function, so that the override is function
# scoped and don't affect other tests
@pytest.fixture
def override_dep():
  app.dependency_overrides[get_db] = get_testdb
  app.dependency_overrides[get_user] = get_testuser
  yield

  # clear the orverride depenedency
  app.dependency_overrides.clear()


# ===== ADDING FIXTURES ====================================================== #
@pytest.fixture
def add_user_to_db():
  user = User(
            email = "user@user.com",
            username = "usera",
            name = "UserA",
            hashed_passwd = bcrypt_hasher.hash("test123"),
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


# ===== TETSING BEGINS HERE ================================================== #
client = TestClient(app)

def test_get_users(override_dep, add_user_to_db):
  response = client.get("/auth/users")

  data = response.json()[0]

  assert response.status_code == status.HTTP_200_OK
  assert data.get('username') == 'usera'
  assert data.get('name') == 'UserA'
  assert data.get('email') == 'user@user.com'


def test_change_password(override_dep, add_user_to_db):
  response = client.post("/auth/change-password", json={'curr_password':"test123", "new_password":"test123"})

  assert response.status_code == status.HTTP_200_OK


def test_change_password_invalid(override_dep, add_user_to_db):
  response = client.post("/auth/change-password", json={'curr_password':"sdfdfsdf", "new_password":"test123"})

  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {"detail": "Password mismatched"}


def test_authenticate_user(override_dep, add_user_to_db):
  tdb = TestSessionLocal()

  # checking with correct details
  authenticated_user = authenticate_user(username = "usera", passwd = "test123", db = tdb)
  assert authenticated_user is not None
  assert authenticated_user.username == "usera"
  assert authenticated_user.email == "user@user.com"

  # checking with wrong username
  authenticated_user = authenticate_user(username = "sadfsdfd", passwd = "test123", db = tdb)
  assert authenticated_user is False

  # checking with wrong password
  authenticated_user = authenticate_user(username = "usera", passwd = "sdfdfhdjhkj", db = tdb)
  assert authenticated_user is False
