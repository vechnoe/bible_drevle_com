import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists

from bible_drevle_com.flatters import *
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
    def get_book_detail(cls, slug):
        book = DBSession.query(Book).filter(
            cls.book_slug == slug).first()
        if not book:
                return None
        chapters_list = DBSession.query(Chapter).order_by(
            Chapter.chapter_id).filter(Chapter.book_slug == slug).all()

        return dict(
            bookId=book.book_id,
            bookSlug=book.book_slug,
            bookTitle=book.title,
            titleSlavonic=book.title_slavonic,
            bookEnding=book.book_ending,
            chapters=list(map(chapter_flatter, chapters_list))
        )

    @classmethod
    def get_books(cls):
        book_list = DBSession.query(cls).order_by(cls.book_id).all()

        books = dict(
            bookCount=len(book_list),
            books=list(map(book_flatter, book_list))
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

        return dict(
            bookSlug=book_slug,
            chapterId=chapter.chapter_id,
            title=chapter.title,
            titleSlavonic=chapter.title_slavonic,
            text=chapter.te
        )


class Kathisma(Base):
    __tablename__ = 'kathismas'
    book_rel = relationship(
        'Book', backref=backref('kathismas', lazy='dynamic'))

    book_slug = sa.Column(
        sa.String, sa.ForeignKey('books.book_slug'), primary_key=True)
    kathisma_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)

    def __repr__(self):
        return 'Кафизма %d' % self.kathisma_id

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_kathismas(cls):
        kathismas_list = DBSession.query(cls).order_by(cls.kathisma_id).all()

        return dict(
            kathismasCount=len(kathismas_list),
            kathismas=list(map(kathismas_flatter, kathismas_list))
        )

    @classmethod
    def get_kathisma_detail(cls, kathisma_id):
        kathisma = DBSession.query(cls).filter(
            cls.book_slug == 'psalms').first()
        if not kathisma:
            return None
        psalm_list = DBSession.query(Psalm).filter(
            Psalm.kathisma_id == kathisma_id).all()

        return dict(
            kathismaId=kathisma.kathisma_id,
            kathismaTitle=kathisma.title,
            titleSlavonic=kathisma.title_slavonic,
            psalms=list(map(psalm_flatter, psalm_list))
        )


class Psalm(Base):
    __tablename__ = 'psalms'
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ['kathisma_id', 'book_slug'],
            ['kathismas.kathisma_id', 'kathismas.book_slug'],
        ),
    )
    kathisma_rel = relationship(
        'Kathisma', backref=backref('psalms', lazy='dynamic'))

    book_slug = sa.Column(sa.String, primary_key=True)
    kathisma_id = sa.Column(sa.Integer, primary_key=True)
    psalm_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)
    text = sa.Column(sa.Text)

    def __repr__(self):
        return 'Кафизма %d: псалом %d' % (self.kathisma_id, self.psalm_id)

    def __str__(self):
        return self.__repr__()
