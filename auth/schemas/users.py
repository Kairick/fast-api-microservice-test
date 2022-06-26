from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая модель пользователя"""
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UserCreate(UserBase):
    """Модель создания пользователя"""
    password: str
    password2: str

    class Config:
        orm_mode = True


class User(UserBase):
    """Модель пользователя без пароля, но со сгенерированными данными"""
    id: int
    uuid: str

    class Config:
        orm_mode = True
