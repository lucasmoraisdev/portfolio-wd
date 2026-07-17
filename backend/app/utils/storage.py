"""
Abstração de storage para uploads.

"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO

from app.core.config import settings
from app.shared.exceptions import StorageException, FileNotFoundException

logger = logging.getLogger(__name__)

class StorageBackend(ABC):
    """Interface abstrata para backend storage."""
    # Caso queria fazer mais de uma opcao de storage tbm (S3, GCP....)

    @abstractmethod
    async def save(
        self,
        file_stream: BinaryIO,
        destination_path: str,
    ) -> int:
        """
        Salva o arquivo no storage.

        Args:
            file_stream: Stream do arquivo (seekable).
            destination_path: Caminho relativo de destino.

        Returns:
            Tamanho do arquivo saldo em bytes
        """
        ...
    
    @abstractmethod
    async def delete(self, file_path: str) -> bool:
        """
        Remove o arquivo do storage.

        Args:
            file_path: Caminho relativo do arquivo.
        
        Returns:
            True se removido com sucesso
        """
        ...
    
    @abstractmethod
    async def exists(self, file_path: str) -> bool:
        """
        Verifica se o arquivo existe no storage.

        Args:
            file_path: caminho do arquivo.
        
        Returns:
            True se arquivo existir.
        """
        ...

    @abstractmethod
    def get_public_url(self, file_path: str) -> str:
        """
        Retorna a URL pública para aceso ao arquivo.
        
        Args:
            file_path: caminho do arquivo.
        
        Returns:
            URL do arquivo para acesso.
        """
        ...
    
    @abstractmethod
    def get_full_path(self, file_path: str) -> Path:
        """
        Retorna o caminho absoluto no filesystem (quando aplicável)
        """

class LocalStorageBackend(StorageBackend):
    """
    Backend de storage local usando filesystem

    Usa o diretório configurado em core/config.py

    Estrutura de diretórios:
        {STORAGE_UPLOAD_DIRECTORY}/
        ├── images/
        │   ├── 2026/
        │   │   └── 07/
        │   │       └── a1b2c3d4.jpg
        │   └── 2026/
        │       └── 08/
        │           └── e5f6g7h8.png
        └── documents/
            └── 2026/
                └── 07/
                    └── relatorio.pdf
    """

    def __init__(self, base_dir: Path | str | None = None) -> None:
        self.base_dir = Path(base_dir or settings.storage.upload_directory).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save(
        self,
        file_stream: BinaryIO,
        destination_path: str,
    ) -> int:
        """Salva o arquivo localmente em chunks"""
        full_path = self.base_dir / destination_path

        full_path.parent.mkdir(parents=True, exist_ok=True)

        total_size = 0
        chunk_size = 1024 * 1024

        try:
            with open(full_path, "wb") as out_file:
                while chunk := file_stream.read(chunk_size):
                    out_file.write(chunk)
                    total_size += len(chunk)

            logger.info(
                "Arquivo salvo: %s (%d bytes)",
                full_path,
                total_size
            )
            return total_size
        except OSError as exc:
            if full_path.exists():
                full_path.unlink(missing_ok=True)
            raise StorageException(
                f"Falha ao salvar arquivo: {exc}"
            ) from exc
        
    async def delete(self, file_path: str) -> bool:
        """Remove o arquivo do do filesystem."""
        full_path = self.base_dir / file_path

        if not full_path.exists():
            logger.warning("Tentativa de deletar arquivo inexistente: %s", full_path)
            raise FileNotFoundException(file_path)
        
        try:
            full_path.unlink()
            logger.info("Arquivo removido: %s", full_path)

            self._cleanup_empty_dirs(full_path.parent)
            return True
        except OSError as exc:
            raise StorageException(
                f"Falha ao remover arquivo: {exc}"
            ) from exc
        
    async def exists(self, file_path: str) -> bool:
        """Verificar se o arquivo existe"""
        full_path = self.base_dir / file_path
        return full_path.is_file()
    
    def get_public_url(self, file_path):
        """Retorna a URL pública"""
        return f"{settings.app.base_url}/uploads/{file_path}"
    
    def get_full_path(self, file_path):
        return self.base_dir / file_path
    
    def _cleanup_empty_dirs(self, directory: Path) -> None:
        """Remove diretórios vazios recursivamente até o base_dir"""
        try:
            for parent in directory.parents:
                if parent in directory.parents:
                    if parent == self.base_dir:
                        break
                    if parent.exists() and not any(parent.iterdir()):
                        parent.rmdir()
        except OSError:
            pass

class S3StorageBackend(StorageBackend):
    """
    Backend de storage para Amazon S3 (esqueleto para futura implementação).

    Uso futuro:
        storage = S3StorageBackend(
            bucket="my-bucket",
            region="us-east-1",
        )
    """

    def __init__(self, bucket: str, region: str = "us-east-1") -> None:
        self.bucket = bucket
        self.region = region
        # self.s3_client = boto3.client("s3", region_name=region)

    async def save(self, file_stream: BinaryIO, destination_path: str) -> int:
        raise NotImplementedError("S3 storage não implementado ainda")

    async def delete(self, file_path: str) -> bool:
        raise NotImplementedError("S3 storage não implementado ainda")

    async def exists(self, file_path: str) -> bool:
        raise NotImplementedError("S3 storage não implementado ainda")

    def get_public_url(self, file_path: str) -> str:
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{file_path}"
    
    def get_full_path(self, file_path: str) -> Path:
        raise NotImplementedError("S3 não possui caminho local")