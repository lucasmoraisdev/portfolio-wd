FROM python:3.13-slim

# Instalar uv para gerenciar dependências rapidamente respeitando o uv.lock
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Instalar dependências necessárias para compilar pacotes se necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instalar dependências no ambiente global do container
RUN uv pip install --system --no-cache -r pyproject.toml

# Copiar os arquivos do projeto
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
COPY README.md ./

# Expor a porta que a API do FastAPI escuta
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Script de inicialização ou comando direto.
# Executa as migrações automáticas do Alembic antes de iniciar o servidor FastAPI.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
