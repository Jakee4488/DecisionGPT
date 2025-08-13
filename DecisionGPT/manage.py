from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use waitress on Windows in production-like runs if desired; flask dev server otherwise
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    except Exception:
        app.run(host="0.0.0.0", port=5000, debug=True)



