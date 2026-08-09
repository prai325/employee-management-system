from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin

class Employee(Base, TimestampMixin):
    __tablename__="employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    designation_id: Mapped[int] = mapped_column(ForeignKey("designations.id"), nullable=False)
    employee_code: Mapped[int] = mapped_column(String(100), unique=True, nullable=False, index=True)
    first_name: Mapped[int] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[int] = mapped_column(String(100), nullable=False)
    last_name: Mapped[int] = mapped_column(String(100), nullable=False)
    phone: Mapped[int] = mapped_column(String(20), nullable=True)
    joining_date: Mapped[int] = mapped_column(Date, nullable=False)
    salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"), nullable=True, index=True
)
    
    user = relationship("User", back_populates="employee")
    department = relationship("Department", back_populates="employees")
    designation = relationship("Designation", back_populates="employees")
    attendances = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")
    shift = relationship("Shift", back_populates="employees")
    emergency_contacts = relationship(
        "EmergencyContact",
        back_populates="employee"
    )