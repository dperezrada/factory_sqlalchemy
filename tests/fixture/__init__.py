# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData, Column, DateTime, ForeignKey, Integer,\
    Sequence, String, Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer,
            Sequence('id_seq', start=0, increment=1),
            autoincrement=True,
            primary_key=True)
    content = Column('content', String(100))
    author_id = Column(Integer, ForeignKey('user.id'))
    created = Column('created', DateTime)


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer,
            Sequence('id_seq', start=0, increment=1),
            autoincrement=True,
            primary_key=True)
    post_id = Column(Integer, ForeignKey('entry.id'))
    content = Column('content', String(100))
    post_id = Column(Integer, ForeignKey('user.id'))
    created = Column('created', DateTime)


class Actor(Base):
    __tablename__ = 'actor'
    id = Column(Integer,
            Sequence('id_seq', start=0, increment=1),
            autoincrement=True,
            primary_key=True)
    name = Column('name', String(32), unique=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,
            Sequence('id_seq', start=0, increment=1),
            autoincrement=True,
            primary_key=True)
    name = Column('name', String(32), unique=True)


association_table = Table('association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id')),
    Column('actor_id', Integer, ForeignKey('actor.id'))
)


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer,
            Sequence('id_seq', start=0, increment=1),
            autoincrement=True,
            primary_key=True)
    name = Column('name', String(32), unique=True)
    actors = relationship("Actor",
                    secondary=association_table,
                    backref="movies")
    score = Column('score', Integer, default=0)


db_config = {'URL': 'sqlite:///test.db'}


def create_db():
    engine = create_engine(db_config['URL'])
    Base.metadata.create_all(engine)
    dbsession = scoped_session(
        sessionmaker(
            autocommit=True,
            autoflush=True,
            bind=engine
        )
    )
    dbsession.expunge_all()
    return engine, dbsession


def drop_db(engine):
    Base.metadata.drop_all(bind=engine)
