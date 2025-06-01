from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import relationship, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(Text)
    gender = Column(String)
    age = Column(Integer)
    who_search = Column(String)

    media = relationship("Media", back_populates="user", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.now)


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    file = Column(LargeBinary)
    media_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="media")


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    getter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
