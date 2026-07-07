from pydantic import Field
from typing import Any

from .settings import SettingBase

class SettingUpdate(SettingBase):
    value: Any
    type: str = Field(
        default=None, 
        pattern="^(string|int|float|bool|json|upload)$"
    )
    is_public: bool | None = None