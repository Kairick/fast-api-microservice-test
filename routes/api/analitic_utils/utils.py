from math import atan2, cos, radians, sin, sqrt

from schemas.routes import Point

EARTH_RADIUS = 6373.0


async def get_total_route_distance(points: list[Point]) -> float:
    """Возвращает длину маршрута"""
    return sum([
        get_point_distance(points[i - 1], points[i])
        for i in range(1, len(points))
    ])


def get_point_distance(start: Point, finish: Point) -> float:
    """Считает расстояние между точками"""

    lat_start = radians(start.latitude)
    lon_start = radians(start.longitude)
    lat_finish = radians(finish.latitude)
    lon_finish = radians(finish.longitude)

    lon_diff = lon_finish - lon_start
    lat_diff = lat_finish - lat_start

    coordinate_result = (sin(lat_diff / 2) ** 2
                         + cos(lat_start) * cos(lat_finish) *
                         sin(lon_diff / 2) ** 2)
    result = 2 * atan2(sqrt(coordinate_result), sqrt(1 - coordinate_result))

    distance = EARTH_RADIUS * result

    return distance
