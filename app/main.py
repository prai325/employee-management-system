from fastapi import FastAPI
from app.core.config import settings
from app.routers.role import router as role_router
from app.routers.department import router as department_router
from app.routers.user import router as user_router
from app.routers.designation import (router as designation_router)
from app.routers.employee import (router as employee_router)
from app.routers.attendance import router as attendance_router

app = FastAPI(title=settings.app_name)

@app.get("/")
async def root():
    return {
        "message": "Employee Management System API"
    }

app.include_router(role_router)
app.include_router(department_router)
app.include_router(user_router)
app.include_router(designation_router)
app.include_router(employee_router)
app.include_router(attendance_router)
