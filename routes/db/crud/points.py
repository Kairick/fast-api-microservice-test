from typing import Union

from sqlalchemy.orm import Session

from db.service import generate_points
from models.routes import Point as ModelPoint
from schemas.routes import Point as SchemePoint
from schemas.routes import PointBase, PointBaseCreate


async def create_new_point(db: Session, point: PointBaseCreate) -> SchemePoint:
    """Создает новую точку маршрута"""
    db_point = ModelPoint(**point.dict())
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


async def bulk_create_points(db: Session, count: int):
    """Пакетное создание точек маршрута с сгенерированной информацией"""
    points_objects = await generate_points(count)
    db.add_all(points_objects)
    db.commit()


async def get_points_from_db(page_number: int, page_size: int, db: Session):
    """Возвращает постраничный список точек маршрута"""
    if not page_size or not page_number:
        return db.query(ModelPoint).order_by(ModelPoint.id).all()
    else:
        offset = page_size * (page_number - 1)
        return db.query(ModelPoint).order_by(
            ModelPoint.id).offset(offset).limit(page_size).all()


async def patch_point(db: Session, point_id: int,
                      new_point: PointBase) -> Union[ModelPoint, None]:
    """Возвращает обновленный объект"""
    old_point = db.get(ModelPoint, point_id)
    if not old_point:
        return None
    old_point.name = new_point.name
    db.add(old_point)
    db.commit()
    db.refresh(old_point)
    return old_point
