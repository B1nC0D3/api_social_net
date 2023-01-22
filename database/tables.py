from sqlalchemy import Column, ForeignKey, Integer, String, Table, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship

from database.database import engine

Base = declarative_base()


class Likes(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='likes')
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    post = relationship('Post', back_populates='likes_rel')


class Dislikes(Base):
    __tablename__ = 'dislikes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user = relationship('User', back_populates='dislikes')
    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    post = relationship('Post', back_populates='dislikes_rel')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    posts = relationship('Post', back_populates='author')
    likes = relationship(
            'Likes', back_populates='user'
    )
    dislikes = relationship(
            'Dislikes', back_populates='user'
    )


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    author = relationship('User', back_populates='posts')
    author_id = Column(Integer, ForeignKey('users.id'), index=True)
    text = Column(String(length=1024))
    likes_rel = relationship('Likes', back_populates='post')
    dislikes_rel = relationship('Dislikes', back_populates='post')
    likes = column_property(
            select([func.count(Likes.post_id)])
            .filter(Likes.post_id == id)
            .scalar_subquery())
    dislikes = column_property(
            select([func.count(Dislikes.post_id)])
            .filter(Dislikes.post_id == id)
            .scalar_subquery())


Base.metadata.create_all(engine)
