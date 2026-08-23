from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permissions import Permission
from app.schemas.permission import (
    PermissionCreate,
)

class PermissionService:

    @staticmethod
    async def create_permission(
        db: AsyncSession,
        data: PermissionCreate,
    ) -> Permission:

        existing = await db.execute(
            select(Permission)
            .where(
                Permission.name == data.name
            )
        )

        permission = existing.scalar_one_or_none()

        if permission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission already exists",
            )

        new_permission = Permission(
            name=data.name,
            description=data.description,
        )

        db.add(new_permission)

        await db.commit()

        await db.refresh(new_permission)

        return new_permission