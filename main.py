
from features.core.config import settings
from fastapi import FastAPI
from features.auth import auth_router
from features.users import user_router

app = FastAPI(
    title="Project Intelligence API",
    description="Backend APIs for internal platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/api-docs",
    openapi_url="/openapi.json",
    debug=settings.debug
)

app.include_router(auth_router)
app.include_router(user_router)
