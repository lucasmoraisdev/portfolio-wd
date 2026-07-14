
from .settings import SettingBase

class ContactInfo(SettingBase):
    phone_primary: str | None = None
    phone_secondary: str | None = None
    whatsapp: str | None = None
    email_commercial: str | None = None
    email_financial: str | None = None
    business_hours: str | None = None
    