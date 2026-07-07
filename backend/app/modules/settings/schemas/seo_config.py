from pydantic import Field

from .settings import SettingBase

class SEOConfig(SettingBase):
    title: str | None = None
    description: str | None = None
    keywords: str | None = None
    canonical: str | None = None
    robots: str | None = Field(default="index, follow")
    author: str | None = None
    theme_color: str | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | None = None
    twitter_card: str | None = Field(default="summary_large_image")