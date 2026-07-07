from pydantic import Field

from .settings import SettingBase
from .section_config import SectionConfig

class SectionsConfig(SettingBase):
    hero: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=1))
    about: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=2))
    toys: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=3))
    categories: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=4))
    team: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=5))
    events: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=6))
    municipalities: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=7))
    clients: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=8))
    testionials: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=9))
    faq: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=10))
    contact: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=11))
    map: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=12))
    footer: SectionConfig = Field(default_factory=lambda: SectionConfig(enabled=True, order=13))