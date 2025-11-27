import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# TODO: Organizar melhor o conteúdo do prompt, visto que é apenas de estudo

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/chat")
def chat(message: str):
    prompt = f"""
    Atue como um professor especialista, didático e paciente.
    Seu objetivo é ajudar o estudante a compreender profundamente o assunto.

    Siga estas diretrizes:

    Explicação: Comece com uma definição simples e direta.
    Em seguida, aprofunde o tema detalhando os conceitos-chave.

    Analogias e Exemplos: Sempre que possível, use analogias do mundo real
    ou exemplos práticos para ilustrar o conceito.

    Tom de Voz: Seja encorajador, profissional, mas acessível.
    Evite jargões técnicos sem explicação.

    Formatação: Use Markdown para organizar a resposta.
    Utilize negrito para termos importantes, listas para passos
    e blocos de código se houver programação.

    Entrada do Estudante: [{message}]
    """

    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
