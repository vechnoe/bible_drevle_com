import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import exists

from bible_drevle_com.flatters import *
from bible_drevle_com.models.base import DBSession, Base


class BibleAbstract(Base):
    __abstract__ = True

    book_slug = sa.Column(sa.String, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def exists(cls, object_id):
        query = DBSession.query(exists().where(cls.id == object_id)).scalar()
        return query

    @classmethod
    def create_objects(cls, objects_list):
        cls.__table__.insert().execute(objects_list)


class Book(BibleAbstract):
    book_ending = sa.Column(sa.Text)
    in_bible_list = sa.Column(sa.Boolean, default=True)

    def __repr__(self):
        return '%d: %s' % (self.id, self.title)

    @classmethod
    def get_book_detail(cls, slug):
        book = DBSession.query(Book).filter(
            cls.book_slug == slug).first()
        if not book:
                return None
        chapters_list = DBSession.query(Chapter).order_by(
            Chapter.id).filter(Chapter.book_slug == slug).all()

        return dict(
            bookId=book.id,
            bookSlug=book.book_slug,
            bookTitle=book.title,
            titleSlavonic=book.title_slavonic,
            bookEnding=book.book_ending,
            chapters=list(map(chapter_flatter, chapters_list))
        )

    @classmethod
    def get_books(cls):
        book_list = DBSession.query(cls).order_by(cls.id).all()

        books = dict(
            bookCount=len(book_list),
            books=list(map(book_flatter, book_list))
        )
        return books


class ChapterAbstarct(BibleAbstract):
    __abstract__ = True

    text = sa.Column(sa.Text)

    @declared_attr
    def book_slug(cls):
        return sa.Column(
            sa.String, sa.ForeignKey('books.book_slug'), primary_key=True)

    @declared_attr
    def book_rel(cls):
        return relationship(
            'Book', backref=backref(cls.__tablename__, lazy='dynamic'))

    def __repr__(self):
        return '%s: %d' % (self.book_slug, self.id)

    @classmethod
    def get_text(cls, book_slug, chapter_id):
        query = DBSession.query(cls)
        chapter = query.filter(
            cls.book_slug == book_slug,
            cls.id == chapter_id).first()

        if not chapter:
            return None

        return dict(
            bookSlug=book_slug,
            chapterId=chapter.id,
            title=chapter.title,
            titleSlavonic=chapter.title_slavonic,
            text=chapter.text
        )


class Chapter(ChapterAbstarct):
    pass


class Pericope(ChapterAbstarct):
    pass


class Kathisma(BibleAbstract):

    book_slug = sa.Column(
        sa.String, sa.ForeignKey('books.book_slug'),
        primary_key=True, server_default='psalms'
    )

    book_rel = relationship(
        'Book', backref=backref('kathismas', lazy='dynamic'))

    def __repr__(self):
        return 'Кафизма %d' % self.id

    @classmethod
    def get_kathismas(cls):
        kathismas_list = DBSession.query(cls).order_by(cls.id).all()

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
            Psalm.id == kathisma_id).all()

        return dict(
            kathismaId=kathisma.id,
            kathismaTitle=kathisma.title,
            titleSlavonic=kathisma.title_slavonic,
            psalms=list(map(psalm_flatter, psalm_list))
        )


class Psalm(BibleAbstract):
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ['kathisma_id', 'book_slug'],
            ['kathismas.id', 'kathismas.book_slug'],
        ),
    )
    kathisma_rel = relationship(
        'Kathisma', backref=backref('psalms', lazy='dynamic'))

    kathisma_id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.Text)
    book_slug = sa.Column(sa.String, primary_key=True, server_default='psalms')

    def __repr__(self):
        return 'Кафизма %d: псалом %d' % (self.kathisma_id, self.psalm_id)
