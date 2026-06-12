from fastapi import FastAPI
from pydantic import BaseModel
# from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
# import torch
import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# model_path = "./tinyllama-coding-model"
 
print("Loading model...")
 
# tokenizer = AutoTokenizer.from_pretrained(model_path)
# model = AutoModelForCausalLM.from_pretrained(model_path)
 
class Question(BaseModel):
    prompt: str
 
@app.post("/ask")
def ask_ai(data: Question):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional coding assistant. Give clear and correct coding answers."
                },
                {
                    "role": "user",
                    "content": data.prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 350
        }
    )

    result = response.json()
    return {
        "response": result["choices"][0]["message"]["content"]
    }
 