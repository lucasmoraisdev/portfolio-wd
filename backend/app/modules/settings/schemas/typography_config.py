from pydantic import Field

from .settings import SettingBase

class TypographyConfig(SettingBase):
    font_family: str = Field(default="Inter, sans-serif")
    font_weight: str = Field(default="400")
    base_size: str = Field(default="16px")