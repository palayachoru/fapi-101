from fastapi import FastAPI, Path, Query, HTTPException

from book import Book, BookRequest


books = [
  Book(111, 'bookA', 'authorX', "Ok book", 4),
  Book(112, 'bookB', 'authorY', "Nice book", 3),
  Book(113, 'bookC', 'authorZ', "Kill book", 2),
  Book(114, 'bookD', 'authorX', "Rom book", 1),
  Book(115, 'bookE', 'authorY', "Shit book", 0),
  Book(116, 'bookF', 'authorZ', "Fruit book", 2),
  Book(117, 'bookG', 'authorX', "Jack book", 3)
]


app = FastAPI()


@app.get('/')
def get_books():
  return books


@app.get("/book/{id}")            # Path parameter validation
def get_book_by_id(id: int = Path(gt=0, le=10)):
  for book in books:
    if book.id == id:
      return book
  raise HTTPException(status_code=404, detail="Book with ID not found")


@app.get("/book")                # Query parameter (?) validation
def get_book_by_rating(rating: int = Query(le=1, ge=5)):
  rbooks = []

  for book in books:
    if book.rating == rating:
      rbooks.append(book)
  return rbooks


@app.post('/add-book')
def add_book(book: BookRequest):
  newbook = Book(**book.model_dump())
  books.append(newbook)


@app.delete('/delete-book/{title}')
def delete_book(title: str):
  for id,book in enumerate(books):
    if book.title == title:
      books.pop(id)
      return
  raise HTTPException(status_code=404, detail="Invalid book title")
