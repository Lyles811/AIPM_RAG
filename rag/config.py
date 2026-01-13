from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# def _env(name: str, default: str | None = None) -> str | None:
#     v = os.getenv(name)
#     return v if v is not None and v != "" else default
def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is not None and v != "":
        return v

    # Streamlit Cloud: read from st.secrets if available
    try:
        import streamlit as st
        if name in st.secrets:
            sv = st.secrets[name]
            if sv is not None and str(sv) != "":
                return str(sv)
    except Exception:
        pass

    return default


@dataclass(frozen=True)
class Settings:
    # SiliconFlow (OpenAI-compatible)
    api_key: str | None = _env("SILICONFLOW_API_KEY")
    base_url: str = _env("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")  # can override
    chat_model: str = _env("SILICONFLOW_CHAT_MODEL", "Qwen/Qwen2.5-72B-Instruct")
    embed_model: str = _env("SILICONFLOW_EMBED_MODEL", "BAAI/bge-m3")

    # RAG defaults
    top_k: int = int(_env("TOP_K", "5") or 5)
    chunk_size: int = int(_env("CHUNK_SIZE", "900") or 900)
    chunk_overlap: int = int(_env("CHUNK_OVERLAP", "120") or 120)
    max_context_chunks: int = int(_env("MAX_CONTEXT_CHUNKS", "6") or 6)
    temperature: float = float(_env("TEMPERATURE", "0.2") or 0.2)

    # Paths
    kb_dir: str = _env("KB_DIR", "data/kb") or "data/kb"
    index_dir: str = _env("INDEX_DIR", "data/index") or "data/index"
    feedback_dir: str = _env("FEEDBACK_DIR", "data/feedback") or "data/feedback"

settings = Settings()
