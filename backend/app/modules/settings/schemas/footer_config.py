from pydantic import Field

from .settings import SettingBase

class FooterConfig(SettingBase):
    institunional: str | None = None
    copyright: str | None = None
    developed_by: str | None = None
    quick_links: list[dict[str, str]] = Field(default_factory=list)