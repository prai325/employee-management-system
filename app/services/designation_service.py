from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.designation import Designation
from app.models.department import Department
from app.schemas.designation import (
    DesignationCreate,
    DesignationUpdate
)

class DesignationService:

    @staticmethod
    async def create_designation(
        db: AsyncSession,
        data: DesignationCreate
    ) -> Designation:

        # Check department
        result = await db.execute(
            select(Department).where(
                Department.id == data.department_id
            )
        )

        department = result.scalar_one_or_none()

        if not department:
            raise ValueError(
                "Department not found"
            )

        # Check duplicate designation
        result = await db.execute(
            select(Designation).where(
                Designation.name == data.name,
                Designation.department_id
                == data.department_id
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise ValueError(
                "Designation already exists "
                "in this department"
            )

        designation = Designation(
            name=data.name,
            department_id=data.department_id
        )

        db.add(designation)

        await db.commit()
        await db.refresh(designation)

        return designation

    @staticmethod
    async def get_designation(
        db: AsyncSession,
        designation_id: int
    ) -> Designation | None:

        result = await db.execute(
            select(Designation).options(selectinload(Designation.department)).where(
                Designation.id == designation_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_designations(
        db: AsyncSession,
        search: str | None = None,
        department_id: int | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_order: str = "asc"
    ):

        offset = (
            page - 1
        ) * page_size

        query = select(Designation).options(
                selectinload(
                    Designation.department
                )
            )

        count_query = select(
            func.count(Designation.id)
        )

        if search:

            search_filter = (
                Designation.name.ilike(
                    f"%{search}%"
                )
            )

            query = query.where(
                search_filter
            )

            count_query = count_query.where(
                search_filter
            )

        if department_id:

            department_filter = (
                Designation.department_id
                == department_id
            )

            query = query.where(
                department_filter
            )

            count_query = count_query.where(
                department_filter
            )

        if sort_order.lower() == "desc":

            query = query.order_by(
                Designation.created_at.desc()
            )

        else:

            query = query.order_by(
                Designation.created_at.asc()
            )

        query = (
            query
            .offset(offset)
            .limit(page_size)
        )

        result = await db.execute(query)

        designations = list(
            result.scalars().all()
        )

        count_result = await db.execute(
            count_query
        )

        total = count_result.scalar_one()

        total_pages = (
            total + page_size - 1
        ) // page_size

        # return {
        #     "items": designations,
        #     "total": total,
        #     "page": page,
        #     "page_size": page_size,
        #     "total_pages": total_pages
        # }

        items = []

        for designation in designations:

            items.append(
                {
                    "id": designation.id,
                    "name": designation.name,
                    "department_id": (
                        designation.department_id
                    ),
                    "department_name": (
                        designation.department.name
                    ),
                }
            )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    @staticmethod
    async def update_designation(
        db: AsyncSession,
        designation_id: int,
        data: DesignationUpdate
    ):

        result = await db.execute(
            select(Designation).where(
                Designation.id == designation_id
            )
        )

        designation = (
            result.scalar_one_or_none()
        )

        if not designation:
            return None

    @staticmethod
    async def delete_designation(
        db: AsyncSession,
        designation_id: int
    ) -> bool:

        result = await db.execute(
            select(Designation).where(
                Designation.id == designation_id
            )
        )

        designation = (
            result.scalar_one_or_none()
        )

        if not designation:
            return False

        await db.delete(designation)

        await db.commit()

        return True