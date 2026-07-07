from pydantic import Field

from .settings import SettingBase

class HeroConfig(SettingBase):
    title: str | None = None
    subtitle: str | None = None
    text: str | None = None
    primary_button: str | None = None
    primary_link: str | None = None
    secondary_button: str | None = None
    secondary_link: str | None = None
    background_image: str | None = None
    background_video: str | None = None
    carousel_images: list[str] = Field(default_factory=list)
    carousel_transition: int = Field(default=5, ge=1, le=10)

    