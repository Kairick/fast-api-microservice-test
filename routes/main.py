from fastapi import FastAPI

from api import analitics, points, routes
from db.database import Base, engine


app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

app.include_router(points.router)
app.include_router(routes.router)
app.include_router(analitics.router)

Base.metadata.create_all(bind=engine)
