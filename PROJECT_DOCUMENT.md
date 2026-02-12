# Interactive Media Intelligence Dashboard
## Project Requirements Document

**Version:** 1.0  
**Date:** February 2025  
**Skills:** Streamlit, Python, AI/ML, Groq, Gemini  
**Target:** Capstone Project – Interactive Media Intelligence

---

## 1. Executive Summary

This document outlines the requirements for an **Interactive Image/Video Gallery Dashboard** that enables users to search for specific actions within media content, view detailed summaries with timestamps and transcripts, and contribute their own content. The system leverages AI/ML (Google Gemini and Groq) for intelligent search and summarization.

---

## 2. Project Objectives

| Objective | Description |
|-----------|-------------|
| **Seamless Search** | Enable users to search for specific actions across the gallery |
| **Rich Summaries** | Display action videos with starting times, transcripts, and relevant details |
| **Visual Representation** | Pair each action with corresponding images |
| **User Contribution** | Allow uploads when desired content is not found |
| **Engagement** | User ratings, categories, and personalized playlists |

---

## 3. Technical Stack

| Component | Technology |
|-----------|------------|
| **Frontend/UI** | Streamlit |
| **Language** | Python 3.10+ |
| **AI/ML – Primary** | Google Gemini API (video analysis, summaries) |
| **AI/ML – Secondary** | Groq API (fast inference for text summaries) |
| **Data Storage** | JSON (gallery metadata, ratings, playlists) |
| **Dependencies** | pandas, Pillow, google-generativeai, groq, python-dotenv |

---

## 4. Functional Requirements

### 4.1 Search & Discovery
- **FR-1.1** Search bar for actions, topics, or keywords
- **FR-1.2** Semantic/keyword-based search across titles, descriptions, actions, tags
- **FR-1.3** Filter by category (Cooking, Fitness, Technology, Music, Art, etc.)
- **FR-1.4** Filter by content type (video, image)
- **FR-1.5** Sort by: Relevance, Title A–Z/Z–A, Rating, Newest

### 4.2 Media Display
- **FR-2.1** Grid and list view modes
- **FR-2.2** Thumbnail preview for each item
- **FR-2.3** Video playback with embed support (e.g., YouTube)
- **FR-2.4** Image viewer with zoom/expand
- **FR-2.5** Key actions with start times displayed on each card

### 4.3 Detail View
- **FR-3.1** Full description and summary
- **FR-3.2** Action list with timestamps (e.g., 00:02:30)
- **FR-3.3** Transcript section (expandable)
- **FR-3.4** AI-generated summary (Gemini/Groq) on demand

### 4.4 Upload
- **FR-4.1** Form for uploading new videos or images
- **FR-4.2** Required: Title, Category, Type, Description
- **FR-4.3** Support for URL-based media (YouTube, direct image links)
- **FR-4.4** Optional: Tags, custom actions/timestamps

### 4.5 User Engagement
- **FR-5.1** Rate content (1–5 stars)
- **FR-5.2** Create custom playlists
- **FR-5.3** Add items to playlists from detail/card view
- **FR-5.4** View playlist contents in sidebar
- **FR-5.5** Persist ratings and playlists across sessions

### 4.6 AI/ML Features
- **FR-6.1** AI-powered search enhancement (when API keys available)
- **FR-6.2** On-demand AI summary generation (Gemini or Groq)
- **FR-6.3** Video analysis via Gemini (when video file/URL provided)
- **FR-6.4** Graceful fallback when APIs are not configured

---

## 5. Non-Functional Requirements

| NFR | Description |
|-----|-------------|
| **Usability** | Intuitive UI, minimal clicks to find content |
| **Performance** | Fast load times; lazy loading for large galleries |
| **Scalability** | JSON-based storage; migration path to DB (SQLite/PostgreSQL) |
| **Security** | API keys via environment variables (.env) |
| **Accessibility** | Semantic structure, readable fonts, sufficient contrast |

---

## 6. Data Model

### Gallery Item
```json
{
  "id": "item_1_cooking",
  "title": "Quick Pasta Carbonara Tutorial",
  "category": "Cooking",
  "type": "video",
  "source": "https://...",
  "thumbnail": "https://...",
  "description": "Learn to make...",
  "duration": "00:15:30",
  "actions": [
    {"name": "Boiling water", "start_time": "00:00:15", "timestamp_sec": 15}
  ],
  "transcript": "Welcome! Today we're making...",
  "tags": ["pasta", "cooking"]
}
```

### User Ratings
```json
{"item_id": {"user_id": 5}}
```

### Playlists
```json
{"My Favorites": ["item_1", "item_3"], "Workout": ["item_2"]}
```

---

## 7. Project Structure

```
interactive-media-intelligence-dashboard/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration (paths, API keys)
├── requirements.txt       # Python dependencies
├── .env.example           # API key template
├── services/
│   ├── ai_service.py      # Gemini & Groq integration
│   └── data_service.py    # Gallery, ratings, playlists
├── scripts/
│   └── generate_sample_data.py
├── data/
│   ├── gallery_metadata.json
│   ├── user_ratings.json
│   ├── user_playlists.json
│   ├── uploads/
│   └── thumbnails/
├── PROJECT_DOCUMENT.md    # This document
├── PROJECT_REPORT.md      # Project report with images
└── README.md
```

---

## 8. API Configuration

| Provider | Purpose | Key Variable |
|----------|---------|--------------|
| Google Gemini | Video analysis, text summaries | `GOOGLE_API_KEY` |
| Groq | Fast text summaries | `GROQ_API_KEY` |

Obtain keys:
- Gemini: https://makersuite.google.com/app/apikey
- Groq: https://console.groq.com/keys

---

## 9. Additional Interactive Features (Enhancement Ideas)

| Feature | Description | Priority |
|---------|-------------|----------|
| Favorites/Bookmarks | Quick access to saved items | High |
| Share link | Copy shareable URL for an item | Medium |
| Comments | User comments on items | Medium |
| Advanced filters | Date range, duration, rating threshold | Medium |
| Export playlist | Export playlist as JSON/CSV | Low |
| Dark/Light theme toggle | User preference | Low |
| Keyboard shortcuts | Navigate with keyboard | Low |

---

## 10. User Experience Goals

1. **Engaging** – Modern UI, clear visual hierarchy, responsive layout
2. **Informative** – Rich metadata, transcripts, AI summaries
3. **Efficient** – Fast search, filters, and minimal steps to reach content

---

## 11. Team Roles & Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Backend** | AI service, data layer, API integration |
| **Frontend** | Streamlit UI, layout, interactions |
| **Data** | Sample data, schema, migration scripts |
| **QA** | Test cases, UX validation |
| **DevOps** | Deployment (Streamlit Cloud, Docker) |

---

## 12. Acceptance Criteria

- [ ] User can search and filter gallery items
- [ ] User can view videos/images with action timestamps
- [ ] User can upload new content
- [ ] User can rate content and create playlists
- [ ] AI summary works when API keys are configured
- [ ] Sample data loads and displays correctly
- [ ] Project runs with `streamlit run app.py`

---

*Document prepared for the Interactive Media Intelligence Dashboard capstone project.*
