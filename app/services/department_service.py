from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.department import Department

class DepartmentService:

    @staticmethod
    async def create_department(db: AsyncSession, name: str) -> Department:
        existing = await db.execute(select(Department).where(Department.name == name))

        if existing.scalar_one_or_none():
            raise ValueError("Department already exists")

        department = Department(name=name)
        db.add(department)

        await db.commit()
        await db.refresh(department)
        return department

    @staticmethod
    async def get_department(db: AsyncSession, department_id: int) -> Department | None:
        result = await db.execute(select(Department).where(Department.id == department_id))

        return result.scalar_one_or_none

    @staticmethod
    async def get_departments(db: AsyncSession, search: str | None = None, page: int = 1, page_size: int = 10, sort_order: str ="asc"):
        offset = (page - 1) * page_size
        query = select(Department)
        count_query = select(func.count(Department.id))

        # Search
        if search:
            search_filter = Department.name.ilike(f"%{search}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        # Sorting
        if sort_order.lower() == "desc":
            query = query.order_by(Department.name.desc())
        else:
            query = query.order_by(Department.name.asc())

        # Pagination
        query = (query.offset(offset).limit(page_size))

        # Get departments
        result = await db.execute(query)

        departments = list(result.scalars().all())

        # Get total
        count_result = await db.execute(count_query)

        total = count_result.scalar_one()

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": departments,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    @staticmethod
    async def update_department(
        db: AsyncSession,
        department_id: int,
        name: str
    ):

        department = await db.execute(
            select(Department).where(
                Department.id == department_id
            )
        )

        department = department.scalar_one_or_none()

        if not department:
            return None

        department.name = name

        await db.commit()
        await db.refresh(department)

        return department

    @staticmethod
    async def delete_department(
        db: AsyncSession,
        department_id: int
    ) -> bool:

        result = await db.execute(
            select(Department).where(
                Department.id == department_id
            )
        )

        department = result.scalar_one_or_none()

        if not department:
            return False

        await db.delete(department)

        await db.commit()

        return True