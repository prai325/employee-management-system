from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Role(Base):
    __tablename__="roles"

    id: Mapped[int] = mapped_column(primary_key=True)             # "Mapped" type hints
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # that name is a string column managed by the ORM.
