from sqlalchemy.orm import Session

from models.users import User as ModelUser
from passlib.hash import bcrypt
from schemas.users import UserCreate


async def create_user(db: Session, user: UserCreate) -> ModelUser:
    hashed_password = bcrypt.hash(user.password)
    db_user = ModelUser(email=user.email, first_name=user.first_name,
                        last_name=user.last_name,
                        hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user_by_email(db: Session, email: str) -> ModelUser:
    """Получить пользователя по email"""
    return db.query(ModelUser).filter(ModelUser.email == email).first()
