from app.modules.user.schemas import UserResponse
from app.shared.responses import ApiResponse

class MeResponse(UserResponse):
    pass

AuthMeApiResponse = ApiResponse[MeResponse]