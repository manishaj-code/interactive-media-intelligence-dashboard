"""Data service for gallery metadata, ratings, playlists."""
import json
from pathlib import Path
from typing import Any, Optional

from config import (
    DATA_DIR,
    METADATA_FILE,
    RATINGS_FILE,
    PLAYLISTS_FILE,
    UPLOADS_DIR,
    GALLERY_DIR,
)


def load_json(path: Path, default: Any = None) -> Any:
    """Load JSON file, return default if not found."""
    if default is None:
        default = []
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return default if default is not None else {}


def save_json(path: Path, data: Any) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_gallery_items() -> list:
    """Get all gallery items from metadata."""
    return load_json(METADATA_FILE, [])


def save_gallery_items(items: list) -> None:
    """Save gallery metadata."""
    save_json(METADATA_FILE, items)


def get_ratings() -> dict:
    """Get user ratings {item_id: {user_id: rating}}."""
    return load_json(RATINGS_FILE, {})


def save_rating(item_id: str, rating: int, user_id: str = "default") -> None:
    """Save user rating for an item."""
    ratings = get_ratings()
    if item_id not in ratings:
        ratings[item_id] = {}
    ratings[item_id][user_id] = rating
    save_json(RATINGS_FILE, ratings)


def get_avg_rating(item_id: str) -> Optional[float]:
    """Get average rating for an item."""
    ratings = get_ratings()
    if item_id not in ratings:
        return None
    vals = list(ratings[item_id].values())
    return round(sum(vals) / len(vals), 1) if vals else None


def get_playlists() -> dict:
    """Get user playlists {playlist_name: [item_ids]}."""
    return load_json(PLAYLISTS_FILE, {})


def save_playlist(name: str, item_ids: list) -> None:
    """Save or update a playlist."""
    playlists = get_playlists()
    playlists[name] = item_ids
    save_json(PLAYLISTS_FILE, playlists)


def add_to_playlist(playlist_name: str, item_id: str) -> None:
    """Add item to playlist."""
    playlists = get_playlists()
    if playlist_name not in playlists:
        playlists[playlist_name] = []
    if item_id not in playlists[playlist_name]:
        playlists[playlist_name].append(item_id)
    save_json(PLAYLISTS_FILE, playlists)


def add_gallery_item(item: dict) -> str:
    """Add new item to gallery, return generated id."""
    items = get_gallery_items()
    new_id = f"item_{len(items) + 1}_{hash(str(item)) % 10000}"
    item["id"] = new_id
    items.append(item)
    save_gallery_items(items)
    return new_id
