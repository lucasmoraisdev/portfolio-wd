import re
from app.core.config import settings

def resolve_upload_url(value: str | None) -> str | None:
    """
    Recebe um valor de configuração (URL absoluta antiga, caminho ou UUID puro)
    e reconstrói a URL pública apontando dinamicamente para o base_url configurado
    no ambiente atual da aplicação.
    """
    if not value or not isinstance(value, str):
        return None
    
    # Procura por um padrão UUIDv4
    match = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', value, re.IGNORECASE)
    if match:
        uuid = match.group(0)
        return f"{settings.app.base_url}{settings.app.api_prefix}/uploads/{uuid}/file"
    
    return value
