"""Production entrypoint for the HandEcho managed website."""
from pathlib import Path

from fastapi.staticfiles import StaticFiles

from api import app

SITE_DIR = Path(__file__).resolve().parent / "site"

# API routes are registered by api.py before the static catch-all mount.
app.mount("/", StaticFiles(directory=SITE_DIR, html=True), name="site")
