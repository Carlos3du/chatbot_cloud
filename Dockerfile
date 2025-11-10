# Usando uma imagem Python oficial como base
FROM python:3.14-slim

# Instalar uv - gerenciador de pacotes Python ultrarrápido
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml ./

# Instalar dependências usando uv
RUN uv pip install --system -r pyproject.toml

# Copiar o código da aplicação
COPY ./app ./app

# Expor a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para rodar a aplicação
# Railway define a variável PORT automaticamente
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
