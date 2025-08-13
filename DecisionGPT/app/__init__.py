import os
from flask import Flask


def ensure_directories() -> None:
    base = os.path.join(os.getcwd(), "storage")
    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, "documents"), exist_ok=True)
    os.makedirs(os.path.join(base, "vectors"), exist_ok=True)


def create_app() -> Flask:
    from dotenv import load_dotenv

    load_dotenv()
    ensure_directories()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25MB uploads

    # Register routes
    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)
    return app



