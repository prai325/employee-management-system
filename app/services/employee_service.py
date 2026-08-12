from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.employees import Employee
from app.models.department import Department
from app.models.designation import Designation

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
)

class EmployeeService:

    @staticmethod
    async def create_employee(
        db: AsyncSession,
        data: EmployeeCreate,
    ) -> Employee:

        # -----------------------------------------
        # Check Department
        # -----------------------------------------

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

        # -----------------------------------------
        # Check Designation
        # -----------------------------------------

        result = await db.execute(
            select(Designation).where(
                Designation.id == data.designation_id
            )
        )

        designation = result.scalar_one_or_none()

        if not designation:
            raise ValueError(
                "Designation not found"
            )

        # -----------------------------------------
        # Check Designation belongs to Department
        # -----------------------------------------

        if (
            designation.department_id
            != data.department_id
        ):
            raise ValueError(
                "Designation does not belong "
                "to the selected department"
            )

        # -----------------------------------------
        # Check Duplicate Employee Code
        # -----------------------------------------

        result = await db.execute(
            select(Employee).where(
                Employee.employee_code
                == data.employee_code
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise ValueError(
                "Employee code already exists"
            )

        # -----------------------------------------
        # Create Employee
        # -----------------------------------------

        employee = Employee(
            first_name=data.first_name,
            middle_name=data.middle_name,
            last_name=data.last_name,

            employee_code=data.employee_code,

            department_id=data.department_id,
            designation_id=data.designation_id,

            joining_date=data.joining_date,
            salary=data.salary,
        )

        db.add(employee)

        await db.commit()

        await db.refresh(employee)

        result = await db.execute(
            select(Employee)
            .options(
                selectinload(Employee.department),
                selectinload(Employee.designation),
            )
            .where(Employee.id == employee.id)
        )

        return result.scalar_one()

    @staticmethod
    async def get_employee(
        db: AsyncSession,
        employee_id: int,
    ) -> Employee | None:

        result = await db.execute(
            select(Employee)
            .options(
                selectinload(Employee.department),
                selectinload(Employee.designation),
            )
            .where(
                Employee.id == employee_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_employees(
        db: AsyncSession,
        search: str | None = None,
        department_id: int | None = None,
        designation_id: int | None = None,
        is_active: bool | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_order: str = "asc",
    ):

        offset = (
            page - 1
        ) * page_size

        # Main query

        query = (
            select(Employee)
            .options(
                selectinload(
                    Employee.department
                ),
                selectinload(
                    Employee.designation
                ),
            )
        )

        # Count query

        count_query = select(
            func.count(Employee.id)
        )

        # Search

        if search:

            search_filter = (
                Employee.first_name.ilike(
                    f"%{search}%"
                )
                |
                Employee.last_name.ilike(
                    f"%{search}%"
                )
                |
                Employee.employee_code.ilike(
                    f"%{search}%"
                )
            )

            query = query.where(
                search_filter
            )

            count_query = count_query.where(
                search_filter
            )

        # Department filter

        if department_id:

            department_filter = (
                Employee.department_id
                == department_id
            )

            query = query.where(
                department_filter
            )

            count_query = count_query.where(
                department_filter
            )

        # Designation filter

        if designation_id:

            designation_filter = (
                Employee.designation_id
                == designation_id
            )

            query = query.where(
                designation_filter
            )

            count_query = count_query.where(
                designation_filter
            )

        # Active filter

        if is_active is not None:

            active_filter = (
                Employee.is_active
                == is_active
            )

            query = query.where(
                active_filter
            )

            count_query = count_query.where(
                active_filter
            )

        # Sorting

        if sort_order.lower() == "desc":

            query = query.order_by(
                Employee.created_at.desc()
            )

        else:

            query = query.order_by(
                Employee.created_at.asc()
            )

        # Pagination

        query = (
            query
            .offset(offset)
            .limit(page_size)
        )

        # Execute

        result = await db.execute(query)

        employees = list(
            result.scalars().all()
        )

        # Count

        count_result = await db.execute(
            count_query
        )

        total = count_result.scalar_one()

        # Total pages

        total_pages = (
            total + page_size - 1
        ) // page_size

        # Response

        items = []

        for employee in employees:

            items.append(
                {
                    "id": employee.id,

                    "first_name":
                        employee.first_name,

                    "middle_name":
                        employee.middle_name,

                    "last_name":
                        employee.last_name,

                    "employee_code":
                        employee.employee_code,

                    "department_id":
                        employee.department_id,

                    "department_name":
                        employee.department.name,

                    "designation_id":
                        employee.designation_id,

                    "designation_name":
                        employee.designation.name,

                    "joining_date":
                        employee.joining_date,
                    "salary":
                        employee.salary,

                    "is_active":
                        employee.is_active,
                }
            )

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }