# ---------------------------
# Estágio 1: Builder (Compilação e Dependências)
# ---------------------------
# Usamos uma versão slim estável
FROM python:3.12-slim AS builder

# Instalar o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Configurações do uv para otimização
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copiar apenas arquivos de dependência para aproveitar o cache do Docker
COPY pyproject.toml uv.lock* ./

# Criar ambiente virtual e instalar dependências
RUN uv venv /app/.venv && \
    . /app/.venv/bin/activate && \
    uv pip install -r pyproject.toml

# ---------------------------
# Estágio 2: Runtime (Imagem Final Leve)
# ---------------------------
FROM python:3.12-slim

# Variáveis de ambiente para produção
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Adiciona o venv ao PATH para que o python/uvicorn seja encontrado automaticamente
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# REMOVIDO: Criação de usuário appuser e ajustes de permissão complexos.
# Rodaremos como ROOT para garantir acesso total aos arquivos e evitar "Permission denied".

# Copiar o ambiente virtual do estágio builder
COPY --from=builder /app/.venv /app/.venv

# Copiar o código da aplicação
COPY ./app ./app

# Expõe a porta
EXPOSE 8000

# Comando de execução
CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]