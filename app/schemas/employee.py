from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    department_id: int
    designation_id: int
    employee_code: str
    joining_date: date
    salary: Decimal = Field(
        gt=0
    )


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    department_id: int | None = None
    designation_id: int | None = None
    employee_code: str | None = None
    joining_date: date | None = None
    salary: Decimal | None = Field(
        default=None,
        gt=0
    )
    is_active: bool | None = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    joining_date: date
    salary: Decimal
    is_active: bool

    department_id: int
    department_name: str

    designation_id: int
    designation_name: str

    first_name: str
    middle_name: str | None
    last_name: str
    
    model_config = ConfigDict(
        from_attributes=True
    )


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int