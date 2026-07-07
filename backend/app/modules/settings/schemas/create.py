from pydantic import Field
from typing import Any

from .settings import SettingBase

class SettingCreate(SettingBase):
    key: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    value: Any
    type: str = Field(
        default="string", 
        pattern="^(string|int|float|bool|json|upload)$"
    )
    is_public: bool = Field(default=False)