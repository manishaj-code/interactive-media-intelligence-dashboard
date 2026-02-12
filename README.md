# Interactive Media Intelligence Dashboard

An interactive Streamlit dashboard for an image/video gallery with AI-powered search, detailed action summaries, user ratings, playlists, and upload capabilities.

## Skills & Tech Stack

- **Streamlit** – Web UI
- **Python 3.10+** – Backend
- **Google Gemini** – Video analysis, summaries
- **Groq** – Fast AI inference
- **AI/ML** – Search, summarization

## Features

- **Search** – Find actions, topics, keywords across the gallery
- **Filters** – Category, content type, sort options
- **Detail View** – Descriptions, action timestamps, transcripts
- **AI Summaries** – On-demand summaries via Gemini or Groq
- **Ratings** – 1–5 star ratings per item
- **Playlists** – Create playlists and add items
- **Upload** – Add new videos/images via URL

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python scripts/generate_sample_data.py

# 3. (Optional) Set API keys for AI features
# Copy .env.example to .env
# Add GOOGLE_API_KEY and/or GROQ_API_KEY

# 4. Run the app
streamlit run app.py
```

## Project Structure

```
├── app.py                 # Main Streamlit app
├── config.py              # Configuration
├── requirements.txt
├── services/
│   ├── ai_service.py      # Gemini & Groq
│   └── data_service.py    # Data layer
├── scripts/
│   └── generate_sample_data.py
├── data/
│   ├── gallery_metadata.json
│   ├── user_ratings.json
│   └── user_playlists.json
├── PROJECT_DOCUMENT.md    # Full requirements
├── PROJECT_REPORT.md      # Report with images
└── README.md
```

## API Keys

- **Gemini:** https://makersuite.google.com/app/apikey
- **Groq:** https://console.groq.com/keys

Set in `.env` or environment variables.

## Documentation

- **PROJECT_DOCUMENT.md** – Full requirements for the team
- **PROJECT_REPORT.md** – Project report with design mockup
