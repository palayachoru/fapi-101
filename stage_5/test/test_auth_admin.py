import pytest

from fastapi.testclient import TestClient
from starlette import status

from main import app
from routers.auth import get_db, get_user
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



# ===== TETSING BEGINS HERE ================================================== #
client = TestClient(app)

def test_get_users(override_dep, add_user_to_db):
  response = client.get("/auth/users")

  data = response.json()[0]

  assert response.status_code == status.HTTP_200_OK
  assert data.get('username') == 'usera'
  assert data.get('name') == 'UserA'
  assert data.get('email') == 'user@user.com'
  assert data.get('username') == 'user@user.com'
