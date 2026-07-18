from fastapi import FastAPI, Body


app = FastAPI()


books = [
  {"title":"bookA", "author": "authorA", "category": "Art"},
  {"title":"bookB", "author": "authorB", "category": "Science"},
  {"title":"bookC", "author": "authorC", "category": "History"},
  {"title":"bookD", "author": "authorD", "category": "Geography"},
  {"title":"bookE", "author": "authorE", "category": "Civic"},
  {"title":"bookF", "author": "authorB", "category": "Science"}
]


@app.get("/")
def hello_world():
  return {"message": "Hello World!!"}


@app.get("/books")
def get_books():
  return books


@app.get("/books/{title}")     # Path Parameter - http://127.0.0.1:8000/books/authorA
def get_book(title: str):
  for book in books:
    if book.get("title") == title:
      return book

  return {}


@app.get("/books/bycat")             # Query Parameter - http://127.0.0.1:8000/books/?category=Science
def get_book_by_category(category: str):
  all_books = []

  for book in books:
    if book.get('category') == category:
      all_books.append(book)

  return all_books


@app.get("/books/byaut")
def get_book_by_author(author: str):
  all_books = []

  for b in books:
    if b.get('author') == author:
      all_books.append(b)

  return all_books


@app.get("/books/{author}")    # Path & Query Parameters combined
def get_book_by_author_category(author: str, category: str):
  all_books = []

  for book in books:
    if book.get('author') == author and book.get('category') == category:
      all_books.append(book)

  return all_books


@app.post("/books/add-book")
def add_book(book=Body()):     # Body() - specify Fetch Request body
  books.append(book)


@app.put("/books/update-book")
def update_book(book=Body()):
  for b in books:
    if b.get("title") == book.get("title"):
      b['title'] = book.get('title')
      b['author'] = book.get('author')
      b['category'] = book.get('category')
      break


@app.delete('/books/delete-book/{title}')
def delete_book(title):
  for i in range(len(books)):
    if books[i].get('title') == title:
      books.pop(i)
      break
