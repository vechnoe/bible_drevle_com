import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import exists

from bible_drevle_com.models.base import DBSession, Base


class Book(Base):
    __tablename__ = 'books'

    book_id = sa.Column(sa.Integer, primary_key=True)
    book_slug = sa.Column(sa.String, primary_key=True)
    title = sa.Column(sa.Text)
    title_slavonic = sa.Column(sa.Text)

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
        chapters_list = DBSession.query(Chapter.chapter_id).filter(
            Chapter.book_slug == slug).all()

        return dict(
            bookId=book.book_id,
            bookTitle=book.title,
            chapters=[c[0] for c in chapters_list]
        )

    @classmethod
    def get_books(cls):
        book_list = DBSession.query(cls).order_by(cls.book_id).all()

        def book_detail(book):
            return dict(
                id=book.book_id,
                slug=book.book_slug,
                title=book.title
            )

        return list(map(book_detail, book_list))


class Chapter(Base):
    __tablename__ = 'chapters'
    book_rel = relationship(
        'Book', backref=backref('chapters', lazy='dynamic'))

    book_slug = sa.Column(
        sa.String, sa.ForeignKey('books.book_slug'), primary_key=True)
    chapter_id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text)

    def __repr__(self):
        return '%s: %d' % (self.book_slug, self.chapter_id)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_full_chapter(cls, book_slug, chapter_id):
        query = DBSession.query(Verse.verse_id, Verse.text)
        verse_list = query.filter(
            Verse.book_slug == book_slug,
            Verse.chapter_id == chapter_id).order_by(Verse.chapter_id).all()

        if not verse_list:
            return None

        def verse_detail(item):
            return dict(
                verseId=item[0],
                verseText=item[1]
            )

        return dict(
            bookSlug=book_slug,
            chapterId=int(chapter_id),
            verses=list(map(verse_detail, verse_list))
        )


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


class Verse(Base):
    __tablename__ = 'verses'
    __table_args__ = (
        sa.ForeignKeyConstraint(
            ['chapter_id', 'book_slug'],
            ['chapters.chapter_id', 'chapters.book_slug'],
        ),
    )
    chapter_rel = relationship(
        'Chapter', backref=backref('verses', lazy='dynamic'))

    book_slug = sa.Column(sa.String, primary_key=True)
    chapter_id = sa.Column(sa.Integer, primary_key=True)
    verse_id = sa.Column(sa.Integer, primary_key=True)
    text = sa.Column(sa.Text)

    def __repr__(self):
        return '%d: %d' % (self.chapter_id, self.verse_id)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_verse_detail(cls, book_slug, chapter_id, verse_id):
        query = DBSession.query(Verse.text)
        verse_detail = query.filter(
            Verse.book_slug == book_slug,
            Verse.chapter_id == chapter_id,
            Verse.verse_id == verse_id,
        ).first()

        if not verse_detail:
            return None

        return dict(
            bookSlug=book_slug,
            chapterId=int(chapter_id),
            verseId=int(verse_id),
            text=verse_detail.text
        )
