import os
import uuid
from typing import List, Dict, Any

from flask import Blueprint, jsonify, request, render_template

from .rag.store import VectorStore
from .rag.ingest import load_file_to_chunks
from .services.gemini_client import embed_texts, generate_response
from .tools.mcp_tools import tool_env_var, tool_web_fetch


bp = Blueprint("routes", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@bp.post("/api/chat")
def api_chat():
    data = request.get_json(force=True)
    messages: List[Dict[str, str]] = data.get("messages", [])
    top_k: int = int(data.get("top_k", 5))

    # RAG: use last user message for retrieval
    user_messages = [m for m in messages if m.get("role") == "user"]
    query_text = user_messages[-1].get("content") if user_messages else ""
    store = VectorStore()
    store.load()
    context_chunks: List[str] = []
    if query_text:
        query_emb = embed_texts([query_text])[0]
        results = store.search(query_emb, k=top_k)
        context_chunks = [r.text for r in results]

    reply = generate_response(messages=messages, context_chunks=context_chunks)
    return jsonify({"reply": reply, "context_count": len(context_chunks)})


@bp.post("/api/upload")
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in {".pdf", ".txt", ".md"}:
        return jsonify({"error": "Unsupported file type"}), 400

    document_id = str(uuid.uuid4())
    storage_dir = os.path.join(os.getcwd(), "storage", "documents")
    os.makedirs(storage_dir, exist_ok=True)
    save_path = os.path.join(storage_dir, f"{document_id}{ext}")
    file.save(save_path)

    chunks = load_file_to_chunks(save_path)
    embeddings = embed_texts([c["text"] for c in chunks])

    metadatas: List[Dict[str, Any]] = []
    for chunk, vector in zip(chunks, embeddings):
        metadatas.append(
            {
                "document_id": document_id,
                "filename": filename,
                "text": chunk["text"],
                "chunk_index": chunk["index"],
            }
        )

    store = VectorStore()
    store.load()
    store.add(embeddings, metadatas)

    return jsonify({"document_id": document_id, "chunks": len(chunks)})


@bp.get("/api/docs")
def api_docs():
    store = VectorStore()
    store.load()
    return jsonify({"documents": store.list_documents()})


@bp.post("/api/tools/call")
def api_tools_call():
    data = request.get_json(force=True)
    name = data.get("name")
    args = data.get("args", {})
    if name == "web.fetch":
        res = tool_web_fetch(args.get("url", ""))
    elif name == "env.get":
        res = tool_env_var(args.get("name", ""))
    else:
        return jsonify({"error": "Unknown tool"}), 400
    return jsonify({"result": res})


