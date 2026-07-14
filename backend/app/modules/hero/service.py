from typing import Any

from app.modules.settings.repository import SettingsRepository
from app.modules.settings.constants import SettingKeys
from app.modules.hero.schemas import HeroResponse, HeroUpdate

class HeroService:
    def __init__(self, repository: SettingsRepository) -> None:
        self.repository = repository

    def _get_val(self, key: str, default: Any = None) -> Any:
        setting = self.repository.get_by_key(key)
        return setting.value if setting and setting.value is not None else default

    def _set_val(self, key: str, value: Any, type_: str = "string") -> None:
        self.repository.create_or_update(key, value, type_, is_public=True)

    def get_hero(self) -> HeroResponse:
        return HeroResponse(
            title=self._get_val(SettingKeys.HERO_TITLE),
            subtitle=self._get_val(SettingKeys.HERO_SUBTITLE),
            text=self._get_val(SettingKeys.HERO_TEXT),
            primary_button=self._get_val(SettingKeys.HERO_PRIMARY_BUTTON),
            primary_link=self._get_val(SettingKeys.HERO_PRIMARY_LINK),
            secondary_button=self._get_val(SettingKeys.HERO_SECONDARY_BUTTON),
            secondary_link=self._get_val(SettingKeys.HERO_SECONDARY_LINK),
            background_image=self._get_val(SettingKeys.HERO_BACKGROUND_IMAGE),
            background_video=self._get_val(SettingKeys.HERO_BACKGROUND_VIDEO),
            carousel_images=self._get_val(SettingKeys.HERO_CAROUSEL_IMAGES, []),
            carousel_transition=self._get_val(SettingKeys.HERO_CAROUSEL_TRANSITION, 5),
        )

    def update_hero(self, data: HeroUpdate) -> HeroResponse:
        key_mappings = [
            (SettingKeys.HERO_TITLE, "title", "string"),
            (SettingKeys.HERO_SUBTITLE, "subtitle", "string"),
            (SettingKeys.HERO_TEXT, "text", "string"),
            (SettingKeys.HERO_PRIMARY_BUTTON, "primary_button", "string"),
            (SettingKeys.HERO_PRIMARY_LINK, "primary_link", "string"),
            (SettingKeys.HERO_SECONDARY_BUTTON, "secondary_button", "string"),
            (SettingKeys.HERO_SECONDARY_LINK, "secondary_link", "string"),
            (SettingKeys.HERO_BACKGROUND_IMAGE, "background_image", "string"),
            (SettingKeys.HERO_BACKGROUND_VIDEO, "background_video", "string"),
            (SettingKeys.HERO_CAROUSEL_IMAGES, "carousel_images", "json"),
            (SettingKeys.HERO_CAROUSEL_TRANSITION, "carousel_transition", "integer"),
        ]

        for setting_key, schema_attr, val_type in key_mappings:
            val = getattr(data, schema_attr)
            if val is not None:
                self._set_val(setting_key, val, val_type)

        return self.get_hero()
