"""AI/ML Service - Gemini and Groq integration for video analysis and summaries."""
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import GOOGLE_API_KEY, GROQ_API_KEY, AI_PROVIDER


def get_video_summary_gemini(video_path: str = None, video_url: str = None, prompt: str = "") -> str:
    """Generate video summary using Google Gemini API."""
    if not GOOGLE_API_KEY:
        return "[Demo] Enable Gemini API by setting GOOGLE_API_KEY in .env for AI-powered video analysis."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        if video_path and Path(video_path).exists():
            video_file = genai.upload_file(video_path)
            response = model.generate_content([
                video_file,
                prompt or "Summarize this video. Extract key actions with timestamps. Provide a transcript overview."
            ])
        elif video_url:
            response = model.generate_content([
                f"Analyze this video: {video_url}. " + (prompt or "Summarize key actions with timestamps.")
            ])
        else:
            return "No video provided for analysis."
        
        return response.text if response.text else "No summary generated."
    except Exception as e:
        return f"[Error] Gemini: {str(e)}"


def get_text_summary_groq(text: str, prompt: str = "Summarize:") -> str:
    """Generate text summary using Groq API (fast inference)."""
    if not GROQ_API_KEY:
        return "[Demo] Enable Groq API by setting GROQ_API_KEY in .env for fast AI summaries."
    
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Error] Groq: {str(e)}"


def get_text_summary_gemini(text: str, prompt: str = "Summarize:") -> str:
    """Generate text summary using Google Gemini API."""
    if not GOOGLE_API_KEY:
        return "[Demo] Enable Gemini API for AI-powered summaries."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{prompt}\n\n{text}")
        return response.text if response.text else "No summary generated."
    except Exception as e:
        return f"[Error] Gemini: {str(e)}"


def get_ai_summary(text: str, prompt: str = "Summarize:") -> str:
    """Get AI summary using configured provider (Gemini or Groq)."""
    if AI_PROVIDER == "groq":
        return get_text_summary_groq(text, prompt)
    return get_text_summary_gemini(text, prompt)


def search_semantic(query: str, items: list, text_field: str = "description") -> list:
    """Simple keyword-based search (AI-enhanced when API available)."""
    query_lower = query.lower().strip()
    if not query_lower:
        return items
    
    scored = []
    for item in items:
        text = str(item.get(text_field, "")) + " " + str(item.get("title", "")) + " " + str(item.get("actions", []))
        text_lower = text.lower()
        score = sum(1 for w in query_lower.split() if w in text_lower)
        if score > 0:
            scored.append((score, item))
    
    scored.sort(key=lambda x: -x[0])
    return [item for _, item in scored]
