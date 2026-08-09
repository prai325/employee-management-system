from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin

class Department(Base, TimestampMixin):
    __tablename__="departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    employees = relationship("Employee", back_populates="department")
    designations = relationship(
        "Designation",
        back_populates="department"
    )