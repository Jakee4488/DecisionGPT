## Troubleshooting

### The server doesn’t stop
`python manage.py` starts a web server and runs until you stop it. Use Ctrl+C.

### 401/403 from Gemini
- Ensure `GOOGLE_API_KEY` is set and valid.
- Verify billing/quotas and model access.

### `google-generativeai` errors
- Reinstall deps: `pip install -r requirements.txt`
- Ensure Python 3.10+.

### Upload fails
- Only `.pdf`, `.txt`, `.md` are accepted by default.
- Max upload size is 25 MB (see `app/__init__.py`).

### No results from RAG
- Upload documents first.
- Check `storage/vectors/` contains `index.npy` and `metadatas.json`.

### Windows path issues
- Run from project root.
- Avoid non-ASCII paths for uploads.


