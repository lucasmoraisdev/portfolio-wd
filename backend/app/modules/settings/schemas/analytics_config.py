from .settings import SettingBase

class AnalyticsConfig(SettingBase):
    google_analytics: str | None = None
    google_tag_manager: str | None = None
    meta_pixel: str | None = None
    google_search_console: str | None = None