from pydantic import BaseModel, ConfigDict


class DesignationCreate(BaseModel):
    name: str
    department_id: int


class DesignationUpdate(BaseModel):
    name: str | None = None
    department_id: int | None = None


class DesignationResponse(BaseModel):
    id: int
    name: str
    department_id: int
    department_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class DesignationListResponse(BaseModel):
    items: list[DesignationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int