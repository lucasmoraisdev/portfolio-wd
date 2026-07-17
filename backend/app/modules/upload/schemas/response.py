from pydantic import Field, model_validator
from uuid import UUID

from app.modules.upload.schemas.file_info import FileInfo
from app.core.config import settings

class UploadResponse(FileInfo):
    id: UUID
    public_url: str = Field(
        ...,
        description="URL pública para acesso"
    )

    @model_validator(mode="after")
    def set_dynamic_public_url(self) -> "UploadResponse":
        self.public_url = f"{settings.app.base_url}{settings.app.api_prefix}/uploads/{self.id}/file"
        return self