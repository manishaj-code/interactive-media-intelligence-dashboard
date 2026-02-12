"""Configuration for Interactive Media Intelligence Dashboard."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
GALLERY_DIR = DATA_DIR / "gallery"
THUMBNAILS_DIR = DATA_DIR / "thumbnails"
METADATA_FILE = DATA_DIR / "gallery_metadata.json"
RATINGS_FILE = DATA_DIR / "user_ratings.json"
PLAYLISTS_FILE = DATA_DIR / "user_playlists.json"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# AI Provider preference: "gemini" or "groq"
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")

# Create directories
for d in [DATA_DIR, UPLOADS_DIR, GALLERY_DIR, THUMBNAILS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
