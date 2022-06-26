from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.utils import validate_token_data
from db.crud.points import (
    create_new_point, bulk_create_points, get_points_from_db, patch_point,
)
from db.service import get_db, check_token
from schemas.routes import PointBaseCreate, Point, PointBase

router = APIRouter()


@router.post('/api/points/new_point/', response_model=Point)
async def create_point(point: PointBaseCreate, db: Session = Depends(get_db),
                       user_data: dict = Depends(check_token)):
    """Создание новой точки

    Координаты передаются в десятичном виде (56.23213, 26.54545)
    """
    await validate_token_data(user_data)
    point = await create_new_point(db=db, point=point)
    return point


@router.post('/api/points/generate_points/')
async def create_points(request: Request, db: Session = Depends(get_db),
                        user_data: dict = Depends(check_token)) -> dict:
    """Создает пакет точек

    Входящие параметры count - количество точек
    """
    await validate_token_data(user_data)
    response = await request.json()
    count = response.get('count')
    await bulk_create_points(db, count)
    return {'message': f'created {count} points'}


@router.get('/api/points/', response_model=list[Point])
async def get_points(page_number: int = None, page_size: int = None,
                     db: Session = Depends(get_db),
                     user_data: dict = Depends(check_token)):
    """Возвращает список точек маршрута

    Параметры запроса:
    page_number - номер страницы
    page_size - количество объектов на странице
    """
    await validate_token_data(user_data)
    return await get_points_from_db(page_number, page_size, db)


@router.patch('/api/points/{point_id}/', response_model=Point)
async def update_point(
        point_id: int, point: PointBase, db: Session = Depends(get_db),
        user_data: dict = Depends(check_token)
) -> Point:
    """Обновляет точку маршрута

    Обновляется только название точки
    """
    await validate_token_data(user_data)
    updated_point = await patch_point(db, point_id, point)
    if not updated_point:
        raise HTTPException(status_code=404, detail='Point not found.')
    return updated_point
