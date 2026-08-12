from sqlalchemy import select, func, case, extract
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employees import Employee
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.enums.attendance import AttendanceStatus
from datetime import date


class AttendanceService:

    @staticmethod
    async def create_attendance(
        db: AsyncSession,
        data: AttendanceCreate,
    ):

        # Check employee
        result = await db.execute(
            select(Employee).where(
                Employee.id == data.employee_id
            )
        )

        employee = result.scalar_one_or_none()

        if not employee:
            raise ValueError(
                "Employee not found"
            )

        # Check duplicate attendance
        result = await db.execute(
            select(Attendance).where(
                Attendance.employee_id
                == data.employee_id,
                Attendance.attendance_date
                == data.attendance_date,
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise ValueError(
                "Attendance already exists "
                "for this employee and date"
            )

        # Create
        attendance = Attendance(
            employee_id=data.employee_id,
            attendance_date=data.attendance_date,
            status=data.status,
            check_in=data.check_in,
            check_out=data.check_out,
            remarks=data.remarks,
        )

        db.add(attendance)

        await db.commit()

        # Reload with employee
        result = await db.execute(
            select(Attendance)
            .options(
                selectinload(
                    Attendance.employee
                )
            )
            .where(
                Attendance.id
                == attendance.id
            )
        )

        return result.scalar_one()

    @staticmethod
    async def get_attendance(
        db: AsyncSession,
        attendance_id: int,
    ):

        result = await db.execute(
            select(Attendance)
            .options(
                selectinload(
                    Attendance.employee
                )
            )
            .where(
                Attendance.id == attendance_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_attendances(
        db: AsyncSession,
        search: str | None = None,
        employee_id: int | None = None,
        status: AttendanceStatus | None = None,
        attendance_date: date | None = None,
        page: int = 1,
        page_size: int = 10,
    ):

        offset = (
            page - 1
        ) * page_size

        query = (
            select(Attendance)
            .options(
                selectinload(
                    Attendance.employee
                )
            )
        )

        count_query = select(
            func.count(Attendance.id)
        )

        # -----------------------------
        # Search by employee name
        # -----------------------------

        if search:

            search_filter = (
                Employee.first_name.ilike(
                    f"%{search}%"
                )
                |
                Employee.last_name.ilike(
                    f"%{search}%"
                )
            )

            query = (
                query
                .join(Attendance.employee)
                .where(search_filter)
            )

            count_query = (
                count_query
                .join(Attendance.employee)
                .where(search_filter)
            )

        # -----------------------------
        # Employee filter
        # -----------------------------

        if employee_id:

            employee_filter = (
                Attendance.employee_id
                == employee_id
            )

            query = query.where(
                employee_filter
            )

            count_query = count_query.where(
                employee_filter
            )

        # -----------------------------
        # Status filter
        # -----------------------------

        if status:

            status_filter = (
                Attendance.status
                == status.value
            )

            query = query.where(
                status_filter
            )

            count_query = count_query.where(
                status_filter
            )

        # -----------------------------
        # Date filter
        # -----------------------------

        if attendance_date:

            date_filter = (
                Attendance.attendance_date
                == attendance_date
            )

            query = query.where(
                date_filter
            )

            count_query = count_query.where(
                date_filter
            )

        # -----------------------------
        # Sorting + Pagination
        # -----------------------------

        query = (
            query
            .order_by(
                Attendance.attendance_date.desc()
            )
            .offset(offset)
            .limit(page_size)
        )

        # -----------------------------
        # Execute
        # -----------------------------

        result = await db.execute(query)

        attendances = list(
            result.scalars().all()
        )

        # -----------------------------
        # Count
        # -----------------------------

        count_result = await db.execute(
            count_query
        )

        total = count_result.scalar_one()

        total_pages = (
            total + page_size - 1
        ) // page_size

        return {
            "items": attendances,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    @staticmethod
    async def update_attendance(
        db: AsyncSession,
        attendance_id: int,
        data: AttendanceUpdate,
    ):

        result = await db.execute(
            select(Attendance)
            .where(
                Attendance.id == attendance_id
            )
        )

        attendance = result.scalar_one_or_none()

        if not attendance:
            raise ValueError(
                "Attendance not found"
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "status" in update_data:
            update_data["status"] = (
                update_data["status"].value
            )

        for field, value in update_data.items():
            setattr(
                attendance,
                field,
                value,
            )

        await db.commit()

        # Reload relationship
        result = await db.execute(
            select(Attendance)
            .options(
                selectinload(
                    Attendance.employee
                )
            )
            .where(
                Attendance.id
                == attendance.id
            )
        )

        return result.scalar_one()

    @staticmethod
    async def delete_attendance(
        db: AsyncSession,
        attendance_id: int,
    ):

        result = await db.execute(
            select(Attendance)
            .where(
                Attendance.id == attendance_id
            )
        )

        attendance = result.scalar_one_or_none()

        if not attendance:
            raise ValueError(
                "Attendance not found"
            )

        await db.delete(attendance)

        await db.commit()

        return True


    @staticmethod
    async def attendance_summary(
    db: AsyncSession,
    employee_id: int,
    year: int,
    month: int,
):

        result = await db.execute(
            select(
                Employee.first_name,
                Employee.last_name,

                func.count(
                    Attendance.id
                ).label("total_days"),

                func.sum(
                    case(
                        (
                            Attendance.status
                            == "present",
                            1,
                        ),
                        else_=0,
                    )
                ).label("present"),

                func.sum(
                    case(
                        (
                            Attendance.status
                            == "absent",
                            1,
                        ),
                        else_=0,
                    )
                ).label("absent"),

                func.sum(
                    case(
                        (
                            Attendance.status
                            == "half_day",
                            1,
                        ),
                        else_=0,
                    )
                ).label("half_day"),

                func.sum(
                    case(
                        (
                            Attendance.status
                            == "leave",
                            1,
                        ),
                        else_=0,
                    )
                ).label("leave"),
            )
            .join(
                Attendance.employee
            )
            .where(
                Attendance.employee_id
                == employee_id
            )
            .where(
                extract(
                    "year",
                    Attendance.attendance_date,
                )
                == year
            )
            .where(
                extract(
                    "month",
                    Attendance.attendance_date,
                )
                == month
            )
            .group_by(
                Employee.id
            )
        )

        row = result.one_or_none()

        if not row:
            return None

        return {
            "employee_id": employee_id,
            "employee_name": (
                f"{row.first_name} "
                f"{row.last_name}"
            ),
            "year": year,
            "month": month,
            "present": row.present or 0,
            "absent": row.absent or 0,
            "half_day": row.half_day or 0,
            "leave": row.leave or 0,
            "total_days": row.total_days or 0,
        }