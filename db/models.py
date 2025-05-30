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
    avatar = Column(LargeBinary)
    about = Column(Text)
    created_at = Column(DateTime, default=datetime.now)