from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Chunk:
    doc_id: str
    title: str
    chunk_id: str
    text: str
    source_path: str

def _normalize_spaces(s: str) -> str:
    s = s.replace("\u00a0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def split_markdown(md: str, chunk_size: int = 900, chunk_overlap: int = 120) -> list[str]:
    """A simple, robust splitter for markdown in Chinese/English.
    Strategy: split by blank lines, then pack paragraphs into chunks.
    """
    md = _normalize_spaces(md)
    paras = [p.strip() for p in md.split("\n\n") if p.strip()]
    chunks = []
    cur = ""
    for p in paras:
        if not cur:
            cur = p
            continue
        if len(cur) + 2 + len(p) <= chunk_size:
            cur = cur + "\n\n" + p
        else:
            chunks.append(cur)
            # overlap: keep tail part
            if chunk_overlap > 0 and len(cur) > chunk_overlap:
                tail = cur[-chunk_overlap:]
                cur = tail + "\n\n" + p
            else:
                cur = p
    if cur:
        chunks.append(cur)
    return chunks

def load_kb_chunks(kb_dir: str, chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    kb_path = Path(kb_dir)
    files = sorted([p for p in kb_path.rglob("*.md") if p.is_file()])
    all_chunks: list[Chunk] = []
    for fp in files:
        doc_id = fp.stem
        md = fp.read_text(encoding="utf-8")
        title = _extract_title(md) or doc_id
        parts = split_markdown(md, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for i, t in enumerate(parts):
            all_chunks.append(
                Chunk(
                    doc_id=doc_id,
                    title=title,
                    chunk_id=f"{doc_id}#{i:03d}",
                    text=t,
                    source_path=str(fp.as_posix()),
                )
            )
    return all_chunks

def _extract_title(md: str) -> str | None:
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None
