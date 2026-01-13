from __future__ import annotations
from dataclasses import dataclass
from .config import settings
from .embeddings import embed_query
from .index import load_index, cosine_top_k
from .llm import chat_complete
from .prompts import SYSTEM_PROMPT, build_user_prompt

@dataclass
class RetrievedChunk:
    chunk_id: str
    title: str
    text: str
    source_path: str
    score: float

class RAGPipeline:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def answer(self, question: str, top_k: int | None = None, temperature: float | None = None):
        idx_data = load_index(settings.index_dir)
        if idx_data is None:
            raise RuntimeError(
                "Index not found. Please run `python ingest.py` first (or use the app sidebar to build index)."
            )
        embeddings, meta = idx_data
        q_vec = embed_query(question, api_key=self.api_key)
        k = top_k or settings.top_k
        idxs, scores = cosine_top_k(q_vec, embeddings, k=k)
        contexts = []
        retrieved = []
        for i, s in zip(idxs, scores):
            m = meta[i]
            contexts.append({"chunk_id": m["chunk_id"], "title": m["title"], "text": m["text"]})
            retrieved.append(
                RetrievedChunk(
                    chunk_id=m["chunk_id"],
                    title=m["title"],
                    text=m["text"],
                    source_path=m.get("source_path", ""),
                    score=float(s),
                )
            )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, contexts)},
        ]
        answer_md = chat_complete(messages, api_key=self.api_key, temperature=temperature)
        return answer_md, retrieved
