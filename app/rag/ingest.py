from typing import List, Dict

import os
from pypdf import PdfReader


def _split_text(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> List[str]:
    chunks: List[str] = []
    start = 0
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - chunk_overlap)
    return chunks


def load_file_to_chunks(path: str) -> List[Dict[str, str | int]]:
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    text = ""
    if ext == ".pdf":
        reader = PdfReader(path)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    elif ext in {".txt", ".md"}:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type")

    chunks = _split_text(text)
    return [{"index": i, "text": c} for i, c in enumerate(chunks)]



