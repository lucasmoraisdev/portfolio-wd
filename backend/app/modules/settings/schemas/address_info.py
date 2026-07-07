from pydantic import Field

from .settings import SettingBase

class AddressInfo(SettingBase):
    zip: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    sate: str | None = None
    country: str | None = Field(default="Brasil")
    latitude: float | None = None
    longitude: float | None = None