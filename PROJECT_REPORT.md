# Interactive Media Intelligence Dashboard
## Project Report

**Date:** February 2025  
**Project:** Capstone – Interactive Image/Video Gallery Dashboard  
**Technologies:** Streamlit, Python, Google Gemini, Groq

---

## 1. Project Overview

This report presents the **Interactive Media Intelligence Dashboard**, a Streamlit-based application that allows users to search for specific actions in a gallery of videos and images, view detailed summaries with timestamps and transcripts, and contribute their own content. The system integrates AI/ML capabilities via Google Gemini and Groq for intelligent search and summarization.

---

## 2. Design Concept & Mockup

The dashboard follows a modern, dark-themed design to provide an engaging and professional user experience:

![Dashboard Mockup](assets/dashboard-mockup.png)

**Key Design Elements:**
- **Left Sidebar:** Filters for category (Cooking, Fitness, Technology, etc.), content type (Video/Image), and sort options
- **Search Bar:** Prominent search for actions, topics, and keywords
- **Media Grid:** Cards showing thumbnails, titles, categories, ratings, and key actions with timestamps
- **Interactive Elements:** Rate, add to playlist, view details

---

## 3. Implemented Features

### 3.1 Core Functionality
| Feature | Status | Description |
|---------|--------|-------------|
| Search | ✅ | Keyword-based search across titles, descriptions, actions, tags |
| Filters | ✅ | Category, content type, sort (relevance, title, rating) |
| Grid/List View | ✅ | Toggle between grid and list layouts |
| Detail View | ✅ | Full description, actions with timestamps, transcript |
| Upload | ✅ | Form to add new videos/images via URL |

### 3.2 AI/ML Integration
| Feature | Provider | Description |
|---------|----------|-------------|
| Text Summary | Gemini / Groq | On-demand AI summary for each item |
| Video Analysis | Gemini | Video file/URL analysis (when API key set) |
| Semantic Search | Custom | Keyword matching with relevance scoring |

### 3.3 User Engagement
| Feature | Status | Description |
|---------|--------|-------------|
| Ratings | ✅ | 1–5 star rating per item, persisted |
| Playlists | ✅ | Create playlists, add items from cards |
| Categories | ✅ | Customizable categories (Cooking, Fitness, Tech, etc.) |

---

## 4. Sample Data

The project includes **8 sample items** spanning multiple categories:

| ID | Title | Category | Type |
|----|-------|----------|------|
| item_1 | Quick Pasta Carbonara Tutorial | Cooking | video |
| item_2 | Full Body HIIT Workout - 20 Minutes | Fitness | video |
| item_3 | Python Streamlit Dashboard Tutorial | Technology | video |
| item_4 | Guitar Chord Progressions - Am to F | Music | video |
| item_5 | Watercolor Landscape - Sunset Scene | Art | video |
| item_6 | Gemini API - Building AI-Powered Apps | Technology | video |
| item_7 | Cooking Action - Chopping Vegetables | Cooking | image |
| item_8 | Yoga Pose - Downward Dog | Fitness | image |

Each item includes:
- Title, description, category, thumbnail
- **Actions** with start times (e.g., "Boiling water @ 00:00:15")
- Transcript (for videos)
- Tags for search

---

## 5. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit App (app.py)                    │
├─────────────────────────────────────────────────────────────┤
│  UI: Search │ Filters │ Gallery │ Detail View │ Upload      │
├─────────────────────────────────────────────────────────────┤
│  services/ai_service.py  │  services/data_service.py        │
│  - Gemini (summaries)    │  - get_gallery_items()           │
│  - Groq (fast inference) │  - save_rating()                 │
│  - search_semantic()     │  - get_playlists()               │
├─────────────────────────────────────────────────────────────┤
│  data/ (JSON: gallery_metadata, user_ratings, playlists)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (if not already present)
python scripts/generate_sample_data.py

# Configure API keys (optional, for AI features)
# Copy .env.example to .env and add GOOGLE_API_KEY, GROQ_API_KEY

# Run the dashboard
streamlit run app.py
```

---

## 7. User Experience Highlights

1. **Engaging:** Dark gradient theme, clear visual hierarchy, responsive layout
2. **Informative:** Rich metadata, action timestamps, expandable transcripts, AI summaries
3. **Efficient:** Fast search, filters, sort options, minimal clicks to find content

---

## 8. Future Enhancements

- Favorites/bookmarks
- Share links for items
- User comments
- Advanced filters (duration, date range)
- Export playlists
- Dark/light theme toggle
- Keyboard shortcuts

---

## 9. Conclusion

The Interactive Media Intelligence Dashboard delivers an intuitive, AI-enhanced gallery experience. Users can search for specific actions, explore content with detailed summaries and timestamps, and contribute via uploads. Ratings and playlists support personalized discovery. The project is ready for team handoff; see `PROJECT_DOCUMENT.md` for full requirements.

---

*Report generated for the Interactive Media Intelligence Dashboard capstone project.*
