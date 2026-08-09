from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.role_service import RoleService
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await RoleService.create_role(db, role_data)

@router.get("/", response_model=PaginatedResponse[RoleResponse])
async def get_roles(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), search: str | None = None, db: AsyncSession = Depends(get_db)):
    return await RoleService.get_roles(db, page, page_size, search)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(role_id: int, db: AsyncSession = Depends(get_db)):
    return await RoleService.get_role_by_id(db, role_id)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role_data: RoleUpdate, db: AsyncSession = Depends(get_db)):
    return await RoleService.update_role(db, role_id, role_data)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    return await RoleService.delete_role(db, role_id)