from pydantic import Field
from uuid import UUID

from app.modules.upload.schemas import FileInfo

class UploadResponse(FileInfo):
    id: UUID
    public_url: str = Field(
        ...,
        description="URL pública para acesso"
    )