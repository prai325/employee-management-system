from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.designation import (
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse,
    DesignationListResponse
)

from app.services.designation_service import (
    DesignationService
)

router = APIRouter(
    prefix="/designations",
    tags=["Designations"]
)

@router.post(
    "/",
    response_model=DesignationResponse,
    status_code=201
)
async def create_designation(
    data: DesignationCreate,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await (
            DesignationService
            .create_designation(
                db=db,
                data=data
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.get(
    "/{designation_id}",
    response_model=DesignationResponse
)
async def get_designation(
    designation_id: int,
    db: AsyncSession = Depends(get_db)
):

    designation = await (
        DesignationService
        .get_designation(
            db=db,
            designation_id=designation_id
        )
    )

    if not designation:

        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return {
        "id": designation.id,
        "name": designation.name,
        "department_id": (
            designation.department_id
        ),
        "department_name": (
            designation.department.name
        ),
    }

@router.get(
    "/",
    response_model=DesignationListResponse
)
async def get_designations(
    search: str | None = None,

    department_id: int | None = Query(
        None,
        ge=1
    ),

    page: int = Query(
        1,
        ge=1
    ),

    page_size: int = Query(
        10,
        ge=1,
        le=100
    ),

    sort_order: str = Query(
        "asc"
    ),

    db: AsyncSession = Depends(get_db)
):

    return await (
        DesignationService
        .get_designations(
            db=db,
            search=search,
            department_id=department_id,
            page=page,
            page_size=page_size,
            sort_order=sort_order
        )
    )

@router.put(
    "/{designation_id}",
    response_model=DesignationResponse
)
async def update_designation(
    designation_id: int,
    data: DesignationUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        designation = await (
            DesignationService
            .update_designation(
                db=db,
                designation_id=designation_id,
                data=data
            )
        )

        if not designation:

            raise HTTPException(
                status_code=404,
                detail="Designation not found"
            )

        return designation

    except ValueError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


@router.delete(
    "/{designation_id}"
)
async def delete_designation(
    designation_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await (
        DesignationService
        .delete_designation(
            db=db,
            designation_id=designation_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )

    return {
        "message":
        "Designation deleted successfully"
    }