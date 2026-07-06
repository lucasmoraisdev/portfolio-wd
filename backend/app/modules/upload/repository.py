from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.upload.models import Upload
from app.modules.upload.schemas import FileInfo

from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

class UploadRepository:
    def __init__(self, db: Session):
        self._db = db

    def create(self, file_info: FileInfo, public_url: str) -> Upload:
        upload = Upload(
            id=uuid4(),
            original_filename=file_info.original_filename,
            stored_filename=file_info.stored_filename,
            file_path=file_info.file_path,
            public_url=public_url,
            file_size=file_info.file_size,
            mime_type=file_info.mime_type,
            extension=file_info.extension
        )
        self._db.add(upload)
        self._db.commit()
        self._db.refresh(upload)
        return upload
    
    def get_by_id(self, upload_id: UUID) -> Upload | None:
        stmt = select(Upload).where(
            Upload.id == upload_id
        )

        return self._db.scalar(stmt)
    
    def list_all(self, limit: int = 100, offset: int = 0) -> list[Upload]:
        stmt = (
            select(Upload)
            .order_by(Upload.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._db.scalars(stmt).all()
    
    def delete(self, upload_id: UUID) -> bool:
        upload = self.get_by_id(upload_id)
        if not upload:
            return False

        stmt = delete(Upload).where(Upload.id == upload_id)
        self._db.execute(stmt)
        self._db.commit()
        return True
    