# -*- coding: utf-8 -*-
from sqlalchemy import Column, create_engine, DateTime, ForeignKey, Integer,\
    Sequence, String, Table
from sqlalchemy.orm import relationship
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


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
