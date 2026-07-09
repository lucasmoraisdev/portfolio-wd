"""
Hierarquia centralizada de exceções da aplicação.

Todas as exceções devem herdar de BusinessException
para serem capturadas pelo handler global.
"""

class BusinessException(Exception):
    """Exceção base para todos os erros da aplicação."""

    def __init__(
        self,
        message: str = "Erro não identificado",
        status_code: int = 400,
        error_code: str = "BUSINESS_ERROR",
        details: dict | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

# ────────── Módulo Auth ────────────────────────────────────────────────────────────
class InvalidCredentialsException(BusinessException):
    """Credenciais inválidas (login)."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="INVALID_CREDENTIALS",
        )

class InvalidTokenException(BusinessException):
    """Token de acesso inválido ou malformado"""

    def __init__(self, message: str = "Token de autenticação inválido"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="TOKEN_INVALID",
        )

class ExpiredTokenException(BusinessException):
    """Token de acesso expirado."""

    def __init__(self, message: str = "Token de autenticação expirado."):
        super().__init__(
            message=message,
            status_code=401,
            error_code="TOKEN_EXPIRED",
        )

class PermissionDeniedException(BusinessException):
    """Usuário sem permissão para acessar o recurso."""

    def __init__(self, message: str = "Permissão negada"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="PERMISSION_DENIED",
        )
# ────────── Módulo User ────────────────────────────────────────────────────────────
class UserNotFoundException(BusinessException):
    """Usuário não encontrado"""

    def __init__(self, user_id: str | None = None, email: str | None = None):
        message = f"Usuário '{user_id}' não encontrado" if user_id else f"Usuário '{email}' não encontrado" if email else "Usuário não encontrado"
        super().__init__(
            message=message,
            status_code=404,
            error_code="USER_NOT_FOUND",
            details={"user_id": user_id} if user_id else {"email": email} if email else {},
        )

class UserAlreadyExistsException(BusinessException):
    """Tentativa de criar usuário com email/identificador já existente."""

    def __init__(self, field: str = "email", value: str | None = None):
        message = f"Usuário com {field} '{value}' já existe" if value else "Usuário já existe"
        super().__init__(
            message=message,
            status_code=409,
            error_code="USER_ALREADY_EXISTS",
            details={"field": field, "value": value} if value else {"field": field},
        )

class UserInactiveException(BusinessException):
    """Usuário está inativo/desativado."""

    def __init__(self, message: str = "Usuário inativo"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="USER_INACTIVE",
        )

class InvalidUserDataException(BusinessException):
    """Usuário inválido."""

    def __init__(self, message: str = "Usuário inválido"):
        super().__init__(
            message=message,
            status_code=400,
            error_code="USER_INVALID",
        )
# ────────── Módulo CMS ─────────────────────────────────────────────────────────────
# ────────── Módulo Contacts ────────────────────────────────────────────────────────
# ────────── Módulo Events ──────────────────────────────────────────────────────────
# ────────── Módulo FAQ ─────────────────────────────────────────────────────────────
# ────────── Módulo Team ────────────────────────────────────────────────────────────
# ────────── Módulo Testimonials ────────────────────────────────────────────────────
# ────────── Módulo Toys ────────────────────────────────────────────────────────────
# ────────── Módulo Settings ────────────────────────────────────────────────────────
# ────────── Módulo Uploads ─────────────────────────────────────────────────────────
class InvalidFileExtensionException(BusinessException):
    """Extensão de arquivo não permitida"""
    def __init__(self, extension: str, allowed: set[str] | None = None):
        allowed_list = ", ".join(sorted(allowed)) if allowed else ""
        message = (
            f"Extensão \".{extension}\" não permitida. Extensões aceitas: {allowed_list}"
        ) if allowed else f"Extensão \".{extension}\" não permitida."
        
        super().__init__(message=message,
            status_code=415,
            error_code="INVALID_FILE_EXTENSION",
            details={}
        )
class FileTooLargeException(BusinessException):
    """Arquivo excede o tamanho máximo permitido."""
    def __init__(self, size: int, max_size: int):
        size_mb = size / (1024 * 1024)
        max_mb = max_size / (1024 * 1024)
        super().__init__(
            message=(
                f"Arquivo muito grande({size_mb:.2f} MB)."
                f"Tamanho máximo permitido: {max_mb:.2f} MB."
            ),
            status_code=413,
            error_code="FILE_TOO_LARGE",
            details={}
        )
class FileNotFoundException(BusinessException):
    """Arquivo não encontrado no storage."""

    def __init__(self, filename: str | None = None):
        message = f"Arquivo \"{filename}\" não encontrado" if filename else "Arquivo não encontrado"
        super().__init__(
            message=message,
            status_code=404,
            error_code="FILE_NOT_FOUND",
            details={}
        )

class FileCorruptedException(BusinessException):
    """Arquivo corrompido ou tipo não corresponde à extensão."""

    def __init__(self, message: str = "Arquivo corrompido ou tipo inválido"):
        super().__init__(
            message=message,
            status_code=400,
            error_code="FILE_CORRUPTED",
            details={}
        )

class StorageException(BusinessException):
    """Erro ao acessar o storage"""

    def __init__(self, message: str = "Erro no storage"):
        super().__init__(
            message=message,
            status_code=400,
            error_code="STORAGE_ERROR",
            details={}
        )
# ────────── Exceções genéricas reutilizáveis ───────────────────────────────────────
class ResourceNotFoundException(BusinessException):
    """Recurso genérico não encontrado"""

    def __init__(self, resource: str = "recurso", resource_id: str | None = None):
        message = f"{resource} '{resource_id}' não encontrado" if resource_id else f"{resource} não encontrado"
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
            details={"resource": resource, "resource_id": resource_id} if resource_id else {"resource": resource},
        )


class ResourceAlreadyExistsException(BusinessException):
    """Recurso genérico já existe."""

    def __init__(self, resource: str = "recurso", field: str | None = None, value: str | None = None):
        message = f"{resource} já existe" + (f" com {field}='{value}'" if field and value else "")
        super().__init__(
            message=message,
            status_code=409,
            error_code="RESOURCE_ALREADY_EXISTS",
            details={"resource": resource, "field": field, "value": value} if field else {"resource": resource},
        )


class ValidationException(BusinessException):
    """Erro de validação de negócio (diferente do RequestValidationError do Pydantic)."""

    def __init__(self, message: str = "Dados inválidos", field: str | None = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details={"field": field} if field else {},
        )


class ConflictException(BusinessException):
    """Conflito de estado (ex: recurso em uso, não pode deletar)."""

    def __init__(self, message: str = "Conflito de estado"):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
            details={}
        )

class SettingsNotFoundException(BusinessException):
    """Configuração não encontrada"""
    
    def __init__(self, key: str | None = None):
        message = f"Configuração \"{key}\" não encontrada" if key else "Configuração não encontrada"
        super().__init__(
            message=message,
            status_code=404,
            error_code="SETTING_NOT_FOUND",
            details={}
        )

class InvalidSettingValueException(BusinessException):
    """Valor inválido para uma configuração."""

    def __init__(self, key: str, reason: str = ""):
        message = f"Valor inválido para \"{key}\"" + (f": {reason}" if reason else "")
        super().__init__(
            message=message,
            status_code=422,
            error_code="INVALID_SETTING_VALUE",
            details={}
        )


class SettingReadOnlyException(BusinessException):
    """Tentativa de alterar uma configuração somente leitura."""

    def __init__(self, key: str):
        super().__init__(
            message=f"Configuração \"{key}\" é somente leitura",
            status_code=403,
            error_code="SETTING_READ_ONLY",
            details={}
        )
