from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin

class Role(Base, TimestampMixin):
    __tablename__="roles"

    id: Mapped[int] = mapped_column(primary_key=True)             # "Mapped" type hints
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # that name is a string column managed by the ORM.

    users = relationship("User", back_populates="role")
