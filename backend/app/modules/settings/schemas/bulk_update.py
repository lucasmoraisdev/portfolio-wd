from pydantic import Field
from typing import Any

from .settings import SettingBase

class SettingBulkUpdate(SettingBase):
    settings: dict[str, Any] = Field(
        ...,
        description="Dict de key -> value"
    )