from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, true, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true(), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default=false(), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    role = relationship("Role", back_populates="users")
    employee = relationship("Employee", back_populates="user", uselist=False)