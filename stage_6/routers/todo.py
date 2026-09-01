from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Todo, TodoRequest
from .auth import get_user



# Defining dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_user)]


router = APIRouter(
  prefix = "/todo",
  tags = ["Todo"]
)


@router.get("/")
def get_task(db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User Not Authorized"
    )

  if user.get('is_admin'):
    return db.query(Todo).all()
  else:
    return db.query(Todo).filter(Todo.user_id == user.get('id')).all()


@router.get("/{taskid}")
def get_task_by_id(db: db_dependency, user: user_dependency, taskid: int=Path(ge=1)):
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User Not Authorized"
    )

  if user.get('is_admin'):
    task = db.query(Todo).filter(Todo.id == taskid).first()
  else:
    task = db.query(Todo).filter(Todo.id == taskid).filter(Todo.user_id == user.get('id')).first()

  if not task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  return task


@router.post("/add")
def add_task(db: db_dependency, user: user_dependency, task: TodoRequest):
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User Not Authorized"
    )

  new_task = Todo(**task.model_dump(), user_id=user.get('id'))
  db.add(new_task)
  db.commit()


@router.put("/update/{taskid}")
def update_task(db: db_dependency, user: user_dependency, task: TodoRequest, taskid: int=Path(ge=1)):
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User Not Authorized"
    )

  if user.get('is_admin'):
    utask = db.query(Todo).filter(Todo.id == taskid).first()
  else:
    utask = db.query(Todo).filter(Todo.id == taskid).filter(Todo.user_id == user.get('id')).first()

  if not utask:
    raise HTTPException(status_code=404, detail="Task not found")

  utask.title = task.title
  utask.description = task.description
  utask.is_completed = task.is_completed
  utask.priority = task.priority

  db.add(utask)
  db.commit()


@router.delete("/delete/{taskid}")
def delete_task(db :db_dependency, user: user_dependency, taskid :int=Path(ge=1)):
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User Not Authorized"
    )

  if user.get('is_admin'):
    dtask = db.query(Todo).filter(Todo.id == taskid).first()
  else:
    dtask = db.query(Todo).filter(Todo.id == taskid).filter(Todo.user_id == user.get('id')).first()

  if not dtask:
    raise HTTPException(status_code=404, detail="Task not found")

  if user.get('is_admin'):
    db.query(Todo).filter(Todo.id == taskid).delete()
  else:
    db.query(Todo).filter(Todo.id == taskid).filter(Todo.user_id == user.get('id')).delete()

  db.commit()
