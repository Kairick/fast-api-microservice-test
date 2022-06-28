import os
import random
import string

import aiohttp
from fastapi import security, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.analitic_utils.utils import get_total_route_distance
from db.database import SessionLocal
from models.routes import Point, Route, RoutePoint
from schemas.report import Report
from schemas.routes import PointWithNumber, RouteWithPoints

AUTH_URL = os.environ.get('AUTH_URL')
OAUTH2SCHEME = security.OAuth2PasswordBearer('/api/auth/login/')

MAX_ROUTE_LENGTH = 98
LATITUDE_RANGE = (-89.9, 89.9)
LONGITUDE_RANGE = (-179.9, 179.9)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def check_token(token: str = Depends(OAUTH2SCHEME)) -> dict:
    """Проверяем авторизацию пользователя на сервере авторизации"""
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(AUTH_URL) as r:
            return await r.json()


async def generate_points(count: int) -> list[Point]:
    """Генерирует точки маршрута"""
    letters = string.ascii_lowercase
    points = [Point(
        latitude=random.uniform(*LATITUDE_RANGE),
        longitude=random.uniform(*LONGITUDE_RANGE),
        name=''.join(random.choice(letters)
                     for _ in range(random.randint(5, 9)))
    ) for _ in range(count)]
    return points


async def get_from_raw_data(routes: list[Route]) -> list[RouteWithPoints]:
    """Преобразует модель в словарь с нужными полями"""
    result = []
    for route in routes:
        route_dict = {
            'id': route.id,
            'number': route.number,
            'user_uuid': route.user_uuid,
            'route_points': _get_points(route.route_points)
        }
        result.append(RouteWithPoints.parse_obj(route_dict))
    return result


def _get_points(route_points: list[RoutePoint]) -> list[PointWithNumber]:
    """Преобразует модель точек в словарь"""
    result = []
    for route_point in route_points:
        route_dict = {
            'id': route_point.point.id,
            'name': route_point.point.name,
            'latitude': route_point.point.latitude,
            'longitude': route_point.point.longitude,
            'sequence_number': route_point.sequence_number
        }
        result.append(PointWithNumber.parse_obj(route_dict))

    return sorted(result, key=lambda d: d.sequence_number)


async def generate_route(db: Session, new_route: Route, points: list[Point]):
    """Генерирует случайным образом точки маршрута и сохраняет в таблицу"""
    max_len = await _get_max_length(points)
    new_points = db.query(Point).order_by(
        func.random()).limit(max_len).all()
    first_point = RoutePoint(sequence_number=1,
                             point_id=points[0].id, route_id=new_route.id)
    last_point = RoutePoint(sequence_number=int(max_len) + 2,
                            point_id=points[1].id, route_id=new_route.id)
    route_points_list = [first_point, last_point]
    for n, new_point in enumerate(new_points):
        route_points_list.append(
            RoutePoint(sequence_number=n + 2,
                       point_id=new_point.id, route_id=new_route.id)
        )
    db.add_all(route_points_list)
    db.commit()


async def make_report(db: Session, uuid: str) -> Report:
    """Формирует отчет по пользователю"""
    routes = db.query(Route).select_from(
        Route
    ).join(RoutePoint).join(Point).filter(
        Route.user_uuid == uuid
    ).order_by(Route.number).all()
    total_routes = len(routes)
    total_distance = 0
    for route in routes:
        total_distance += await get_total_route_distance(
            [route_point.point for route_point in route.route_points])
    report = Report(total_routes=total_routes, total_distance=total_distance)
    return report


async def _get_max_length(points: list[Point]) -> int:
    """Возвращает максимальное количество точек в маршруте

    Максимальное количество точек - 100 (с учетом начальной и конечной точек)
    """
    latitude_len = abs(points[0].latitude - points[1].latitude)
    longitude_len = abs(points[0].longitude - points[1].longitude)
    max_len = latitude_len if latitude_len > longitude_len else longitude_len
    return max_len if max_len < MAX_ROUTE_LENGTH else MAX_ROUTE_LENGTH
