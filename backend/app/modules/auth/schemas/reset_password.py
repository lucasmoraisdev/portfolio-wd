from pydantic import BaseModel, ConfigDict, Field

class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    token: str

    password: str = Field(
        min_length=8,
        max_length=128
    )