from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.role import RoleCreate
from app.models.role import Role

class RoleService:
    @staticmethod
    async def create_role(db: AsyncSession, role_data: RoleCreate) -> Role:
        role = Role(name = role_data.name)
        db.add(role)

        await db.commit()
        await db.refresh(role)
        return role
