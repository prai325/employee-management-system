from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.attendance import AttendanceResponse, AttendanceCreate, AttendanceListResponse, AttendanceUpdate, AttendanceSummaryResponse
from app.services.attendance_service import AttendanceService
from app.utils.attendance_mapper import attendance_response
from app.enums.attendance import AttendanceStatus
from datetime import date

router = APIRouter(prefix="/attendances", tags=["Attendances"])

@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=201,
)
async def create_attendance(
    data: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
):

    try:

        attendance = await (
            AttendanceService
            .create_attendance(
                db=db,
                data=data,
            )
        )

        return attendance_response(
            attendance
        )

    except ValueError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
async def get_attendance(attendance_id: int, db: AsyncSession = Depends(get_db)):
    attendance = await (AttendanceService.get_attendance(db=db, attendance_id=attendance_id))
    if not attendance:

        raise HTTPException(
            status_code=404,
            detail="Attendance not found",
        )

    return attendance_response(
        attendance
    )

@router.get(
    "/",
    response_model=AttendanceListResponse,
)
async def get_attendances(
    search: str | None = None,

    employee_id: int | None = Query(
        None,
        ge=1,
    ),

    status: AttendanceStatus | None = None,

    attendance_date: date | None = None,

    page: int = Query(
        1,
        ge=1,
    ),

    page_size: int = Query(
        10,
        ge=1,
        le=100,
    ),

    db: AsyncSession = Depends(get_db),
):

    result = await (
        AttendanceService
        .get_attendances(
            db=db,
            search=search,
            employee_id=employee_id,
            status=status,
            attendance_date=attendance_date,
            page=page,
            page_size=page_size,
        )
    )

    result["items"] = [
        attendance_response(
            attendance
        )
        for attendance in result["items"]
    ]

    return result

@router.patch(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
async def update_attendance(
    attendance_id: int,
    data: AttendanceUpdate,
    db: AsyncSession = Depends(get_db),
):

    try:

        attendance = await (
            AttendanceService
            .update_attendance(
                db=db,
                attendance_id=attendance_id,
                data=data,
            )
        )

        return attendance_response(
            attendance
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.delete(
    "/{attendance_id}",
    status_code=204,
)
async def delete_attendance(
    attendance_id: int,
    db: AsyncSession = Depends(get_db),
):

    try:

        await (
            AttendanceService
            .delete_attendance(
                db=db,
                attendance_id=attendance_id,
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

@router.get(
    "/summary/{employee_id}",
    response_model=AttendanceSummaryResponse,
)
async def attendance_summary(
    employee_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_db),
):

    result = await (
        AttendanceService
        .attendance_summary(
            db=db,
            employee_id=employee_id,
            year=year,
            month=month,
        )
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Attendance data not found",
        )

    return result