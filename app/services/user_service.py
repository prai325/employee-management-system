from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password
from app.schemas.user import UserCreate

class UserService:

    @staticmethod
    async def create_user(
        db: AsyncSession,
        data: UserCreate
    ) -> User:

        result = await db.execute(
            select(User).where(
                User.email == data.email
            )
        )

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError(
                "User with this email already exists"
            )

        result = await db.execute(
            select(Role).where(
                Role.id == data.role_id
            )
        )

        role = result.scalar_one_or_none()

        if not role:
            raise ValueError("Role not found")

        hashed_password = hash_password(
            data.password
        )

        user = User(
            first_name=data.first_name,
            middle_name=data.middle_name,
            last_name=data.last_name,
            email=data.email,
            password=hashed_password,
            role_id=data.role_id
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def get_user(
        db: AsyncSession,
        user_id: int
    ) -> User | None:

        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_users(
        db: AsyncSession,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_order: str = "asc"
    ):

        offset = (
            page - 1
        ) * page_size

        # query = select(User).options(defer(User.password))
        query = select(User)

        count_query = select(
            func.count(User.id)
        )

        if search:

            search_filter = or_(
                User.first_name.ilike(
                    f"%{search}%"
                ),
                User.middle_name.ilike(
                    f"%{search}%"
                ),
                User.last_name.ilike(
                    f"%{search}%"
                ),
                User.email.ilike(
                    f"%{search}%"
                )
            )

            query = query.where(
                search_filter
            )

            count_query = count_query.where(
                search_filter
            )

        if sort_order.lower() == "desc":

            query = query.order_by(
                User.created_at.desc()
            )

        else:

            query = query.order_by(
                User.created_at.asc()
            )

        query = (
            query
            .offset(offset)
            .limit(page_size)
        )

        result = await db.execute(query)

        users = list(
            result.scalars().all()
        )

        count_result = await db.execute(
            count_query
        )

        total = count_result.scalar_one()

        total_pages = (
            total + page_size - 1
        ) // page_size

        return {
            "items": users,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        data
    ):

        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return None

        if data.email is not None:

            existing = await db.execute(
                select(User).where(
                    User.email == data.email,
                    User.id != user_id
                )
            )

            if existing.scalar_one_or_none():
                raise ValueError(
                    "Email already exists"
                )

            user.email = data.email

        if data.first_name is not None:
            user.first_name = data.first_name

        if data.middle_name is not None:
            user.middle_name = data.middle_name

        if data.last_name is not None:
            user.last_name = data.last_name

        if data.role_id is not None:

            role_result = await db.execute(
                select(Role).where(
                    Role.id == data.role_id
                )
            )

            role = role_result.scalar_one_or_none()

            if not role:
                raise ValueError(
                    "Role not found"
                )

            user.role_id = data.role_id

        if data.is_active is not None:
            user.is_active = data.is_active

        if data.is_verified is not None:
            user.is_verified = data.is_verified

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: int
    ) -> bool:

        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            return False

        await db.delete(user)

        await db.commit()

        return True