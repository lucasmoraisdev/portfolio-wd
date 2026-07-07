SETTINGS_PREFIX="/settings"
SETTINGS_TAG="Settings"

DEFAULT_SECTIONS=[
    "hero",
    "about",
    "toys",
    "categories",
    "team",
    "events",
    "municipalities",
    "clients",
    "testimonials",
    "faq",
    "contact",
    "map",
    "footer"
]

DEFAULT_THEME_COLORS = {
    "primary": "#3B82F6",
    "secondary": "#10B981",
    "accent": "#F59E0B",
    "background": "#FFFFFF",
    "text": "#1F2937",
    "button": "#3B82F6"
}

DEFAULT_TYPOGRAPHY = {
    "font_family": "Inter, sans-serif",
    "font_weight": "400",
    "base_size": "16px"
}

DEFAULT_LAYOUT = {
    "max_content_width": "1280px",
    "border_radius": "8px",
    "shadows": True,
    "spacing": "medium",
}

DEFAULT_FORMATS = {
    "language": "pt-BR",
    "timezone": "America/Sao_Paulo",
    "date_format": "DD/MM/YYYY",
    "phone_format": "(##) #####-####",
}

class SettingKeys:
    # Empresa
    COMPANY_NAME = "company_name"
    COMPANY_TRADING_NAME = "company_trading_name"
    COMPANY_SLOGAN = "company_slogan"
    COMPANY_SHORT_DESCRIPTION = "company_short_description"
    COMPANY_FULL_DESCRIPTION = "company_full_description"
    COMPANY_CNPJ = "company_cnpj"
    COMPANY_FOUNDING_YEAR = "company_founding_year"

    # Hero
    HERO_TITLE = "hero_title"
    HERO_SUBTITLE = "hero_subtitle"
    HERO_TEXT = "hero_text"
    HERO_PRIMARY_BUTTON = "hero_primary_button"
    HERO_PRIMARY_LINK = "hero_primary_link"
    HERO_SECONDARY_BUTTON = "hero_secondary_button"
    HERO_SECONDARY_LINK = "hero_secondary_link"
    HERO_BACKGROUND_IMAGE = "hero_background_image"
    HERO_BACKGROUND_VIDEO = "hero_background_video"
    HERO_CAROUSEL_IMAGES = "hero_carousel_images"
    HERO_CAROUSEL_TRANSITION = "hero_carousel_transition"

    # Contato
    CONTACT_PHONE_PRIMARY = "contact_phone_primary"
    CONTACT_PHONE_SECONDARY = "contact_phone_secondary"
    CONTACT_WHATSAPP = "contact_whatsapp"
    CONTACT_EMAIL_COMMERCIAL = "contact_email_commercial"
    CONTACT_EMAIL_FINANCIAL = "contact_email_financial"
    CONTACT_BUSINESS_HOURS = "contact_business_hours"

    # Endereço
    ADDRESS_ZIP = "address_zip"
    ADDRESS_STREET = "address_street"
    ADDRESS_NUMBER = "address_number"
    ADDRESS_COMPLEMENT = "address_complement"
    ADDRESS_NEIGHBORHOOD = "address_neighborhood"
    ADDRESS_CITY = "address_city"
    ADDRESS_STATE = "address_state"
    ADDRESS_COUNTRY = "address_country"
    ADDRESS_LATITUDE = "address_latitude"
    ADDRESS_LONGITUDE = "address_longitude"

    # Redes Sociais
    SOCIAL_INSTAGRAM = "social_instagram"
    SOCIAL_FACEBOOK = "social_facebook"
    SOCIAL_TIKTOK = "social_tiktok"
    SOCIAL_YOUTUBE = "social_youtube"
    SOCIAL_LINKEDIN = "social_linkedin"
    SOCIAL_X = "social_x"
    SOCIAL_PINTEREST = "social_pinterest"

    # SEO
    SEO_TITLE = "seo_title"
    SEO_DESCRIPTION = "seo_description"
    SEO_KEYWORDS = "seo_keywords"
    SEO_CANONICAL = "seo_canonical"
    SEO_ROBOTS = "seo_robots"
    SEO_AUTHOR = "seo_author"
    SEO_THEME_COLOR = "seo_theme_color"
    SEO_OG_TITLE = "seo_og_title"
    SEO_OG_DESCRIPTION = "seo_og_description"
    SEO_OG_IMAGE = "seo_og_image"
    SEO_TWITTER_CARD = "seo_twitter_card"

    # Analytics
    ANALYTICS_GA = "analytics_ga"
    ANALYTICS_GTM = "analytics_gtm"
    ANALYTICS_META_PIXEL = "analytics_meta_pixel"
    ANALYTICS_GSC = "analytics_gsc"

    # Tema
    THEME_PRIMARY_COLOR = "theme_primary_color"
    THEME_SECONDARY_COLOR = "theme_secondary_color"
    THEME_ACCENT_COLOR = "theme_accent_color"
    THEME_BACKGROUND_COLOR = "theme_background_color"
    THEME_TEXT_COLOR = "theme_text_color"
    THEME_BUTTON_COLOR = "theme_button_color"

    # Tipografia
    TYPO_FONT_FAMILY = "typo_font_family"
    TYPO_FONT_WEIGHT = "typo_font_weight"
    TYPO_BASE_SIZE = "typo_base_size"

    # Layout
    LAYOUT_MAX_WIDTH = "layout_max_width"
    LAYOUT_BORDER_RADIUS = "layout_border_radius"
    LAYOUT_SHADOWS = "layout_shadows"
    LAYOUT_SPACING = "layout_spacing"

    # Seções
    SECTIONS_ORDER = "sections_order"
    SECTIONS_ENABLED = "sections_enabled"

    # Rodapé
    FOOTER_INSTITUTIONAL = "footer_institutional"
    FOOTER_COPYRIGHT = "footer_copyright"
    FOOTER_DEVELOPED_BY = "footer_developed_by"
    FOOTER_QUICK_LINKS = "footer_quick_links"

    # Geral
    GENERAL_LANGUAGE = "general_language"
    GENERAL_TIMEZONE = "general_timezone"
    GENERAL_DATE_FORMAT = "general_date_format"
    GENERAL_PHONE_FORMAT = "general_phone_format"

    # Uploads (referências)
    UPLOAD_LOGO_MAIN = "upload_logo_main"
    UPLOAD_LOGO_WHITE = "upload_logo_white"
    UPLOAD_LOGO_SMALL = "upload_logo_small"
    UPLOAD_FAVICON = "upload_favicon"
    UPLOAD_APPLE_TOUCH = "upload_apple_touch"
    UPLOAD_OG_IMAGE = "upload_og_image"
    UPLOAD_SHARE_BANNER = "upload_share_banner"