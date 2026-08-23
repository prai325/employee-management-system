from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin
# Import the association table and model
from app.models.permissions import role_permission_association, Permission

class Role(Base, TimestampMixin):
    __tablename__="roles"

    id: Mapped[int] = mapped_column(primary_key=True)             # "Mapped" type hints
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # that name is a string column managed by the ORM.

    users = relationship("User", back_populates="role")

    # ADD THIS: Many-to-Many relationship to Permissions
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=role_permission_association,
        back_populates="roles"
    )