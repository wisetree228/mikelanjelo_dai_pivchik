"""
Модели (таблицы бд)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary, BigInteger, Float, func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, declarative_base
from dotenv import load_dotenv
import os
import math

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
    city = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    media = relationship("Media", back_populates="user", cascade="all, delete-orphan")
    likes_created = relationship("Like", foreign_keys='Like.author_id', back_populates="author")
    likes_got = relationship("Like", foreign_keys='Like.getter_id', back_populates="getter")
    created_at = Column(DateTime, default=datetime.now)

    @hybrid_property
    def distance_to(self, target_lat: float, target_lon: float) -> float:
        """Расчёт расстояния в Python (в километрах)"""
        if (self.lat is None) or (self.lon is None) or (target_lat is None) or (target_lon is None):
            return None
        return self.haversine(self.lat, self.lon, target_lat, target_lon)

    @distance_to.expression
    def distance_to(cls, target_lat: float, target_lon: float):
        """SQL-версия для использования в запросах"""
        return cls.haversine_expression(cls.lat, cls.lon, target_lat, target_lon)

    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Формула Haversine для расчёта расстояния между точками (в км)"""
        R = 6371  # Радиус Земли в км
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) + \
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def haversine_expression(lat1, lon1, lat2, lon2):
        """SQL-выражение для формулы Haversine"""
        return 6371 * 2 * func.asin(
            func.sqrt(
                func.pow(func.sin(func.radians(lat2 - lat1) / 2), 2) +
                func.cos(func.radians(lat1)) *
                func.cos(func.radians(lat2)) *
                func.pow(func.sin(func.radians(lon2 - lon1) / 2), 2)
            )
        )


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
