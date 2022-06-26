from uuid import uuid4

from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, String

from db.database import Base


class User(Base):
    """Таблица пользователей системы"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True,
                   comment='Почта пользователя')
    first_name = Column(String, nullable=True, comment='Имя пользователя')
    last_name = Column(String, nullable=True, comment='Фамилия пользователя')
    uuid = Column(String, default=str(uuid4()),
                  comment='uuid пользователя для связи с основной базой')
    hashed_password = Column(String, comment='Хэшированный пароль')

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)
