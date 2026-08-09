from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserListResponse
)

from app.services.user_service import (
    UserService
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await UserService.create_user(
            db=db,
            data=data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    user = await UserService.get_user(
        db=db,
        user_id=user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.get("/", response_model=UserListResponse)
async def get_users(
    search: str | None = None,

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

    return await UserService.get_users(
        db=db,
        search=search,
        page=page,
        page_size=page_size,
        sort_order=sort_order
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):

    try:

        user = await UserService.update_user(
            db=db,
            user_id=user_id,
            data=data
        )

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    except ValueError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

@router.delete(
    "/{user_id}"
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted = await UserService.delete_user(
        db=db,
        user_id=user_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }