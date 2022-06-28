from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.service import authenticate_user, create_token, decode_token, get_db

router = APIRouter()


@router.post('/api/auth/login/')
async def login(email: str, password: str, db: Session = Depends(get_db)):
    """Авторизует пользователя и возвращает токен"""
    user = await authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return await create_token(user)


@router.get('/api/auth/validate_token/')
async def validate_token(data: dict = Depends(decode_token)):
    """Проверяет токен на валидность и возвращает uuid и
     дату 'годности' токена
     """
    return data

