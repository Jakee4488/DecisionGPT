import os
from typing import List, Optional, Dict, Any

import numpy as np


try:
    import google.generativeai as genai
except Exception as exc:  # pragma: no cover
    genai = None  # type: ignore


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")


def _configure_if_needed() -> None:
    global genai
    if genai is None:
        raise RuntimeError("google-generativeai is not installed.")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable is required.")
    genai.configure(api_key=api_key)


def embed_texts(texts: List[str]) -> np.ndarray:
    _configure_if_needed()
    vectors: List[List[float]] = []
    for text in texts:
        res = genai.embed_content(model=EMBED_MODEL, content=text)
        vectors.append(res["embedding"])  # type: ignore[index]
    return np.array(vectors, dtype=np.float32)


def build_system_prompt(context_chunks: List[str], tool_outputs: Optional[List[str]] = None) -> str:
    context_block = "\n\n".join(context_chunks[:10]) if context_chunks else ""
    tools_block = "\n\n".join(tool_outputs or [])
    parts = [
        "You are DecisionGPT, a helpful assistant that answers using the provided context when relevant.",
        "If the answer is not in the context, use your general knowledge but be clear about assumptions.",
    ]
    if context_block:
        parts.append("Context:\n" + context_block)
    if tools_block:
        parts.append("Tool Results:\n" + tools_block)
    return "\n\n".join(parts)


def generate_response(
    messages: List[Dict[str, str]],
    context_chunks: Optional[List[str]] = None,
    tool_outputs: Optional[List[str]] = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1024,
) -> str:
    _configure_if_needed()
    model = genai.GenerativeModel(GEMINI_MODEL)
    system_prompt = build_system_prompt(context_chunks or [], tool_outputs)

    contents: List[Dict[str, Any]] = []
    contents.append({"role": "user", "parts": [system_prompt]})
    for msg in messages:
        role = msg.get("role", "user")
        contents.append({"role": role, "parts": [msg.get("content", "")]})

    resp = model.generate_content(
        contents,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        },
    )
    return resp.text or ""



