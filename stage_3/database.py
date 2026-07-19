from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. specify location of database file
DATABASE_URL = 'sqlite:///./todo.db'

# 2. create a global database engine
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

# 3. create SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. create a base
Base = declarative_base()


# For every request -- this function is invoked by FastAPI and result is injected
# back to the endpoint function.This funcion create new session to interact with
# the database. Once the yeild is finished, then 'finally' is executed to close
# the database connction
def get_db():
  db = SessionLocal()

  try:
    yield db
  finally:
    db.close()
