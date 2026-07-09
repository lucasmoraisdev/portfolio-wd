import logging
from typing import Any
from uuid import UUID

from fastapi import UploadFile

from .constants import SettingKeys
from app.shared.exceptions import (
    SettingNotFoundException
)
from .repository import SettingRepository
from .schemas import (
    SettingPublicResponse,
    SettingAdminResponse,
    SettingResponse,
    UploadReferences
)
from app.modules.upload.service import UploadService
from app.modules.upload.repository import UploadRepository
from app.shared.database import get_db

logger = logging.getLogger(__name__)

class SettingsService:
    """
    Service para configurações globais

    Responsável por:
    - Mapera key-value store para objetos estruturados
    - Gerenciar uploads relacionados (logs, favicon, etc)
    - Cachear configurações frequentes
    """

    def __init__(
        self,
        repository: SettingRepository,
        upload_service: UploadService | None = None,
    ) -> None:
        self._repository = repository
        self._upload_service = upload_service

# Helpers

    def _get_value(self, key: str, default: Any = None) -> Any:
        setting = self._repository.get_by_key(key)
        return setting.value if setting and setting.value is not None else default
    
    def _set_value(
        self,
        key: str,
        value: Any,
        type_: str = "string",
        is_public: bool = False
    ) -> SettingResponse:
        """Define um valor e retorna o schema de resposta"""
        model = self._repository.create_or_update(key, value, type_, is_public)
        return SettingResponse.model_validate(model)
    
    def get_public_settings(self) -> SettingPublicResponse:
        return SettingPublicResponse(
            company=self._build_company(),
            hero=self._build_hero(),
            contact=self._build_contact(),
            address=self._build_address(),
            social=self._build_social(),
            seo=self._build_seo(),
            theme=self._build_theme(),
            typography=self._build_typography(),
            layout=self._build_layout(),
            sections=self._build_sections(),
            footer=self._build_footer(),
            general=self._build_general(),
            uploads=self._build_uploads()
        )

    def get_admin_settings(self) -> SettingAdminResponse:
        return SettingAdminResponse(
            company=self._build_company(),
            hero=self._build_hero(),
            contact=self._build_contact(),
            address=self._build_address(),
            social=self._build_social(),
            seo=self._build_seo(),
            analytics=self._build_analytics(),
            theme=self._build_theme(),
            typography=self._build_typography(),
            layout=self._build_layout(),
            sections=self._build_sections(),
            footer=self._build_footer(),
            general=self._build_general(),
            uploads=self._build_uploads()
        )
    
    def _build_company(self) -> dict[str, Any]:
        return {
            "name": self._get_value(SettingKeys.COMPANY_NAME),
            "trading_name": self._get_value(SettingKeys.COMPANY_TRADING_NAME),
            "slogan": self._get_value(SettingKeys.COMPANY_SLOGAN),
            "short_description": self._get_value(SettingKeys.COMPANY_SHORT_DESCRIPTION),
            "full_description": self._get_value(SettingKeys.COMPANY_FULL_DESCRIPTION),
            "cnp": self._get_value(SettingKeys.COMPANY_CNPJ),
            "founding_year": self._get_value(SettingKeys.COMPANY_FOUNDING_YEAR),
        }

    def _build_hero(self) -> dict[str, Any]:
        return {
            "title": self._get_value(SettingKeys.HERO_TITLE),
            "subtitle": self._get_value(SettingKeys.HERO_SUBTITLE),
            "text": self._get_value(SettingKeys.HERO_TEXT),
            "primary_button": self._get_value(SettingKeys.HERO_PRIMARY_BUTTON),
            "primary_link": self._get_value(SettingKeys.HERO_PRIMARY_LINK),
            "secondary_button": self._get_value(SettingKeys.HERO_SECONDARY_BUTTON),
            "secondary_link": self._get_value(SettingKeys.HERO_SECONDARY_LINK),
            "background_image": self._get_value(SettingKeys.HERO_BACKGROUND_IMAGE),
            "background_video": self._get_value(SettingKeys.HERO_BACKGROUND_VIDEO),
            "carousel_images": self._get_value(SettingKeys.HERO_CAROUSEL_IMAGES, []),
            "carousel_transition": self._get_value(SettingKeys.HERO_CAROUSEL_TRANSITION, 5),
        }
    
    def _build_contact(self) -> dict[str, Any]:
        return {
            "phone_primary": self._get_value(SettingKeys.CONTACT_PHONE_PRIMARY),
            "phone_secondary": self._get_value(SettingKeys.CONTACT_PHONE_SECONDARY),
            "whatsapp": self._get_value(SettingKeys.CONTACT_WHATSAPP),
            "email_commercial": self._get_value(SettingKeys.CONTACT_EMAIL_COMMERCIAL),
            "email_financial": self._get_value(SettingKeys.CONTACT_EMAIL_FINANCIAL),
            "business_hours": self._get_value(SettingKeys.CONTACT_BUSINESS_HOURS),
        }
    
    def _build_address(self) -> dict[str, Any]:
        return {
            "zip": self._get_value(SettingKeys.ADDRESS_ZIP),
            "street": self._get_value(SettingKeys.ADDRESS_STREET),
            "number": self._get_value(SettingKeys.ADDRESS_NUMBER),
            "complement": self._get_value(SettingKeys.ADDRESS_COMPLEMENT),
            "neighborhood": self._get_value(SettingKeys.ADDRESS_NEIGHBORHOOD),
            "city": self._get_value(SettingKeys.ADDRESS_CITY),
            "state": self._get_value(SettingKeys.ADDRESS_STATE),
            "country": self._get_value(SettingKeys.ADDRESS_COUNTRY, "Brasil"),
            "latitude": self._get_value(SettingKeys.ADDRESS_LATITUDE),
            "longitude": self._get_value(SettingKeys.ADDRESS_LONGITUDE),
        }
    
    def _build_social(self) -> dict[str, Any]:
        return {
            "instagram": self._get_value(SettingKeys.SOCIAL_INSTAGRAM),
            "facebook": self._get_value(SettingKeys.SOCIAL_FACEBOOK),
            "tiktok": self._get_value(SettingKeys.SOCIAL_TIKTOK),
            "youtube": self._get_value(SettingKeys.SOCIAL_YOUTUBE),
            "linkedin": self._get_value(SettingKeys.SOCIAL_LINKEDIN),
            "x": self._get_value(SettingKeys.SOCIAL_X),
            "pinterest": self._get_value(SettingKeys.SOCIAL_PINTEREST),
        }
    
    def _build_seo(self) -> dict[str, Any]:
        return {
            "title": self._get_value(SettingKeys.SEO_TITLE),
            "description": self._get_value(SettingKeys.SEO_DESCRIPTION),
            "keywords": self._get_value(SettingKeys.SEO_KEYWORDS),
            "canonical": self._get_value(SettingKeys.SEO_CANONICAL),
            "robots": self._get_value(SettingKeys.SEO_ROBOTS),
            "author": self._get_value(SettingKeys.SEO_AUTHOR),
            "theme_color": self._get_value(SettingKeys.SEO_THEME_COLOR),
            "og_title": self._get_value(SettingKeys.SEO_OG_TITLE),
            "og_description": self._get_value(SettingKeys.SEO_OG_DESCRIPTION),
            "og_image": self._get_value(SettingKeys.SEO_OG_IMAGE),
            "twitter_card": self._get_value(SettingKeys.SEO_TWITTER_CARD, "summary_large_image"),
        }
    
    def _build_analytics(self) -> dict[str, Any]:
        return {
            "google_analytics": self._get_value(SettingKeys.ANALYTICS_GA),
            "google_tag_manager": self._get_value(SettingKeys.ANALYTICS_GTM),
            "meta_pixel": self._get_value(SettingKeys.ANALYTICS_META_PIXEL),
            "google_search_console": self._get_value(SettingKeys.ANALYTICS_GSC),
        }
    
    def _build_theme(self) -> dict[str, Any]:
        return {
            "primary": self._get_value(SettingKeys.THEME_PRIMARY_COLOR, "#3B82F6"),
            "secondary": self._get_value(SettingKeys.THEME_SECONDARY_COLOR, "#10B981"),
            "accent": self._get_value(SettingKeys.THEME_ACCENT_COLOR, "#F59E0B"),
            "background": self._get_value(SettingKeys.THEME_BACKGROUND_COLOR, "#FFFFFF"),
            "text": self._get_value(SettingKeys.THEME_TEXT_COLOR, "#1F2937"),
            "button": self._get_value(SettingKeys.THEME_BUTTON_COLOR, "#3B82F6"),
        }
    
    def _build_typography(self) -> dict[str, Any]:
        return {
            "font_family": self._get_value(SettingKeys.TYPO_FONT_FAMILY, "Inter, sans-serif"),
            "font_weight": self._get_value(SettingKeys.TYPO_FONT_WEIGHT, "400"),
            "base_size": self._get_value(SettingKeys.TYPO_BASE_SIZE, "16px"),
        }
    
    def _build_layout(self) -> dict[str, Any]:
        return {
            "max_content_width": self._get_value(SettingKeys.LAYOUT_MAX_WIDTH, "1280px"),
            "border_radius": self._get_value(SettingKeys.LAYOUT_BORDER_RADIUS, "8px"),
            "shadows": self._get_value(SettingKeys.LAYOUT_SHADOWS, True),
            "spacing": self._get_value(SettingKeys.LAYOUT_SPACING, "medium"),
        }
    
    def _build_sections(self) -> dict[str, Any]:
        default = {
            "hero": {"enabled": True, "order": 1},
            "about": {"enabled": True, "order": 2},
            "toys": {"enabled": True, "order": 3},
            "categories": {"enabled": True, "order": 4},
            "team": {"enabled": True, "order": 5},
            "events": {"enabled": True, "order": 6},
            "municipalities": {"enabled": True, "order": 7},
            "clients": {"enabled": True, "order": 8},
            "testimonials": {"enabled": True, "order": 9},
            "faq": {"enabled": True, "order": 10},
            "contact": {"enabled": True, "order": 11},
            "map": {"enabled": True, "order": 12},
            "footer": {"enabled": True, "order": 13},
        }
        stored = self._get_value(SettingKeys.SECTIONS_ENABLED, {})
        if stored:
            default.update(stored)
        return default

    def _build_footer(self) -> dict[str, Any]:
        return {
            "institutional": self._get_value(SettingKeys.FOOTER_INSTITUTIONAL),
            "copyright": self._get_value(SettingKeys.FOOTER_COPYRIGHT),
            "developed_by": self._get_value(SettingKeys.FOOTER_DEVELOPED_BY),
            "quick_links": self._get_value(SettingKeys.FOOTER_QUICK_LINKS, []),
        }

    def _build_general(self) -> dict[str, Any]:
        return {
            "language": self._get_value(SettingKeys.GENERAL_LANGUAGE, "pt-BR"),
            "timezone": self._get_value(SettingKeys.GENERAL_TIMEZONE, "America/Sao_Paulo"),
            "date_format": self._get_value(SettingKeys.GENERAL_DATE_FORMAT, "DD/MM/YYYY"),
            "phone_format": self._get_value(SettingKeys.GENERAL_PHONE_FORMAT),
        }

    def _build_uploads(self) -> dict[str, str | None]:
        """Busca URLs públicas dos uploads referenciados."""
        refs = {
            "logo_main": self._get_value(SettingKeys.UPLOAD_LOGO_MAIN),
            "logo_white": self._get_value(SettingKeys.UPLOAD_LOGO_WHITE),
            "logo_small": self._get_value(SettingKeys.UPLOAD_LOGO_SMALL),
            "favicon": self._get_value(SettingKeys.UPLOAD_FAVICON),
            "apple_touch": self._get_value(SettingKeys.UPLOAD_APPLE_TOUCH),
            "og_image": self._get_value(SettingKeys.UPLOAD_OG_IMAGE),
            "share_banner": self._get_value(SettingKeys.UPLOAD_SHARE_BANNER),
        }

        # Resolve IDs de upload para URLs públicas
        # Se o valor for um UUID, busca a URL do upload
        resolved = {}
        for key, value in refs.items():
            if value and isinstance(value, str):
                # Aqui poderia buscar no upload_service se for UUID
                resolved[key] = value
            else:
                resolved[key] = None

        return resolved

    # ─── Operações CRUD ───────────────────────────────────────────

    def update_settings(self, settings: dict[str, Any]) -> list[SettingResponse]:
        """Atualiza múltiplas configurações de uma vez."""
        models = self.repository.bulk_update(settings)
        return [SettingResponse.model_validate(m) for m in models]

    def update_single(self, key: str, value: Any) -> SettingResponse:
        """Atualiza uma configuração individual."""
        type_ = self.repository._infer_type(value)
        is_public = key.startswith((
            "company_", "hero_", "contact_", "social_",
            "seo_", "theme_", "footer_", "upload_",
        ))
        model = self.repository.create_or_update(key, value, type_, is_public)
        return SettingResponse.model_validate(model)

    # ─── Uploads relacionados ─────────────────────────────────────

    async def upload_logo(
        self,
        file: UploadFile,
        logo_type: str = "main",
    ) -> SettingResponse:
        """Faz upload de um logo e atualiza a referência."""
        if not self.upload_service:
            raise RuntimeError("UploadService não configurado")

        upload = await self.upload_service.upload(file, file_type="logos")

        key_map = {
            "main": SettingKeys.UPLOAD_LOGO_MAIN,
            "white": SettingKeys.UPLOAD_LOGO_WHITE,
            "small": SettingKeys.UPLOAD_LOGO_SMALL,
        }
        key = key_map.get(logo_type, SettingKeys.UPLOAD_LOGO_MAIN)

        return self._set_value(key, upload.public_url, "string", is_public=True)

    async def upload_favicon(self, file: UploadFile) -> SettingResponse:
        """Faz upload do favicon."""
        if not self.upload_service:
            raise RuntimeError("UploadService não configurado")

        upload = await self.upload_service.upload(file, file_type="favicons")
        return self._set_value(
            SettingKeys.UPLOAD_FAVICON,
            upload.public_url,
            "string",
            is_public=True,
        )

    async def upload_banner(self, file: UploadFile) -> SettingResponse:
        """Faz upload de um banner (hero background ou share)."""
        if not self.upload_service:
            raise RuntimeError("UploadService não configurado")

        upload = await self.upload_service.upload(file, file_type="banners")

        # Adiciona à lista de banners do hero
        banners = self._get_value(SettingKeys.HERO_CAROUSEL_IMAGES, [])
        if isinstance(banners, list):
            banners.append(upload.public_url)
            self._set_value(SettingKeys.HERO_CAROUSEL_IMAGES, banners, "json", is_public=True)

        return SettingResponse.model_validate(
            self.repository.get_by_key(SettingKeys.HERO_CAROUSEL_IMAGES)
        )

    async def delete_banner(self, banner_url: str) -> bool:
        """Remove um banner da lista do hero."""
        banners = self._get_value(SettingKeys.HERO_CAROUSEL_IMAGES, [])
        if isinstance(banners, list) and banner_url in banners:
            banners.remove(banner_url)
            self._set_value(SettingKeys.HERO_CAROUSEL_IMAGES, banners, "json", is_public=True)
            return True
        return False