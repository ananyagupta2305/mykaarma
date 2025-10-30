import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(prompt, system_prompt=None, temperature=0.5):
    """
    Calls Groq API with system + user prompt
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 8000,
    }

    try:
        res = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq API Error:", e)
        return "Sorry, I'm unable to process your request right now."
