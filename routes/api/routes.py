from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils import validate_token_data
from db.crud.routes import create_new_route, get_routes_from_db
from db.service import check_token, get_db
from schemas.routes import RouteCreate, RouteWithPoints

router = APIRouter()


@router.post('/api/routes/new_route/', response_model=RouteWithPoints)
async def create_route(route: RouteCreate, db: Session = Depends(get_db),
                       user_data: dict = Depends(check_token)):
    """Создание нового маршрута

    Координаты передаются в десятичном виде (56.23213, 26.54545)
    """
    await validate_token_data(user_data)
    user_uuid = user_data.get('uuid')
    route = await create_new_route(db=db, route=route, uuid=user_uuid)
    if not route:
        raise HTTPException(
            status_code=401,
            detail='Not enough correct points to create a route.'
        )
    return route


@router.get('/api/routes/', response_model=list[RouteWithPoints])
async def get_routes(page_number: int = None, page_size: int = None,
                     db: Session = Depends(get_db),
                     user_data: dict = Depends(check_token)):
    """Возвращает список маршрутов

    Параметры запроса:
    page_number - номер страницы
    page_size - количество объектов на странице
    """
    await validate_token_data(user_data)
    routes = await get_routes_from_db(page_number, page_size, db)
    return routes
