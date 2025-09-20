from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
def chat(prompt: Prompt):
    try:
        result = subprocess.run(
            ["ilab", "chat", "--prompt", prompt.prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return {"response": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr or str(e)}

@app.get("/")
def root():
    return {"message": "InstructLab API is running. Use POST /chat with { 'prompt': 'your question' }"}
