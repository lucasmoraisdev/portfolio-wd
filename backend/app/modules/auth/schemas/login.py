from pydantic import BaseModel, ConfigDict, EmailStr

class LoginRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr

    password: str