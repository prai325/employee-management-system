from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin

# 1. Association Table for the Many-to-Many relationship
role_permission_association = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

# 2. Permission Model
class Permission(Base, TimestampMixin):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Example names: "user:create", "user:delete", "report:view"
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) 
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationship back to Roles
    roles: Mapped[list["Role"]] = relationship(
        "Role", 
        secondary=role_permission_association, 
        back_populates="permissions"
    )
