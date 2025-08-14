## Deployment

### Windows (Waitress)
The default `manage.py` tries to use Waitress first.
```powershell
set GOOGLE_API_KEY=your_key
python manage.py
```

### Docker (example)
Create `Dockerfile` (not included by default):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=5000
CMD ["python", "manage.py"]
```

Build and run:
```bash
docker build -t decisiongpt .
docker run -e GOOGLE_API_KEY=your_key -p 5000:5000 decisiongpt
```


