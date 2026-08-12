from datetime import date, time
from pydantic import BaseModel
from app.enums.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):

    employee_id: int
    attendance_date: date
    status: AttendanceStatus
    check_in: time | None = None
    check_out: time | None = None
    remarks: str | None = None

class AttendanceResponse(BaseModel):

    id: int
    employee_id: int
    employee_name: str
    attendance_date: date
    status: AttendanceStatus
    check_in: time | None
    check_out: time | None
    remarks: str | None

class AttendanceListResponse(BaseModel):

    items: list[AttendanceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class AttendanceUpdate(BaseModel):
    attendance_date: date | None = None
    status: AttendanceStatus | None = None
    check_in: time | None = None
    check_out: time | None = None
    remarks: str | None = None

class AttendanceSummaryResponse(BaseModel):

    employee_id: int
    employee_name: str

    year: int
    month: int

    present: int
    absent: int
    half_day: int
    leave: int

    total_days: int