## API

### POST /api/chat
- Body:
```json
{
  "messages": [{"role": "user"|"assistant", "content": "..."}],
  "top_k": 5
}
```
- Response:
```json
{
  "reply": "...",
  "context_count": 3
}
```

### POST /api/upload
- Multipart form-data with `file` (PDF/TXT/MD)
- Response:
```json
{
  "document_id": "uuid",
  "chunks": 42
}
```

### GET /api/docs
- Response:
```json
{
  "documents": [
    {"document_id": "...", "filename": "...", "chunks": 12}
  ]
}
```

### GET /healthz
- Response: `{ "status": "ok" }`

### POST /api/tools/call
- Body:
```json
{ "name": "web.fetch", "args": {"url": "https://example.com"} }
```
or
```json
{ "name": "env.get", "args": {"name": "PATH"} }
```
- Response:
```json
{ "result": { /* tool-specific fields */ } }
```


