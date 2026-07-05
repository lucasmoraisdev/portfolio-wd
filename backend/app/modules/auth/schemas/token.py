from pydantic import BaseModel
from app.shared.responses import ApiResponse

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

AuthTokenApiResponse = ApiResponse[TokenResponse]