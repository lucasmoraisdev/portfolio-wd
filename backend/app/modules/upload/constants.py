from pathlib import Path

from app.core.config import settings

UPLOAD_PREFIX = '/uploads'
UPLOAD_TAG = 'Uploads'

UPLOAD_BASE_DIR = Path(settings.storage.upload_directory)

ALLOWED_IMAGE_EXTENSIONS: set[str] = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp",
    "svg",
    "bmp",
    "ico"
}

ALLOWED_VIDEO_EXTENSIONS: set[str] = {
    "mp4",
    "webm",
    "ogg",
    "mov",
    "avi"
}

ALLOWED_ALL_EXTENSIONS: set[str] = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_VIDEO_EXTENSIONS)

MAX_FILE_SIZE_BYTES = settings.storage.max_upload_size
MAX_IMAGE_SIZE_BYTES = min(MAX_FILE_SIZE_BYTES, 5 * 1024 * 1024)

DIRECTORY_STRUCTURE = "{type}/{year}/{month}"
FILENAME_FORMAT = "{uuid}.{ext}"

CHUNK_SIZE = 1024 * 1024

UPLOAD_TABLE_NAME = "uploads"