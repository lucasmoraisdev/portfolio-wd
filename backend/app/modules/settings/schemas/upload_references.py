from .settings import SettingBase

class UploadReferences(SettingBase):
    logo_main: str | None = None
    logo_white: str | None = None
    logo_small: str | None = None
    favicon: str | None = None
    apple_touch: str | None = None
    og_image: str | None = None
    share_banner: str | None = None