from pydantic import BaseModel, Field


class PointBase(BaseModel):
    """Базовая модель с одним названием для изменения имени"""
    name: str


class PointBaseCreate(PointBase):
    """Базовая модель создания точки маршрута"""
    latitude: float = Field(..., gt=-90, le=90)
    longitude: float = Field(..., gt=-180, le=180)

    class Config:
        orm_mode = True


class Point(PointBaseCreate):
    """Основная модель точки маршрута с id"""
    id: int


class PointWithNumber(Point):
    """Модель точки с порядковым номером маршрута"""
    sequence_number: int


class RoutePoints(BaseModel):
    """Модель связанной таблицы маршрутов и точке"""
    routes_id: int
    points_id: int
    sequence_number: int

    class Config:
        orm_mode = True


class RouteBase(BaseModel):
    """Базовый класс маршрута"""
    number: int


class RouteCreate(RouteBase):
    """Класс для создания маршрута"""
    start_point: int
    end_point: int

    class Config:
        orm_mode = True


class Route(RouteBase):
    """Модель маршрута со всем полями"""
    id: int
    user_uuid: str


class RouteWithPoints(RouteBase):
    """Модель маршрута со всем полями"""
    id: int
    user_uuid: str
    route_points: list[PointWithNumber]
