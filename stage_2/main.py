from fastapi import FastAPI, Body

from book import Book


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
