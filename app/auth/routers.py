from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.auth.schemas import (
    LoginRequest,
    TokenResponse,
)
from app.auth.service import AuthService
from app.models.user import User
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    try:
        return await AuthService.login(
            db=db,
            data=data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

# Test API
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):

    return current_user