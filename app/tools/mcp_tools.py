from typing import Any, Dict

import os
import requests


def tool_web_fetch(url: str, timeout: int = 10) -> Dict[str, Any]:
    try:
        resp = requests.get(url, timeout=timeout)
        return {"status": resp.status_code, "text": resp.text[:20000]}
    except Exception as exc:
        return {"error": str(exc)}


def tool_env_var(name: str) -> Dict[str, Any]:
    return {"name": name, "value": os.getenv(name)}



