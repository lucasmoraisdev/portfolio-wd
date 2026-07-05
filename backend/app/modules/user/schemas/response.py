from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from app.shared.responses import ApiResponse

class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    
    name: str

    email: EmailStr

    is_active: bool

    created_at: datetime

    updated_at: datetime

UserApiResponse = ApiResponse[UserResponse]