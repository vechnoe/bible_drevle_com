from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

engine = create_engine(
    'postgresql+psycopg2://bible:123456@localhost/bible')
Session = sessionmaker(bind=engine, extension=ZopeTransactionExtension())

DBSession = Session(bind=engine)
Base = declarative_base(bind=engine)
