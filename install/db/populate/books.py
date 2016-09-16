from bible_drevle_com.models import Book
from base import Config

BOOKS = Config('books')()

for book in BOOKS:
    if not Book.exists(book['id']):
        Book.create_objects([book])
