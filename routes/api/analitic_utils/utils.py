from math import atan2, cos, radians, sin,  sqrt

from schemas.routes import Point

R = 6373.0


async def get_total_route_distance(points: list[Point]) -> float:
    """Возвращает длину маршрута"""
    return sum([
        get_point_distance(points[i - 1], points[i])
        for i in range(1, len(points))
    ])


def get_point_distance(start: Point, finish: Point) -> float:
    """Считает расстояние между точками"""

    lat1 = radians(start.latitude)
    lon1 = radians(start.longitude)
    lat2 = radians(finish.latitude)
    lon2 = radians(finish.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
