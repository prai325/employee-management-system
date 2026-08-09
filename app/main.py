from fastapi import FastAPI
from app.core.config import settings
from app.routers.role import router as role_router

app = FastAPI(title=settings.app_name)

@app.get("/")
async def root():
    return {
        "message": "Employee Management System API"
    }

app.include_router(role_router)