from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate
)
from app.services.department_service import DepartmentService


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=201
)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await DepartmentService.create_department(
            db=db,
            name=data.name
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):

    department = await DepartmentService.get_department(
        db,
        department_id
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department

@router.get("/")
async def get_departments(
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_order: str = Query("asc"),
    db: AsyncSession = Depends(get_db)
):

    return await DepartmentService.get_departments(
        db=db,
        search=search,
        page=page,
        page_size=page_size,
        sort_order=sort_order
    )

@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db)
):

    if data.name is None:
        raise HTTPException(
            status_code=400,
            detail="Name is required"
        )

    department = await DepartmentService.update_department(
        db=db,
        department_id=department_id,
        name=data.name
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department

@router.delete(
    "/{department_id}"
)
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await DepartmentService.delete_department(
        db,
        department_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {
        "message": "Department deleted successfully"
    }