## RAG Details

### Ingestion
- Files accepted: PDF, TXT, MD
- PDF text extraction via `pypdf`
- Text is normalized to LF newlines
- Split into overlapping chunks (default 800 chars, 120 overlap)

### Embeddings
- Uses Gemini embeddings (`text-embedding-004` by default)
- Batch called per chunk (simple loop)
- Stored as float32 NumPy arrays on disk

### Storage
- Embeddings: `storage/vectors/index.npy`
- Metadata: `storage/vectors/metadatas.json`
- Documents: `storage/documents/`

### Retrieval
- Query embedding computed for the last user message
- scikit-learn `NearestNeighbors` with cosine metric
- Returns top-k chunk texts as RAG context

### Generation
- System-like context is prepended to a content list and sent to Gemini
- Model: `gemini-1.5-flash` by default


