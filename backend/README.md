# Resposta padrão para API

{
    "success": true,
    "message": "Toy created successfully.",
    "data": {}
}

# Resposta de erro padrão para API

{
    "success": false,
    "message": "Validation error.",
    "errors": []
}

# Resposta padrão paginada para API

{
    "success": true,
    "data": [],
    "pagination": {
        "page": 1,
        "size": 20,
        "total": 135
    }
}

# Exceções

NotFoundException

UnauthorizedException

ValidationException

ConflictException

ForbiddenException

StorageException

# Logs

INFO

Application started

version=1.0.0

environment=development

# Logs de erro

ERROR

Database connection failed

host=...

user=...

stacktrace...

# Estrutura de pastas
backend/
│
├── app/
│
├── core/
│   ├── config.py
│   ├── lifespan.py
│   └── logging.py
│
├── shared/
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── mixins.py
│   │   └── __init__.py
│   │
│   ├── security/
│   │   ├── jwt.py
│   │   ├── password.py
│   │   ├── permissions.py
│   │   └── dependencies.py
│   │
│   ├── exceptions/
│   ├── middleware/
│   ├── pagination/
│   ├── responses/
│   ├── storage/
│   └── utils/
│
├── modules/
│   ├── auth/
│   ├── cms/
│   ├── toys/
│   ├── events/
│   ├── faq/
│   ├── team/
│   ├── testimonials/
│   ├── contacts/
│   └── settings/
│
└── main.py