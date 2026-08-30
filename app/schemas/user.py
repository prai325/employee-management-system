from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    first_name: str
    middle_name: str | None = None
    last_name: str
    email: EmailStr
    password: str
    role_id: int
    profile_image: str | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    role_id: int | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    profile_image: str | None = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    middle_name: str | None
    last_name: str
    email: EmailStr
    role_id: int
    is_active: bool
    is_verified: bool
    last_login: datetime | None
    profile_image: str | None

    model_config = ConfigDict(
        from_attributes=True
    )

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int