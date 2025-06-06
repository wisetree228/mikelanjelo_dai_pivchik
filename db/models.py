"""
Модели (таблицы бд)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import relationship, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if 'sqlite' in DATABASE_URL:
    engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    about = Column(Text)
    gender = Column(String)
    age = Column(Integer)
    who_search = Column(String)
    username = Column(String)

    media = relationship("Media", back_populates="user", cascade="all, delete-orphan")
    likes_created = relationship("Like", foreign_keys='Like.author_id', back_populates="author")
    likes_got = relationship("Like", foreign_keys='Like.getter_id', back_populates="getter")
    created_at = Column(DateTime, default=datetime.now)


class Media(Base):
    """
    Модель медиа (фото или видео пользователя)
    """
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file = Column(LargeBinary)
    media_type = Column(String)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="media")


class Like(Base):
    """
    Модель лайка от одного пользователя другому
    """
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    getter_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    author = relationship("User", foreign_keys=[author_id], back_populates="likes_created")
    getter = relationship("User", foreign_keys=[getter_id], back_populates="likes_got")
