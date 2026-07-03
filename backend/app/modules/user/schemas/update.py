from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )

    is_active: bool | None = None