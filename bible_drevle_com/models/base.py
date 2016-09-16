import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from zope.sqlalchemy import ZopeTransactionExtension

engine = create_engine(
    'postgresql+psycopg2://bible:123456@localhost/bible')
Session = sessionmaker(bind=engine, extension=ZopeTransactionExtension())

DBSession = Session(bind=engine)


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return '%ss' % cls.__name__.lower()

    id = sa.Column(sa.Integer, primary_key=True)

Base = declarative_base(bind=engine, cls=Base)
