import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()


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

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    return response.json()




import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    if GROQ_API_KEY:
        logger.info("✅ GROQ_API_KEY loaded successfully.")
    else:
        logger.error("❌ GROQ_API_KEY is missing! Check your environment variables.")
