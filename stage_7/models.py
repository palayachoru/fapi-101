from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from pydantic import Field, BaseModel
from typing import Optional

from database import Base


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  email = Column(String, unique=True)
  username = Column(String, unique=True)
  name = Column(String)
  hashed_passwd = Column(String)
  is_active = Column(Boolean, default=True)
  is_admin = Column(Boolean, default=False)        # user is admin/normal user
  phone_no = Column(String)


class UserRequest(BaseModel):
  email: str
  username: str = Field(min_length=3, max_length=10)
  name: str = Field(min_length=3, max_length=20)
  passwd: str
  is_active: Optional[bool] = Field(default=True)
  is_admin: bool = Field(default=False)
  phone_no: str = Field()


class PasswordChangeRequest(BaseModel):
  curr_password: str
  new_password: str






class Todo(Base):
  __tablename__ = 'todo'

  # defining columns & accepted data types
  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  is_completed = Column(Boolean, default=False)
  user_id = Column(Integer, ForeignKey("users.id"))
  phone_no = Column(String)


class TodoRequest(BaseModel):
  title: str = Field(min_length=3, max_length=50)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(ge=1, le=5)
  is_completed: Optional[bool] = Field(default=False)

  model_config = {
    "json_schema_extra": {
      "example": {
        "title": "Title",
        "description": "Specification of task",
        "priority": 2,
        "is_completed": False,
      }
    }
  }
