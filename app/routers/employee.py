from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
)

from app.services.employee_service import (
    EmployeeService,
)
from app.utils.employee_mapper import employee_response


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201,
)
async def create_employee(
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):

    try:

        employee = await (
            EmployeeService
            .create_employee(
                db=db,
                data=data,
            )
        )

        return employee_response(employee)

    except ValueError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

@router.get(
    "/",
    response_model=EmployeeListResponse,
)
async def get_employees(
    search: str | None = None,

    department_id: int | None = Query(
        None,
        ge=1,
    ),

    designation_id: int | None = Query(
        None,
        ge=1,
    ),

    is_active: bool | None = None,

    page: int = Query(
        1,
        ge=1,
    ),

    page_size: int = Query(
        10,
        ge=1,
        le=100,
    ),

    sort_order: str = Query(
        "asc",
    ),

    db: AsyncSession = Depends(get_db),
):

    return await (
        EmployeeService
        .get_employees(
            db=db,
            search=search,
            department_id=department_id,
            designation_id=designation_id,
            is_active=is_active,
            page=page,
            page_size=page_size,
            sort_order=sort_order,
        )
    )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
):

    employee = await (
        EmployeeService
        .get_employee(
            db=db,
            employee_id=employee_id,
        )
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return {
        "id": employee.id,

        "first_name":
            employee.first_name,

        "middle_name":
            employee.middle_name,

        "last_name":
            employee.last_name,

        "employee_code":
            employee.employee_code,

        "department_id":
            employee.department_id,

        "department_name":
            employee.department.name,

        "designation_id":
            employee.designation_id,

        "designation_name":
            employee.designation.name,

        "joining_date":
            employee.joining_date,

        "salary":
            employee.salary,

        "is_active":
            employee.is_active,
    }