from sqlalchemy import (
    Column, ForeignKey, Integer, String, Float, Sequence, UniqueConstraint,
)
from sqlalchemy.orm import relationship

from db.database import Base


class Point(Base):
    """Таблица точек маршрута"""
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, comment='Название точки маршрута')
    latitude = Column(Float, index=True, comment='Координата широты')
    longitude = Column(Float, index=True, comment='Координата долготы')


class Route(Base):
    """Таблица маршрутов"""
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, comment='Уникальный номер маршрута')
    user_uuid = Column(String, comment='uuid пользователя, создавшего маршрут')
    __table_args__ = (UniqueConstraint('user_uuid', 'number',
                                       name='_user_uuid_number_uc'),
                      )


class RoutePoint(Base):
    """Таблица, связывающая маршруты и точки с дополнительным полем"""
    __tablename__ = 'route_point'
    seq = Sequence('route_point_id_seq')
    id = Column(Integer, seq, server_default=seq.next_value(),
                primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'),
                      primary_key=True, comment='Связь с таблицей маршруты')
    point_id = Column(Integer, ForeignKey('points.id'),
                      primary_key=True, comment='Связь с таблицей точки')
    sequence_number = Column(Integer,
                             comment='Порядковый номер точки на маршруте')
    point = relationship(Point, backref="route_points")
    route = relationship(Route, backref="route_points")
