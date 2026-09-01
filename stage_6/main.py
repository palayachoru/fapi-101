from fastapi import FastAPI

from models import Base
from database import engine
from routers import auth, todo


app = FastAPI()


# create a database file and generate tables & columns
Base.metadata.create_all(bind=engine)

# include API end-point functions
app.include_router(todo.router)    # for manipulating todo data
app.include_router(auth.router)    # for manipulation user data
