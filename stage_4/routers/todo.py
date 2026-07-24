from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from database import get_db
from models import Todo, TodoRequest


router = APIRouter()




@router.get("/")
def get_task(db:Session = Depends(get_db)):
  return db.query(Todo).all()


@router.get("/task/{taskid}")
def get_task_by_id(db:Session = Depends(get_db), taskid:int = Path(ge=1)):
  task = db.query(Todo).filter(Todo.id == taskid).first()
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")

  return task


@router.post("/add-task")
def add_task(task: TodoRequest, db:Session = Depends(get_db)):
  new_task = Todo(**task.model_dump())
  db.add(new_task)
  db.commit()


@router.put("/update-task/{taskid}")
def update_task(task: TodoRequest, db:Session = Depends(get_db), taskid:int = Path(ge=1)):
  utask = db.query(Todo).filter(Todo.id == taskid).first()
  if not utask:
    raise HTTPException(status_code=404, detail="Task not found")

  utask.title = task.title
  utask.description = task.description
  utask.is_completed = task.is_completed
  utask.priority = task.priority

  db.add(utask)
  db.commit()


@router.delete("/delete-task/{taskid}")
def delete_task(db:Session = Depends(get_db), taskid:int = Path(ge=1)):
  dtask = db.query(Todo).filter(Todo.id == taskid).first()
  if not dtask:
    raise HTTPException(status_code=404, detail="Task not found")

  db.query(Todo).filter(Todo.id == taskid).delete()
  db.commit()
