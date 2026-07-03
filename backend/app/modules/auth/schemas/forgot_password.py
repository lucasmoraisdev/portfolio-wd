from pydantic import BaseModel, ConfigDict, EmailStr

class ForgotPasswordRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr