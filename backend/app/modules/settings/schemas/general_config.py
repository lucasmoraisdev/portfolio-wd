from pydantic import Field

from .settings import SettingBase

class GeneralConfig(SettingBase):
    language: str = Field(default="pt-BR")
    timezone: str = Field(default="America/Sao_Paulo")
    date_format: str = Field(default="DD/MM/YYYY")
    phone_format: str | None = None