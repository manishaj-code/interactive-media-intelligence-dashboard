"""Generate sample gallery data for Interactive Media Intelligence Dashboard."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import METADATA_FILE, DATA_DIR

SAMPLE_ITEMS = [
    {
        "id": "item_1_cooking",
        "title": "Quick Pasta Carbonara Tutorial",
        "category": "Cooking",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/pasta1/400/225",
        "description": "Learn to make authentic Italian Carbonara in 15 minutes. Creamy egg-based sauce with guanciale and pecorino.",
        "duration": "00:15:30",
        "actions": [
            {"name": "Boiling water for pasta", "start_time": "00:00:15", "timestamp_sec": 15},
            {"name": "Frying guanciale", "start_time": "00:02:30", "timestamp_sec": 150},
            {"name": "Mixing egg yolks with cheese", "start_time": "00:05:00", "timestamp_sec": 300},
            {"name": "Combining pasta with sauce", "start_time": "00:12:00", "timestamp_sec": 720},
        ],
        "transcript": "Welcome! Today we're making Carbonara. First, get your water boiling... Add salt, then the pasta...",
        "tags": ["pasta", "italian", "carbonara", "cooking", "quick meal"],
    },
    {
        "id": "item_2_fitness",
        "title": "Full Body HIIT Workout - 20 Minutes",
        "category": "Fitness",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/hiit1/400/225",
        "description": "High-intensity interval training for total body conditioning. No equipment needed.",
        "duration": "00:20:00",
        "actions": [
            {"name": "Warm-up jog in place", "start_time": "00:00:00", "timestamp_sec": 0},
            {"name": "Jump squats", "start_time": "00:03:00", "timestamp_sec": 180},
            {"name": "Burpees", "start_time": "00:06:30", "timestamp_sec": 390},
            {"name": "Mountain climbers", "start_time": "00:10:00", "timestamp_sec": 600},
            {"name": "Cool-down stretches", "start_time": "00:17:00", "timestamp_sec": 1020},
        ],
        "transcript": "Let's get started! Warm up for 3 minutes... Now jump squats for 45 seconds...",
        "tags": ["hiit", "workout", "fitness", "no equipment", "cardio"],
    },
    {
        "id": "item_3_tech",
        "title": "Python Streamlit Dashboard Tutorial",
        "category": "Technology",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/streamlit1/400/225",
        "description": "Build an interactive data dashboard with Streamlit and Python. Includes charts and filters.",
        "duration": "00:25:45",
        "actions": [
            {"name": "Project setup", "start_time": "00:00:30", "timestamp_sec": 30},
            {"name": "Creating sidebar filters", "start_time": "00:05:00", "timestamp_sec": 300},
            {"name": "Adding charts with Plotly", "start_time": "00:12:00", "timestamp_sec": 720},
            {"name": "Deploying to Streamlit Cloud", "start_time": "00:20:00", "timestamp_sec": 1200},
        ],
        "transcript": "Hello! In this tutorial we'll build a Streamlit dashboard. First, create your project folder...",
        "tags": ["python", "streamlit", "dashboard", "data visualization", "tutorial"],
    },
    {
        "id": "item_4_music",
        "title": "Guitar Chord Progressions - Am to F",
        "category": "Music",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/guitar1/400/225",
        "description": "Learn smooth chord transitions from Am to F. Perfect for beginners.",
        "duration": "00:08:20",
        "actions": [
            {"name": "Am chord finger position", "start_time": "00:00:45", "timestamp_sec": 45},
            {"name": "Transition practice", "start_time": "00:03:00", "timestamp_sec": 180},
            {"name": "F chord introduction", "start_time": "00:05:30", "timestamp_sec": 330},
            {"name": "Full progression playthrough", "start_time": "00:06:45", "timestamp_sec": 405},
        ],
        "transcript": "Today we're working on the Am to F transition. Start with Am... Keep your thumb behind the neck...",
        "tags": ["guitar", "chords", "music", "beginner", "acoustic"],
    },
    {
        "id": "item_5_art",
        "title": "Watercolor Landscape - Sunset Scene",
        "category": "Art",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/watercolor1/400/225",
        "description": "Paint a beautiful sunset using wet-on-wet watercolor technique. Step-by-step for all skill levels.",
        "duration": "00:18:00",
        "actions": [
            {"name": "Sky wash application", "start_time": "00:01:00", "timestamp_sec": 60},
            {"name": "Sun placement", "start_time": "00:04:00", "timestamp_sec": 240},
            {"name": "Foreground silhouette", "start_time": "00:10:00", "timestamp_sec": 600},
            {"name": "Detail refinement", "start_time": "00:14:00", "timestamp_sec": 840},
        ],
        "transcript": "We'll start with a wet paper wash. Load your brush with orange and yellow...",
        "tags": ["watercolor", "landscape", "sunset", "painting", "tutorial"],
    },
    {
        "id": "item_6_ai",
        "title": "Gemini API - Building AI-Powered Apps",
        "category": "Technology",
        "type": "video",
        "source": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "thumbnail": "https://picsum.photos/seed/gemini1/400/225",
        "description": "Integrate Google Gemini API for text generation, summarization, and multimodal analysis.",
        "duration": "00:22:15",
        "actions": [
            {"name": "API key setup", "start_time": "00:00:45", "timestamp_sec": 45},
            {"name": "Text generation example", "start_time": "00:05:30", "timestamp_sec": 330},
            {"name": "Image analysis with Gemini", "start_time": "00:12:00", "timestamp_sec": 720},
            {"name": "Video summarization", "start_time": "00:17:00", "timestamp_sec": 1020},
        ],
        "transcript": "Welcome! We'll use the Gemini API for various AI tasks. First, get your API key from Google AI Studio...",
        "tags": ["gemini", "ai", "python", "api", "machine learning"],
    },
    {
        "id": "item_7_image",
        "title": "Cooking Action - Chopping Vegetables",
        "category": "Cooking",
        "type": "image",
        "source": "https://picsum.photos/seed/chopping/800/600",
        "thumbnail": "https://picsum.photos/seed/chopping/400/225",
        "description": "Proper knife technique for dicing onions and vegetables safely.",
        "actions": [{"name": "Chopping vegetables", "start_time": "N/A", "timestamp_sec": 0}],
        "transcript": "",
        "tags": ["cooking", "knife", "vegetables", "technique"],
    },
    {
        "id": "item_8_image",
        "title": "Yoga Pose - Downward Dog",
        "category": "Fitness",
        "type": "image",
        "source": "https://picsum.photos/seed/yoga1/800/600",
        "thumbnail": "https://picsum.photos/seed/yoga1/400/225",
        "description": "Correct form for Adho Mukha Svanasana (Downward Dog) for flexibility and strength.",
        "actions": [{"name": "Downward dog pose", "start_time": "N/A", "timestamp_sec": 0}],
        "transcript": "",
        "tags": ["yoga", "stretch", "flexibility", "pose"],
    },
]


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(SAMPLE_ITEMS, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(SAMPLE_ITEMS)} sample items at {METADATA_FILE}")


if __name__ == "__main__":
    main()
