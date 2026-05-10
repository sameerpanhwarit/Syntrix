import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_llm(prompt: str):
    models = [
        os.getenv("MODEL_PRIMARY"),
        os.getenv("MODEL_FALLBACK"),
        "qwen/qwen-7b-chat"
    ]

    for model in models:
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=20
            )

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception:
            continue

    return "All AI models failed."