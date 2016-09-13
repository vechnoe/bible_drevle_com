from psycopg2 import IntegrityError

from bible_drevle_com.models import Book
from base import Config

BOOKS = Config('books')()

for book in BOOKS:
    if not Book.exists(book['book_id']):
        Book.create_books([book])
