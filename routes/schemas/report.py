from pydantic import BaseModel


class Report(BaseModel):
    """Модель для отчета"""
    total_routes: int
    total_distance: float
