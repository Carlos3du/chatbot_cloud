# ---------------------------
# Dockerfile Estável (Single Stage / System Install)
# ---------------------------
# Usamos a imagem slim direta para garantir compatibilidade total
FROM python:3.12-slim

# Instalar o uv (gerenciador ultrarrápido)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Compilação para acelerar o startup
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Copiar arquivos de dependência
COPY pyproject.toml uv.lock* ./

# --- MUDANÇA PRINCIPAL ---
# Instalação direta no sistema (--system).
# Eliminamos a criação de .venv e a cópia entre estágios.
# Isso garante que o binário 'uvicorn' seja instalado em /usr/local/bin
# com as permissões corretas de execução nativas do Linux.
RUN uv pip install --system -r pyproject.toml

# Copiar o código da aplicação
COPY ./app ./app

COPY start.sh ./
RUN chmod +x start.sh

# Expõe a porta
EXPOSE 8000

# Comando de execução
# Como instalamos no sistema, o uvicorn estará no PATH global automaticamente.
CMD ["/bin/sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
