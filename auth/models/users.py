from uuid import uuid4

from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, String

from db.database import Base


class User(Base):
    """Таблица пользователей системы"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    uuid = Column(String, default=str(uuid4()))
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)
