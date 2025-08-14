## Architecture

### Components
- `manage.py`: App entrypoint. Starts waitress (fallback to Flask dev server).
- `app/__init__.py`: App factory. Loads `.env`, prepares storage, registers routes.
- `app/routes.py`: HTTP endpoints for UI, chat, uploads, docs list, and tools.
- `app/rag/ingest.py`: File loading and text chunking.
- `app/rag/store.py`: Vector store with NearestNeighbors and disk persistence.
- `app/services/gemini_client.py`: Gemini client for embeddings and chat.
- `app/tools/mcp_tools.py`: Simple MCP-like tools.
- `app/templates/index.html`, `app/static/*`: UI.

### High-Level Diagram
```mermaid
graph TD
  UI[Web UI] -->|/api/upload| Upload[Upload Handler]
  UI -->|/api/chat| Chat[Chat Handler]
  Upload --> Ingest[Chunk + Embed]
  Ingest --> Store[(Vector Store)]
  Chat --> Retrieve[Embed Query + KNN]
  Retrieve --> Store
  Retrieve --> Context[Top-K Context]
  Context --> Prompt[Prompt Builder]
  Prompt --> Gemini[Gemini API]
  Gemini --> UI
  UI -->|/api/tools/call| Tools[Tools Endpoint]
  Tools --> WebFetch[web.fetch]
  Tools --> EnvGet[env.get]
```

### Data Storage
- `storage/documents/`: Uploaded files.
- `storage/vectors/index.npy`: Numpy array of embeddings.
- `storage/vectors/metadatas.json`: Chunk metadata and text for retrieval.


