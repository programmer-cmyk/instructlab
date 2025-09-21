from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")  # We’ll set this in Render
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

class Query(BaseModel):
    prompt: str

@app.post("/chat")
def chat(query: Query):
    payload = {"inputs": query.prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    try:
        data = response.json()
        return {"response": data[0]["generated_text"]}
    except Exception as e:
        return {"error": str(e), "raw": response.text}

@app.get("/")
def root():
    return {"message": "Ask me questions at POST /chat"}
