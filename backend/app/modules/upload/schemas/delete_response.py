from app.modules.upload.schemas.base import UploadBase

class UploadDeleteResponse(UploadBase):
    deleted: bool = True
    filename: str
    message: str = "Arquivo removido com sucesso."