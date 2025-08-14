## DecisionGPT

Flask RAG chat app using Google Gemini, with uploads and simple MCP-style tools.

### Quick Links
- See `docs/Overview.md`
- Architecture: `docs/Architecture.md`
- Setup: `docs/Setup.md`
- Usage: `docs/Usage.md`
- API: `docs/API.md`
- RAG details: `docs/RAG.md`
- Tools: `docs/Tools.md`
- Deployment: `docs/Deployment.md`
- Troubleshooting: `docs/Troubleshooting.md`
- Structure: `docs/Structure.md`

### Project Structure
```
DecisionGPT/
├── manage.py                # Entrypoint (waitress or dev server)
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignore rules
├── README.md                # Quick start and docs links
├── app/
│   ├── __init__.py          # App factory, dotenv, blueprint
│   ├── routes.py            # API + UI routes
│   ├── rag/
│   │   ├── ingest.py        # File loaders + chunking
│   │   └── store.py         # Vector store + KNN
│   ├── services/
│   │   └── gemini_client.py # Gemini embeddings + chat
│   ├── tools/
│   │   └── mcp_tools.py     # MCP-like tools
│   ├── templates/
│   │   └── index.html       # UI template
│   └── static/
│       ├── style.css        # UI styles
│       └── main.js          # UI logic
├── storage/
│   ├── documents/           # Uploaded files
│   └── vectors/             # Embeddings + metadata
└── docs/                    # Detailed documentation
    ├── Overview.md
    ├── Architecture.md
    ├── Setup.md
    ├── Usage.md
    ├── API.md
    ├── RAG.md
    ├── Tools.md
    ├── Deployment.md
    └── Troubleshooting.md
```

### Setup (short)
1. Create a virtual environment and install deps:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
2. Set environment:
```
set GOOGLE_API_KEY=your_key
```

### Run
```
python manage.py
```

Open `http://localhost:5000`.

