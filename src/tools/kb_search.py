import os
from pathlib import Path
from typing import List, Tuple

KB_DIR = Path(__file__).resolve().parents[2] / "data" / "kb"

def load_kb_file(filename: str) -> str:
    path = KB_DIR / filename
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def split_faq_blocks(text: str) -> List[str]:
    blocks = []
    current = []
    for line in text.splitlines():
        if line.startswith("## "):  # new question
            if current:
                blocks.append("\n".join(current).strip())
                current = []
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return [b for b in blocks if b]

def score_block(query: str, block: str) -> int:
    q = query.lower()
    keywords = [w for w in q.replace("?", "").split() if len(w) > 3]
    return sum(1 for kw in keywords if kw in block.lower())

def search_kb(filename: str, query: str, top_k: int = 1) -> List[Tuple[int, str]]:
    text = load_kb_file(filename)
    if not text:
        return []
    blocks = split_faq_blocks(text)
    scored = [(score_block(query, b), b) for b in blocks]
    scored = [item for item in scored if item[0] > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
