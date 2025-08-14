## Usage

### Web UI
1. Navigate to `http://localhost:5000`.
2. Upload documents (PDF/TXT/MD) on the right panel.
3. Ask questions in the chat box on the left.
4. The model uses retrieved context from your uploaded documents when relevant.

### REST API Quick Reference

Chat
```http
POST /api/chat
Content-Type: application/json
{
  "messages": [
    {"role": "user", "content": "What does the document say about security?"}
  ],
  "top_k": 5
}
```

Upload
```http
POST /api/upload
Content-Type: multipart/form-data
file=@yourdoc.pdf
```

List Documents
```http
GET /api/docs
```

Health
```http
GET /healthz
```


