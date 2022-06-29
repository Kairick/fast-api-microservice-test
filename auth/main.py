from fastapi import FastAPI

from api import auth, users

app = FastAPI(openapi_url="/api/auth/openapi.json", docs_url="/api/auth/docs")
app.include_router(users.router)
app.include_router(auth.router)
