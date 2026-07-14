from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )

    name: str = Field()
    version: str = Field(default="0.1.0")
    env: str = Field(default="development")

    debug: bool = Field(env="DEBUG", default=False)
    api_prefix: str = Field(default="/api/v1")
    log_level: str = Field(default="INFO")

    @field_validator("env")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "production", "testing"}
        if v.lower() not in allowed:
            raise ValueError(f"Env environment not allowed. Got {v.lower()}")
        return v.lower()

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )

    url: str = Field()
    pool_size: int = Field(default=5)
    max_overflow: int = Field(default=10)
    echo: bool = Field(default=False)

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v:
            raise ValueError("Database URL can not be empty")
        return v
    
class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    algorithm: str = Field(default="HS256")
    secret_key: str = Field()
    access_token_expire_minutes: int = Field(
        alias="ACCESS_TOKEN_EXPIRE_MINUTES", default=60 * 24 * 7
    )

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if not v:
            raise ValueError("JWT secret key can not be empty")
        elif len(v) < 32:
            raise ValueError("JWT secret key must be at least 32 characters long")
        return v
    
class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="STORAGE_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    upload_directory: str = Field(alias="STORAGE_UPLOAD_DIRECTORY")
    max_upload_size: int = Field(alias="STORAGE_MAX_UPLOAD_SIZE")

    @field_validator("upload_directory")
    @classmethod
    def ensure_upload_directory(cls, v: str) -> str:
        if not v:
            raise ValueError("Upload directory can not be empty")
        path = Path(v)
        if not path.exists() or not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
            return str(path.resolve())
        return v
    
class CORSSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    origin: list[str] = Field(alias="CORS_ORIGINS", default=["*"])
    
    @field_validator("origin", mode="before")
    @classmethod
    def parse_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            raise ValueError("CORS_ORIGINS must be a string or a list of strings")

class Settings:
    """ Agregador de todas as configurações da aplicação."""

    def __init__(self):
        self.app = AppSettings()
        self.database = DatabaseSettings()
        self.jwt = JWTSettings()
        self.storage = StorageSettings()
        self.cors = CORSSettings()

    def __repr__(self) -> str:
        return (
            f"Settings("
            f"app={self.app}, "
            f"database={self.database}, "
            f"jwt={self.jwt}, "
            f"storage={self.storage}, "
            f"cors={self.cors}"
            f")"
        )

@lru_cache()
def get_settings() -> Settings:
    """ Retorna uma instância cacheada de Settings."""
    return Settings()

settings = get_settings()

    