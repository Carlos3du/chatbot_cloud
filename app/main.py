from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


app = FastAPI()
app.get("/")
def root():
    return {"status": "running"}

@app.post("/chat")
def chat(message: str):
    try:
        response = model.generate_content(message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))