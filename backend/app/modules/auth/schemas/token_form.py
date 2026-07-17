from pydantic import BaseModel


class TokenFormResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"