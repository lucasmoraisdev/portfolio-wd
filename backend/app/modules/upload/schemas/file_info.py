from pydantic import Field

from app.modules.upload.schemas.base import UploadBase

class FileInfo(UploadBase):
    original_filename: str = Field(
        ...,
        description="Nome original do arquivo"
    )
    stored_filename: str = Field(
        ...,
        description="Nome único gerado no storage"
    )
    file_path: str = Field(
        ...,
        description="Caminho relativo no storage"
    )
    file_size: int = Field(
        ...,
        description="Tamanho em bytes"
    )
    mime_type: str = Field(
        ...,
        description="Tipo MIME detectado"
    )
    extension: str = Field(
        ...,
        description="Extensão do arquivo"
    )