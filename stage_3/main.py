from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session

import models

from models import Todo, TodoRequest
from database import engine, get_db

app = FastAPI()

# create a database file and generate tables & columns
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def get_tasks(db:Session = Depends(get_db)):
  return db.query(Todo).all()


@app.get("/{taskid}")
def get_task_by_id(taskid: int = Path(ge=1, le=100), db:Session = Depends(get_db)):
  task = db.query(Todo).filter(Todo.id == taskid).first()

  if not task:
    raise HTTPException(status_code=404, detail=f"No task with id {taskid}")

  return task


@app.post("/add-task")
def add_task(task: TodoRequest, db:Session = Depends(get_db)):
  # serialize the data from json string and ceate object instance
  new_task = Todo(**task.model_dump())

  db.add(new_task)
  db.commit()


@app.put("/update-task/{taskid}")
def update_task(
          taskreq:TodoRequest,
          taskid:int = Path(ge=1),
          db:Session = Depends(get_db)
         ):
  utask = db.query(Todo).filter(Todo.id == taskid).first()
  if not utask:
    raise HTTPException(status_code=404, detail="Task not found")

  utask.title = taskreq.title
  utask.description = taskreq.description
  utask.is_completed = taskreq.is_completed
  utask.priority = taskreq.priority

  db.add(utask)
  db.commit()


@app.delete("/delete-task/{taskid}")
def delete_task(taskid: int = Path(ge=1), db:Session = Depends(get_db)):
  dtask = db.query(Todo).filter(Todo.id == taskid).first()
  if not dtask:
    raise HTTPException(status_code=404, detail="Task not found")

  db.query(Todo).filter(Todo.id == taskid).delete()
  db.commit()
