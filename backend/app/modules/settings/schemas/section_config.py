from .settings import SettingBase

class SectionConfig(SettingBase):
    enabled: bool = True
    order: int = 0