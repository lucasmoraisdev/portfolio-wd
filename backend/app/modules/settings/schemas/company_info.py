from .settings import SettingBase

class CompanyInfo(SettingBase):
    name: str | None = None
    trading_name: str | None = None
    slogan: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    cnp: str | None = None
    founding_year: str | None = None