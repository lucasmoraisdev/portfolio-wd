# Arquitetura

## Objetivo

Separar responsabilidades utilizando arquitetura em camadas.

Frontend

↓

REST API

↓

FastAPI

↓

Services

↓

Repositories

↓

PostgreSQL

---

## Backend

- API
- Services
- Repository
- Models
- Schemas

---

## Frontend

- App Router
- Components
- Hooks
- Services
- Providers

---

## Infraestrutura

NGINX

↓

Next.js

↓

FastAPI

↓

PostgreSQL

## Login
email
senha

↓

JWT

## Logout
POST /auth/logout

↓

204 No Content

## Esqueci senha
POST /auth/forgot-password

{
    "email": "user@email.com"
}

↓

gera token

↓

salva hash do token

↓

define expiração

↓

envia e-mail

## Resetar senha
POST /auth/reset-password

{
    "token": "...",
    "password": "NovaSenha123!"
}

↓

valida token

↓

altera senha

↓

invalida token

↓

200 OK