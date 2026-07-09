from pydantic import Field
from typing import Any
from uuid import UUID

from .settings import SettingBase

class SettingResponse(SettingBase):
    id: UUID
    key: str
    value: Any
    type: str
    is_public: bool
    
class SettingPublicResponse(SettingBase):
    """Resposta para consumo no front"""
    company: dict[str, Any] = Field(default_factory=dict)
    hero: dict[str, Any] = Field(default_factory=dict)
    contact: dict[str, Any] = Field(default_factory=dict)
    address: dict[str, Any] = Field(default_factory=dict)
    social: dict[str, Any] = Field(default_factory=dict)
    seo: dict[str, Any] = Field(default_factory=dict)
    theme: dict[str, Any] = Field(default_factory=dict)
    typography: dict[str, Any] = Field(default_factory=dict)
    layout: dict[str, Any] = Field(default_factory=dict)
    sections: dict[str, Any] = Field(default_factory=dict)
    footer: dict[str, Any] = Field(default_factory=dict)
    general: dict[str, Any] = Field(default_factory=dict)
    uploads: dict[str, str | Any] = Field(default_factory=dict)

class SettingAdminResponse(SettingBase):
    """Resposta admin com tudo"""
    company: dict[str, Any] = Field(default_factory=dict)
    hero: dict[str, Any] = Field(default_factory=dict)
    contact: dict[str, Any] = Field(default_factory=dict)
    address: dict[str, Any] = Field(default_factory=dict)
    social: dict[str, Any] = Field(default_factory=dict)
    seo: dict[str, Any] = Field(default_factory=dict)
    analytics: dict[str, Any] = Field(default_factory=dict)
    theme: dict[str, Any] = Field(default_factory=dict)
    typography: dict[str, Any] = Field(default_factory=dict)
    layout: dict[str, Any] = Field(default_factory=dict)
    sections: dict[str, Any] = Field(default_factory=dict)
    footer: dict[str, Any] = Field(default_factory=dict)
    general: dict[str, Any] = Field(default_factory=dict)
    uploads: dict[str, str | Any] = Field(default_factory=dict)
