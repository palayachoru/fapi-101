from pydantic import BaseModel, Field
from typing import Optional

class Book:
  id: int
  title: str
  author: str
  description: str
  rating: int
  color: str

  def __init__(self, id, title, author, description, rating, color = 'White'):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.color = color



# Model for pydantic validation
class BookRequest(BaseModel):
  id: int  = Field(ge=1, le=100)
  title: str  = Field(min_length=3, max_length=10)
  author: str  = Field(min_length=3, max_length=10)
  description: str = Field(min_length=3, max_length=100)
  rating: int  = Field(ge=1, le=5)
  color: Optional[str] = Field(description='Color is optional', default=None)  # optional field

  # default values populated in "Example Value" section in Swagger UI
  model_config = {
    "json_schema_extra": {
      "example": {
        "id": "ICSNN Number",
        "title": "Book's Name",
        "author": "XXX",
        "description": "A one liner about the book",
        "rating": "rate out of 5",
        "color": "book's bind color"
      }
    }
  }
