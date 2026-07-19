from sqlalchemy import Column, Integer, String, Boolean
from pydantic import Field, BaseModel
from typing import Optional

from database import Base


class Todo(Base):
  __tablename__ = 'todo'

  # defining columns & accepted data types
  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  is_completed = Column(Boolean, default=False)


class TodoRequest(BaseModel):
  title: str = Field(min_length=3, max_length=50)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(ge=1, le=5)
  is_completed: Optional[bool] = Field(default=False)

  model_config = {
    "json_schema_extra": {
      "example": {
        "title": "Task title",
        "description": "Detailed split up of task",
        "priority": "Specify task priority",
        "is_completed": "Is the task done"
      }
    }
  }
