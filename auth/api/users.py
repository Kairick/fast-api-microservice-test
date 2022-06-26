from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.crud.users import create_user, get_user_by_email
from db.service import get_db, email_is_valid
from schemas.users import UserCreate

router = APIRouter()


@router.post('/api/auth/user/')
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя

    Email - уникальное поле
    """
    if not email_is_valid(user.email):
        raise HTTPException(status_code=400, detail='Email is not valid')
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    if user.password != user.password2:
        raise HTTPException(status_code=400,
                            detail='Password are not identical')
    user = await create_user(db=db, user=user)
    return {'message': f'User {user.first_name} {user.last_name} was created!'}
