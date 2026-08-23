from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
)
from app.services.permission_service import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)

@router.post(
    "/",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission_api(
    data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
):

    return await PermissionService.create_permission(
        db,
        data,
    )