from __future__ import annotations
from openai import OpenAI
from .config import settings

def make_client(api_key: str | None = None, base_url: str | None = None) -> OpenAI:
    key = api_key or settings.api_key
    if not key:
        raise RuntimeError("Missing API key. Set SILICONFLOW_API_KEY in .env or provide it in UI.")
    return OpenAI(api_key=key, base_url=base_url or settings.base_url)

def chat_complete(messages, api_key: str | None = None, temperature: float | None = None, model: str | None = None):
    client = make_client(api_key=api_key)
    resp = client.chat.completions.create(
        model=model or settings.chat_model,
        messages=messages,
        temperature=settings.temperature if temperature is None else temperature,
    )
    return resp.choices[0].message.content
