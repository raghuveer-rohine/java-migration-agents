import os
from openai import OpenAI
import requests

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

def get_llm_response(prompt: str) -> str:
    if LLM_PROVIDER == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content

    elif LLM_PROVIDER == "ollama":
        response = requests.post(
            f"{os.getenv('OLLAMA_BASE_URL')}/api/generate",
            json={
                "model": os.getenv("OLLAMA_MODEL"),
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    else:
        raise ValueError("Unsupported LLM_PROVIDER")
