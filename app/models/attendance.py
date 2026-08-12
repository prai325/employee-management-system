from datetime import date, datetime, time
from enum import Enum

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import TimestampMixin


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class Attendance(Base, TimestampMixin):
    __tablename__ = "attendances"

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "attendance_date",
            name="uq_employee_attendance_date"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    status: Mapped[AttendanceStatus] = mapped_column(
        String(20),
        nullable=False
    )

    check_in: Mapped[time | None] = mapped_column(
        Time(timezone=True),
        nullable=True
    )

    check_out: Mapped[time | None] = mapped_column(
        Time(timezone=True),
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    employee = relationship(
        "Employee",
        back_populates="attendances"
    )