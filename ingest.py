from __future__ import annotations
import os
from tqdm import tqdm
from rag.config import settings
from rag.chunking import load_kb_chunks
from rag.embeddings import embed_texts
from rag.index import save_index

def main():
    print("== Build index ==")
    print(f"KB_DIR: {settings.kb_dir}")
    print(f"INDEX_DIR: {settings.index_dir}")
    if not settings.api_key:
        raise RuntimeError("Missing SILICONFLOW_API_KEY in .env")

    chunks = load_kb_chunks(settings.kb_dir, settings.chunk_size, settings.chunk_overlap)
    print(f"Loaded {len(chunks)} chunks.")

    batch_size = 32
    embeddings = []
    texts = [c.text for c in chunks]
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i+batch_size]
        vecs = embed_texts(batch)
        embeddings.append(vecs)
    import numpy as np
    emb = np.vstack(embeddings)
    save_index(settings.index_dir, emb, chunks)
    print("Index saved.")
    print("Done.")

if __name__ == "__main__":
    main()
