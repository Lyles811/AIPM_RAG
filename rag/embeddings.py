from __future__ import annotations
import numpy as np
from .llm import make_client
from .config import settings

def embed_texts(texts: list[str], api_key: str | None = None, model: str | None = None) -> np.ndarray:
    """Return embeddings as shape (n, d) float32 array."""
    client = make_client(api_key=api_key)
    resp = client.embeddings.create(
        model=model or settings.embed_model,
        input=texts,
    )
    vecs = [d.embedding for d in resp.data]
    return np.array(vecs, dtype=np.float32)

def embed_query(text: str, api_key: str | None = None, model: str | None = None) -> np.ndarray:
    return embed_texts([text], api_key=api_key, model=model)[0]
