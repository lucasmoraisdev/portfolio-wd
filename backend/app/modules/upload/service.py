import logging
import mimetypes
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.modules.upload.constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    DIRECTORY_STRUCTURE,
    FILENAME_FORMAT
)
from app.shared.exceptions import (
    InvalidFileExtensionException,
    FileTooLargeException,
    FileNotFoundException,
    FileCorruptedException
)
from app.modules.upload.schemas import UploadResponse, FileInfo
from app.utils.storage import StorageBackend, LocalStorageBackend
from app.modules.upload.repository import UploadRepository

logger = logging.getLogger(__name__)

class UploadService:
    """
    Service responsável pelo processamento de uploads.

    Fluxo:
        1. Valida extensão e tamanho (usa STORAGE_MAX_UPLOAD_SIZE do config)
        2. Gera nome único e estrutura de diretórios
        3.. Salva no storage backend
        4. Persiste metadados no banco
    """

    def __init__(
        self,
        repository: UploadRepository,
        storage: StorageBackend | None = None
    ) -> None:
        self.repository = repository
        self.storage = storage or LocalStorageBackend()

    async def upload(
        self,
        file: UploadFile,
        file_type: str = "images",
    ) -> UploadResponse:
        """
        Processa o upload de um arquivo.

        Args:
            file: Arquivo recebido via multipart/form-data.
            file_type: Tipo de arquivo para organização em diretórios (imagens, documentos, avatares, etc...)

        Returns:
            UploadResponse com metadados do arquivo salvo.
        """
        self._validate_file(file)

        file_info = self._generate_file_info(file, file_type)

        file_size = await self.storage.save(
            file_stream=file.file,
            destination_path=file_info.file_path,
        )

        file_info.file_size = file_size

        public_url = self.storage.get_public_url(file_info.file_path)

        upload_record = self.repository.create(file_info, public_url)

        logger.info(
            "Upload realizado: %s -> %s (%d bytes)",
            file_info.original_filename,
            file_info.stored_filename,
            file_size
        )

        return UploadResponse.model_validate(upload_record)
    
    async def delete(self, upload_id: UUID) -> UploadResponse:
        """
        Remove um arquivo do storage e marca como deletado do banco.

        Args:
            upload_id: ID do upload no banco de dados.

        Returns:
            UploadResponse do arquivo removido.
        """
        upload = self.repository.get_by_id(upload_id)
        if not upload:
            raise FileNotFoundException(str(upload_id))
        
        await self.storage.delete(upload.file_path)

        self.repository.soft_delete(upload_id)

        logger.info("Upload removido: %s", upload.stored_filename)

        return UploadResponse.model_validate(upload)
        
    def get_by_id(self, upload_id: UUID) -> UploadResponse:
        """Busca um upload pelo ID"""
        upload = self.repository.get_by_id(upload_id)
        if not upload:
            raise FileNotFoundException(str(upload_id))
        return UploadResponse.model_validate(upload)

    def list_uploads(self, limit: int = 100, offset: int = 0) -> list[UploadResponse]:
        """List uploads com paginação"""
        uploads = self.repository.list_all(limit=limit, offset=offset)
        return [UploadResponse.model_validate(u) for u in uploads]

    def _validate_file(self, file: UploadFile) -> None:
        """
        Valida extensão e tamanho do arquivo.

        Usa STORAGE_MAX_UPLOAD_SIZE do core/config.py

        Raises:
            InvalidFileExtensionException: Se a extensão não for permitida.
            FileTooLargeException: Se o arquivo exceder o limite.
        """
        if not file.filename:
            raise FileCorruptedException("Nome do arquivo não fornecido")
        
        extension = self._get_extension(file.filename)
        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise InvalidFileExtensionException(
                extension=extension,
                allowed=ALLOWED_IMAGE_EXTENSIONS
            )
        
        max_upload_size = settings.storage.max_upload_size
        max_size = (
            min(max_upload_size, 5 * 1024 * 1024)
            if extension in ALLOWED_IMAGE_EXTENSIONS
            else max_upload_size
        )

        self._validate_file(file, max_size)
    
    def _validate_size(self, file: UploadFile, max_size: int) -> None:
        """
        Valida o tamanho do arquivo lendo em chunks.

        Raises:
            FileTooLargeException: Se exceder o limite.
        """
        total_size = 0
        chunk_size = 1024 * 1024

        while chunk := file.file.read(chunk_size):
            total_size += len(chunk)
            if total_size > max_size:
                raise FileTooLargeException(
                    size=total_size,
                    max_size=max_size
                )
        
        file.file.seek(0)
    
    def _generate_file_info(self, file: UploadFile, file_type: str) -> FileInfo:
        """
        Gera nome único e estrutura de diretórios para o arquivo.

        Estrutura: {STORAGE_UPLOAD_DIRECTORY}/{tipo}/{ano}/{mes}/{uuid}.{ext}
        Exemplo: uploads/images/2026/07/a1b2c3d4-...1wd1.jpg
        """
        original_filename = file.filename or "unknown"
        extension = self._get_extension(original_filename)
        mime_type = file.content_type or mimetypes.guess_type(original_filename)[0] or "application/octet-stream"

        unique_id = str(uuid4())
        stored_filename = FILENAME_FORMAT.format(
            uuid=unique_id,
            ext=extension
        )

        now = datetime.now()
        file_path = DIRECTORY_STRUCTURE.format(
            type=file_type,
            year=now.year,
            month=f"{now.month:02d}",            
        ) + f"/{stored_filename}"

        return FileInfo(
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            full_path=str(self.storage.get_full_path(file_path)),
            file_size=0,
            mime_type=mime_type
        )
    
    @staticmethod
    def _get_extension(filename: str) -> str:
        """Extrai a extensão do filename em lowercase."""
        return Path(filename).suffix.lstrip(".").lower()