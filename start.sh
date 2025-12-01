# Inicia o backend (FastAPI) em segundo plano (&)
# Ajuste a porta se necessário. O backend roda internamente no container.
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Inicia o frontend (Streamlit)
# O Streamlit precisa saber que está rodando sem monitor (headless) e no endereço 0.0.0.0
streamlit run frontend/main.py --server.port 8501 --server.address 0.0.0.0