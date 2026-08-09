from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base_model import TimestampMixin
from enum import Enum 

class DocumentType(str, Enum):
    AADHAAR = "aadhaar"
    PAN = "pan"
    RESUME = "resume"
    OFFER_LETTER = "offer_letter"
    EXPERIENCE_LETTER = "experience_letter"
    OTHER = "other"

class EmployeeDocument(Base, TimestampMixin):
    __tablename__="employee_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False, index=True)
    document_type: Mapped[DocumentType] = mapped_column(String(50), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    employee = relationship("Employee", back_populates="documents")