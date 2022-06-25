from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: str


class UserCreate(UserBase):
    password: str
    password2: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    uuid: str

    class Config:
        orm_mode = True
