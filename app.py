from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

class Query(BaseModel):
    prompt: str

@app.post("/chat")
def chat(query: Query):
    payload = {"inputs": query.prompt}
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    except Exception as e:
        return {"error": f"Failed to connect to Hugging Face API: {str(e)}"}
    
    if response.status_code != 200:
        return {"error": f"Hugging Face API returned {response.status_code}", "raw": response.text}

    try:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return {"response": data[0]["generated_text"]}
        elif isinstance(data, dict) and "generated_text" in data:
            return {"response": data["generated_text"]}
        else:
            return {"error": "Unexpected response structure", "raw": data}
    except Exception as e:
        return {"error": f"Failed to parse response: {str(e)}", "raw": response.text}

@app.get("/")
def root():
    return {"message": "Ask me questions at POST /chat"}
