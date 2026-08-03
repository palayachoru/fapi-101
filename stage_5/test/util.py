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
