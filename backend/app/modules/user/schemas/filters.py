from pydantic import BaseModel, ConfigDict, Field

class UserFilter(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    name: str | None = None

    email: str | None = None

    is_active: bool | None = None

    page: int = Field(
        default=1,
        ge=1,
        description="Page number for pagination. Must be greater than or equal to 1."
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page for pagination. Must be between 1 and 100."
    )