import os

import requests
import streamlit as st
from dotenv import load_dotenv


def limpar_input():
    st.session_state["input_message"] = ""


load_dotenv()
API_url = os.getenv("API_url")

st.set_page_config(page_title="📚 IsCool GPT")


with st.container(key="header"):
    st.title("📚 IsCool GPT")


with st.container(key="user_input"):
    message = st.text_area(
        key="input_message",
        label="input",
        label_visibility="hidden",
        placeholder="Digite sua dúvida aqui...",
    )


with st.container(key="buttons", horizontal_alignment="right", horizontal=True):
    if st.button("Limpar", type="secondary", on_click=limpar_input):
        st.rerun()

    enviar = st.button("Enviar", type="primary")


with st.container(key="chat_output"):
    if enviar:
        if message.strip():
            try:
                with st.spinner("Enviando..."):
                    response = requests.post(
                        API_url, params={"message": message}, timeout=30
                    )

                    if response.status_code == 200:
                        output = response.json()

                        st.markdown("###💡 Resposta")
                        st.write(output["response"])
                    else:
                        st.error(f"Falha ao processar mensagem: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro de conexão: {str(e)}")
        else:
            st.warning("Por favor, digite uma mensagem")
