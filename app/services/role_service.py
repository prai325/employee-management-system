from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.role import RoleCreate, RoleUpdate
from app.models.role import Role

class RoleService:

    @staticmethod
    async def create_role(db: AsyncSession, role_data: RoleCreate) -> Role:
        role = Role(name = role_data.name)
        db.add(role)

        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def get_roles(db: AsyncSession, page: int, page_size: int, search: str | None = None):
        offset = (page - 1) * page_size
        query = select(Role)
        count_query = select(func.count(Role.id))
        
        if search:
            search_filter = Role.name.ilike(f"%{search}%")
            
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
            
        query = (query.offset(offset).limit(page_size))

        # result = await db.execute(select(Role).offset(offset).limit(page_size)) 
        result = await db.execute(query)
        roles = list(result.scalars().all())

        count_result = await db.execute(count_query)
        total = count_result.scalar_one()
        
        total_pages = (total + page_size - 1)  // page_size

        return {
            "items": roles,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
        
    @staticmethod
    async def get_role_by_id(db: AsyncSession, role_id: int) -> Role:
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        return role

    @staticmethod
    async def update_role(db: AsyncSession, role_id: int, role_data: RoleUpdate) -> Role:
        role = await RoleService.get_role_by_id(db, role_id)
        role.name = role_data.name

        await db.commit()
        await db.refresh(role)
        return role

    @staticmethod
    async def delete_role(db: AsyncSession, role_id: int) -> None:
        role = await RoleService.get_role_by_id(db, role_id)

        await db.delete(role)
        await db.commit()