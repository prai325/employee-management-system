from datetime import date
from enum import Enum
from sqlalchemy import Date, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import TimestampMixin
from app.db.base import Base

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class LeaveRequest(Base, TimestampMixin):
    __tablename__="leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_types.id"), nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[LeaveStatus] = mapped_column(String(20), nullable=False)

    employee = relationship("Employee", back_populates="leave_requests")
    leave_type = relationship("LeaveType", back_populates="leave_requests")