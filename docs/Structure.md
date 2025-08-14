## Project Structure

```
DecisionGPT/
├── manage.py                # Entrypoint
├── requirements.txt         # Dependencies
├── README.md                # Quick start + links
├── .gitignore               # Ignore rules
├── app/
│   ├── __init__.py          # App factory, dotenv, blueprint
│   ├── routes.py            # API + UI routes
│   ├── rag/
│   │   ├── ingest.py        # File loaders + chunking
│   │   └── store.py         # Vector store + KNN
│   ├── services/
│   │   └── gemini_client.py # Embeddings + generation
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
└── docs/                    # Documentation
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


