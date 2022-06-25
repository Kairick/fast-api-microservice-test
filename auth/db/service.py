import os
import time
from datetime import datetime, timedelta
from typing import Union

import email_validator
import jwt
from fastapi import Depends, security
from sqlalchemy.orm import Session

from db.crud.users import get_user_by_email
from db.database import SessionLocal
from models.users import User as ModelUser
from schemas.users import User as SchemaUser

OAUTH2SCHEME = security.OAuth2PasswordBearer('/api/auth/login/')

SECRET = os.getenv("JWT_TOKEN", "Some_token")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_token(user: ModelUser) -> dict:
    """Генерируем токен для пользователя"""
    user_object = SchemaUser.from_orm(user).dict()
    expire = datetime.utcnow() + timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    user_object.update({"exp": expire})
    token = jwt.encode(user_object, SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


async def authenticate_user(
        email: str, password: str, db: Session) -> Union[ModelUser, bool]:
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False

    return user


async def decode_token(db: Session = Depends(get_db),
                       token: str = Depends(OAUTH2SCHEME)) -> dict:
    """Валидирует пользователя по токену и возвращает uuid пользователя"""
    try:
        payload = jwt.decode(
        token, os.getenv("JWT_TOKEN", "Some_token"), algorithms=[ALGORITHM])
        user = db.query(ModelUser).get(payload['id'])

    except:
        return {'success': False, 'uuid': None, 'expires': None}
    if payload.get('exp') and payload.get('exp') < int(time.time()):
        return {'success': False, 'uuid': None, 'expires': payload['exp']}
    return {'success': True, 'uuid': user.uuid, 'expires': payload['exp']}


def email_is_valid(email: str) -> bool:
    """Валидация email"""
    try:
        email_validator.validate_email(email)
    except email_validator.EmailNotValidError:
        return False
    return True
