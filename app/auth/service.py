from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.auth.schemas import LoginRequest


class AuthService:

    @staticmethod
    async def login(
        db: AsyncSession,
        data: LoginRequest,
    ):

        result = await db.execute(
            select(User)
            .where(User.email == data.email)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            data.password,
            user.password,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        if not user.is_active:
            raise ValueError(
                "User account is inactive"
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "role_id": str(user.role_id),
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }