from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
async def root():
    return {
        "message": "Employee Management System API"
    }