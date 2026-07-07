from pydantic import Field

from .settings import SettingBase

class LayoutConfig(SettingBase):
    max_content_width: str = Field(default="1280px")
    border_radius: str = Field(default="8px")
    shadows: bool = Field(default=True)
    spacing: str = Field(default="medium")