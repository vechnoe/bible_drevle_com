import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists

from bible_drevle_com.utils import row2dict
from bible_drevle_com.models.base import DBSession, Base


class Book(Base):
    __tablename__ = 'books'

    book_id = sa.Column(sa.Integer, primary_key=True)
    book_slug = sa.Column(sa.String, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)
    book_ending = sa.Column(sa.Text)

    def __repr__(self):
        return '%d: %s' % (self.book_id, self.title)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def exists(cls, book_id):
        query = DBSession.query(exists().where(cls.book_id == book_id)).scalar()
        return query

    @classmethod
    def create_books(cls, book_list):
        cls.__table__.insert().execute(book_list)

    @classmethod
    def get_book(cls, slug):
        book = DBSession.query(Book).filter(
            cls.book_slug == slug).first()
        if not book:
                return None
        chapters_list = DBSession.query(Chapter).filter(
            Chapter.book_slug == slug).all()

        return dict(
            bookId=book.book_id,
            bookTitle=book.title,
            titleSlavonic=book.title_slavonic,
            bookEnding=book.book_ending,
            chapters=list(map(row2dict, chapters_list))
        )

    @classmethod
    def get_books(cls):
        book_list = DBSession.query(cls).order_by(cls.book_id).all()

        def book_detail(book):
            return dict(
                bookId=book.book_id,
                bookSlug=book.book_slug,
                bookTitle=book.title,
                titleSlavonic=book.title_slavonic,
            )

        book_list = list(map(book_detail, book_list))

        books = dict(
            bookCount=len(book_list),
            books=book_list
        )
        return books


class Chapter(Base):
    __tablename__ = 'chapters'
    book_rel = relationship(
        'Book', backref=backref('chapters', lazy='dynamic'))

    book_slug = sa.Column(
        sa.String, sa.ForeignKey('books.book_slug'), primary_key=True)
    chapter_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)
    text = sa.Column(sa.Text)

    def __repr__(self):
        return '%s: %d' % (self.book_slug, self.chapter_id)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_chapter_text(cls, book_slug, chapter_id):
        query = DBSession.query(cls)
        chapter = query.filter(
            cls.book_slug == book_slug,
            cls.chapter_id == chapter_id).first()

        if not chapter:
            return None

        chapter = row2dict(chapter)

        return dict(
            bookSlug=book_slug,
            chapterId=int(chapter_id),
            title=chapter['title'],
            titleSlavonic=chapter['title_slavonic'],
            text=chapter['text']
        )

"""
class Chapter(Base):
    __tablename__ = 'chapters'
    book_rel = relationship(
        'Book', backref=backref('chapters', lazy='dynamic'))

    book_slug = sa.Column(
        sa.String, sa.ForeignKey('books.book_slug'), primary_key=True)
    chapter_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)
    text = sa.Column(sa.Text)

    def __repr__(self):
        return '%s: %d' % (self.book_slug, self.chapter_id)

    def __str__(self):
        return self.__repr__()


class ChapterText(Base):
    __tablename__ = 'chapter_texts'
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ['chapter_id', 'book_slug'],
            ['chapters.chapter_id', 'chapters.book_slug'],
        ),
    )
    chapter_rel = relationship(
        'Chapter', backref=backref('chapter_texts', lazy='dynamic'))

    book_slug = sa.Column(sa.String, primary_key=True)
    chapter_id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.Text)
"""