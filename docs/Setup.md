## Setup

### Prerequisites
- Python 3.10+
- A Google Gemini API key (`GOOGLE_API_KEY`)

### Install Dependencies
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Environment
Create a `.env` file in the project root (same folder as `manage.py`):
```dotenv
GOOGLE_API_KEY=your_actual_api_key_here
# Optional
# GEMINI_MODEL=gemini-1.5-flash
# GEMINI_EMBED_MODEL=text-embedding-004
```

Alternatively, set env vars in PowerShell for the current session:
```powershell
$env:GOOGLE_API_KEY = "your_actual_api_key_here"
```

### Run
```powershell
python manage.py
```
Open `http://localhost:5000`.


