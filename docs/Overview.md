## Overview

DecisionGPT is a Python Flask web app that provides Retrieval-Augmented Generation (RAG) chat using the Google Gemini API. It supports uploading documents (PDF/TXT/MD), creates embeddings for chunked content, and retrieves relevant context for each user query. It also exposes simple MCP-style tool calls.

### Key Features
- RAG pipeline: upload → chunk → embed → store → retrieve → answer
- Gemini chat integration for high-quality responses
- Document uploads: PDF, TXT, MD
- Persistent vector store (NumPy + scikit-learn KNN)
- Minimal, clean web UI (Pico.css)
- Simple MCP-like tools: `web.fetch`, `env.get`

### Tech Stack
- Flask for the web server and REST API
- google-generativeai for Gemini chat and embeddings
- scikit-learn (NearestNeighbors) for vector search
- pypdf for PDF text extraction
- Vanilla JS front-end with Pico.css
- Waitress for production-ready serving on Windows

### Typical Flow
1. User uploads a document.
2. The app splits text into chunks and generates embeddings.
3. Embeddings and metadata are persisted under `storage/`.
4. On chat, the last user message is embedded and used to retrieve top-k chunks.
5. The context is prepended to the prompt, and Gemini generates the reply.
6. Result is shown in the UI.


