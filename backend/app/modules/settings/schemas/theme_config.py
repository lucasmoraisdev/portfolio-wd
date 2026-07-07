from pydantic import Field, field_validator

from .settings import SettingBase

class ThemeConfig(SettingBase):
    primary: str = Field(default="#3B82F6")
    secondary: str = Field(default="#10B981")
    accent: str = Field(default="#F59E0B")
    background: str = Field(default="#FFFFFF")
    text: str = Field(default="#1F2937")
    button: str = Field(default="#3B82F6")

    @field_validator("primary", "secondary", "accent", "background", "text", "button")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        if v and not v.startswith("#"):
            raise ValueError("Cor deve ser um hex vá´lido (Ex: #3B82F6)")
        return v