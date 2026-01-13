from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from .chunking import Chunk
from .config import settings

def save_index(index_dir: str, embeddings: np.ndarray, chunks: list[Chunk]) -> None:
    p = Path(index_dir)
    p.mkdir(parents=True, exist_ok=True)
    np.save(p / "embeddings.npy", embeddings)
    meta = [
        {
            "doc_id": c.doc_id,
            "title": c.title,
            "chunk_id": c.chunk_id,
            "text": c.text,
            "source_path": c.source_path,
        }
        for c in chunks
    ]
    (p / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def load_index(index_dir: str):
    p = Path(index_dir)
    emb_path = p / "embeddings.npy"
    meta_path = p / "meta.json"
    if not emb_path.exists() or not meta_path.exists():
        return None
    embeddings = np.load(emb_path)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return embeddings, meta

def cosine_top_k(query_vec: np.ndarray, embeddings: np.ndarray, k: int = 5):
    # normalize
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    E = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12)
    sims = E @ q
    idx = np.argsort(-sims)[:k]
    return idx.tolist(), sims[idx].tolist()
