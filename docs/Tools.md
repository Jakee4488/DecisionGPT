## Tools (MCP-style)

The app exposes a minimal tools endpoint to demonstrate MCP-style tool calls.

### Endpoint
POST `/api/tools/call`

### Available Tools
- `web.fetch`: Fetch a URL and return the response text (truncated).
  - Args: `{ "url": "https://example.com" }`
  - Returns: `{ "status": 200, "text": "..." }`
- `env.get`: Read an environment variable.
  - Args: `{ "name": "GOOGLE_API_KEY" }`
  - Returns: `{ "name": "GOOGLE_API_KEY", "value": "..." }`

### Example
```bash
curl -s -X POST http://localhost:5000/api/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"web.fetch","args":{"url":"https://example.com"}}'
```


