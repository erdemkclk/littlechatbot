import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests

app = FastAPI()

# Mount static files
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

# Serve index.html for root and fallback
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/{path:path}")
async def serve_catch_all(path: str):
    return FileResponse("static/index.html")

# Your chat endpoint
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "messages": [{"role": "user", "content": user_message}],
        "model": "llama3-8b-8192",
        "temperature": 0.7,
        "max_tokens": 200,
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    return response.json()
