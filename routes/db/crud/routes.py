from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.service import get_from_raw_data, generate_route
from models.routes import Route as ModelRoute, Point, RoutePoint
from schemas.routes import RouteCreate, RouteWithPoints


async def create_new_route(db: Session, route: RouteCreate,
                           uuid: str) -> Union[RouteWithPoints, None]:
    """Создает новую точку маршрута"""
    route_dict = route.dict()
    route_dict['user_uuid'] = uuid
    del route_dict['start_point']
    del route_dict['end_point']
    db_route = ModelRoute(**route_dict)

    points = db.query(Point).filter(
        Point.id.in_([route.start_point, route.end_point])).all()
    if len(points) < 2:
        return None
    db.add(db_route)
    try:
        db.commit()
    except IntegrityError:
        return None
    db.refresh(db_route)
    await generate_route(db, db_route, points)
    route = await get_from_raw_data([db_route])
    return route[0]


async def get_routes_from_db(page_number: int, page_size: int, db: Session):
    """Возвращает постраничный список маршрутов"""
    if not page_number or not page_size:
        raw_routes = db.query(ModelRoute).select_from(
            ModelRoute
        ).join(RoutePoint).join(Point).order_by(
            ModelRoute.id).all()
    else:
        offset = page_size * (page_number - 1)
        raw_routes = db.query(ModelRoute).select_from(
            ModelRoute
        ).join(RoutePoint).join(Point).order_by(
            ModelRoute.id
        ).offset(offset).limit(page_size).all()
    routes = await get_from_raw_data(raw_routes)
    return routes
