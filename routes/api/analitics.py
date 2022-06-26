from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.utils import validate_token_data
from db.service import check_token, get_db, make_report
from schemas.report import Report

router = APIRouter()


@router.get('/api/report/', response_model=Report)
async def get_report(db: Session = Depends(get_db),
                     user_data: dict = Depends(check_token)):
    """Возвращает список маршрутов

    Параметры запроса:
    page_number - номер страницы
    page_size - количество объектов на странице
    """
    await validate_token_data(user_data)
    report = await make_report(db, user_data['uuid'])
    return report
