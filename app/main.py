import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

#TODO: Organizar melhor o conteúdo do prompt, visto que é apenas de estudo
#TODO: Adaptar o workflow para utilizar uma imagem docker em cada branch

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/chat")
def chat(message: str):
    try:
        response = model.generate_content(message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
