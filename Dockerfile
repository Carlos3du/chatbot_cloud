# ---------------------------
# Estágio 1: Builder (Compilação e Dependências)
# ---------------------------
# Usamos uma versão slim estável (ajuste para 3.14 se realmente tiver acesso à imagem)
FROM python:3.12-slim AS builder

# Instalar o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Configurações do uv para otimização
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copiar apenas arquivos de dependência para aproveitar o cache do Docker
# O asterisco em uv.lock* permite que o comando funcione mesmo se você não tiver o lock file ainda
COPY pyproject.toml uv.lock* ./

# Criar ambiente virtual e instalar dependências
# Usamos o próprio venv para isolar as libs, facilitando a cópia para o próximo estágio
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

# Criar um usuário não-root por segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar o ambiente virtual do estágio builder
COPY --from=builder /app/.venv /app/.venv

# Copiar o código da aplicação
COPY ./app ./app

# Ajustar permissões (opcional, mas boa prática se a app precisar escrever algo)
RUN chown -R appuser:appuser /app

# Mudar para o usuário seguro
USER appuser

# Expõe a porta (documentação apenas)
EXPOSE 8000

# Comando de execução
# Usamos shell form (/bin/sh -c) para garantir que a variável ${PORT} seja expandida corretamente
# Se a variável PORT não estiver definida, usa 8000 como fallback
CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]