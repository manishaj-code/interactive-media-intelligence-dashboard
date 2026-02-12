"""
Interactive Media Intelligence Dashboard
Streamlit app for image/video gallery with AI-powered search and summaries.
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root
sys_path = Path(__file__).resolve().parent
sys.path.insert(0, str(sys_path))

from config import UPLOADS_DIR, GALLERY_DIR
from services.data_service import (
    get_gallery_items,
    save_gallery_items,
    get_ratings,
    save_rating,
    get_avg_rating,
    get_playlists,
    save_playlist,
    add_to_playlist,
    add_gallery_item,
    delete_gallery_item,
    clear_entire_gallery,
)
from services.ai_service import search_semantic, get_ai_summary
import re

# Page config


def extract_youtube_id(url: str):
    """Extract YouTube video ID from various URL formats."""
    if not url or not isinstance(url, str):
        return None
    patterns = [
        r"(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def normalize_youtube_url(url: str) -> str:
    """Convert YouTube URL to embed format for reliable playback."""
    vid = extract_youtube_id(url)
    return f"https://www.youtube.com/embed/{vid}" if vid else url


def get_youtube_thumbnail(url: str) -> str:
    """Get YouTube thumbnail image URL from video URL."""
    vid = extract_youtube_id(url)
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else url

st.set_page_config(
    page_title="Interactive Media Intelligence Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS - black background = white text, white background = black text
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    /* MAIN AREA: Black/dark background → WHITE text */
    .stApp, [data-testid="stAppViewContainer"] {
        background: #0a0a0a !important;
        color: #ffffff !important;
    }
    .stApp p, .stApp span, .stApp div[class*="stMarkdown"],
    [data-testid="stVerticalBlock"] p, [data-testid="stVerticalBlock"] .stMarkdown p,
    div[data-testid="stMarkdown"] p, div[data-testid="stMarkdown"] li,
    [data-testid="stWidgetLabel"] label, .stCaption {
        color: #ffffff !important;
    }
    .stApp h1, .stApp h2, .stApp h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
    }
    div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] label,
    [data-testid="stSlider"] label {
        color: #ffffff !important;
    }
    /* Expander on dark background → white text */
    div[data-testid="stExpander"] {
        background: #1a1a1a !important;
        border: 1px solid #333;
    }
    div[data-testid="stExpander"] p, div[data-testid="stExpander"] label {
        color: #ffffff !important;
    }

    /* SIDEBAR: White background → BLACK text */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background: #ffffff !important;
        color: #000000 !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] label,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[data-testid="stTextInput"] label {
        color: #000000 !important;
    }

    .metric-card { background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 1rem; }
    .action-badge { background: #667eea; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; }

    /* BUTTONS - all light grey */
    .stApp [data-testid="stButton"] button,
    .stApp button[kind="primary"],
    .stApp button[kind="secondary"],
    [data-testid="stSidebar"] [data-testid="stButton"] button,
    [data-testid="stSidebar"] button,
    [data-testid="stFormSubmitButton"] button,
    form button[type="submit"],
    button {
        background: #d3d3d3 !important;
        color: #000000 !important;
        border: 1px solid #b0b0b0 !important;
    }
    .stApp [data-testid="stButton"] button:hover,
    .stApp button[kind="primary"]:hover,
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover,
    [data-testid="stFormSubmitButton"] button:hover,
    form button[type="submit"]:hover,
    button:hover {
        background: #c0c0c0 !important;
        color: #000000 !important;
        border-color: #a0a0a0 !important;
    }
</style>
""", unsafe_allow_html=True)


def init_session():
    """Initialize session state."""
    if "playlist_name" not in st.session_state:
        st.session_state.playlist_name = ""
    if "favorites" not in st.session_state:
        st.session_state.favorites = set()
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "grid"


def render_sidebar():
    """Render sidebar with filters and playlists."""
    with st.sidebar:
        st.markdown("## 🎯 Filters & Navigation")
        st.divider()
        
        # Categories
        items = get_gallery_items()
        categories = ["All"] + sorted(set(i.get("category", "Other") for i in items))
        selected_cat = st.selectbox("Category", categories)
        
        # Content type
        types = ["All", "video", "image"]
        selected_type = st.selectbox("Content Type", types)
        
        # Sort
        sort_by = st.selectbox(
            "Sort by",
            ["Relevance", "Title A-Z", "Title Z-A", "Rating", "Newest"]
        )
        
        st.divider()
        st.markdown("### 📋 Playlists")
        playlists = get_playlists()
        if playlists:
            for name, ids in playlists.items():
                with st.expander(f"📁 {name} ({len(ids)} items)"):
                    for item_id in ids[:5]:
                        st.caption(f"• {item_id}")
                    if len(ids) > 5:
                        st.caption(f"... and {len(ids)-5} more")
        else:
            st.caption("No playlists yet. Create one from an item!")
        
        # Create playlist - compact
        with st.expander("➕ Create playlist"):
            new_pl = st.text_input("Playlist name", key="new_playlist", label_visibility="collapsed", placeholder="Enter name...")
            if st.button("Create", key="create_pl_btn") and new_pl:
                save_playlist(new_pl.strip(), [])
                st.success(f"Created '{new_pl}'")
                st.rerun()
        
        st.divider()
        st.caption("📤 Upload content in the section below")

        # Gallery actions
        with st.expander("⚙️ Gallery settings", expanded=False):
            if st.session_state.get("confirm_clear_gallery"):
                st.warning("Delete all items?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✓ Yes, clear all", key="clear_yes"):
                        clear_entire_gallery()
                        st.session_state.pop("confirm_clear_gallery", None)
                        if "selected_item" in st.session_state:
                            del st.session_state.selected_item
                        st.success("Gallery cleared!")
                        st.rerun()
                with c2:
                    if st.button("✗ Cancel", key="clear_no"):
                        st.session_state.pop("confirm_clear_gallery", None)
                        st.rerun()
            else:
                if st.button("🗑️ Delete entire gallery", key="clear_gallery"):
                    st.session_state["confirm_clear_gallery"] = True
                    st.rerun()
    
    return selected_cat, selected_type, sort_by


def filter_and_sort(items, category, content_type, sort_by, query=""):
    """Filter and sort gallery items."""
    if query:
        items = search_semantic(query, items)
    if category != "All":
        items = [i for i in items if i.get("category") == category]
    if content_type != "All":
        items = [i for i in items if i.get("type") == content_type]
    
    if sort_by == "Title A-Z":
        items = sorted(items, key=lambda x: x.get("title", "").lower())
    elif sort_by == "Title Z-A":
        items = sorted(items, key=lambda x: x.get("title", "").lower(), reverse=True)
    elif sort_by == "Rating":
        items = sorted(items, key=lambda x: get_avg_rating(x.get("id")) or 0, reverse=True)
    
    return items


def render_item_card(item, show_actions=True):
    """Render a single gallery item card."""
    item_id = item.get("id", "")
    title = item.get("title", "Untitled")
    category = item.get("category", "")
    desc = item.get("description", "")[:150] + "..." if len(item.get("description", "")) > 150 else item.get("description", "")
    source = item.get("source", "")
    thumbnail = item.get("thumbnail", "https://picsum.photos/400/225")
    if extract_youtube_id(source):
        thumbnail = get_youtube_thumbnail(source) or thumbnail
    item_type = item.get("type", "video")
    actions = item.get("actions", [])
    
    avg_rating = get_avg_rating(item_id)
    
    with st.container():
        col_img, col_info = st.columns([1, 2])
        with col_img:
            st.image(thumbnail, use_container_width=True)
        with col_info:
            st.markdown(f"### {title}")
            st.caption(f"📂 {category} | {'🎬 Video' if item_type == 'video' else '🖼️ Image'}")
            if avg_rating:
                st.markdown(f"⭐ {avg_rating}/5")
            st.write(desc)
            
            if show_actions and actions:
                st.markdown("**Key actions:**")
                for a in actions[:4]:
                    ts = a.get("start_time", "N/A")
                    name = a.get("name", "")
                    st.caption(f"• {name} @ {ts}")
            
            # Primary action - View details (prominent)
            if st.button("👁️ View details", key=f"view_{item_id}", use_container_width=True):
                st.session_state.selected_item = item_id
                st.rerun()
            
            # Secondary actions in expander
            with st.expander("⚡ Rate, playlist & more"):
                r1, r2 = st.columns(2)
                with r1:
                    st.caption("⭐ Rate")
                    rating = st.slider("Stars", 1, 5, int(avg_rating or 3), key=f"rate_{item_id}", label_visibility="collapsed")
                    if st.button("Save rating", key=f"save_rate_{item_id}", use_container_width=True):
                        save_rating(item_id, rating)
                        st.success("Saved!")
                with r2:
                    st.caption("📁 Add to playlist")
                    playlists = get_playlists()
                    pl_name = st.selectbox("Playlist", [""] + list(playlists.keys()), key=f"pl_{item_id}", label_visibility="collapsed")
                    if pl_name and st.button("➕ Add", key=f"add_pl_{item_id}", use_container_width=True):
                        add_to_playlist(pl_name, item_id)
                        st.success("Added!")
                st.caption("🗑️ Remove")
                if st.session_state.get(f"confirm_delete_{item_id}"):
                    d1, d2 = st.columns(2)
                    with d1:
                        if st.button("Yes, delete", key=f"confirm_del_{item_id}", use_container_width=True):
                            if delete_gallery_item(item_id):
                                st.session_state.pop(f"confirm_delete_{item_id}", None)
                                st.success("Deleted!")
                                st.rerun()
                    with d2:
                        if st.button("Cancel", key=f"cancel_del_{item_id}", use_container_width=True):
                            st.session_state.pop(f"confirm_delete_{item_id}", None)
                            st.rerun()
                else:
                    if st.button("🗑️ Delete", key=f"delete_{item_id}", use_container_width=True):
                        st.session_state[f"confirm_delete_{item_id}"] = True
                        st.rerun()
        
        st.divider()


def render_item_detail(item):
    """Render full item detail view."""
    item_id = item.get("id", "")
    st.markdown(f"## {item.get('title', '')}")
    st.caption(f"📂 {item.get('category')} | {item.get('type', 'video').upper()}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        source = item.get("source", "")
        thumb = item.get("thumbnail", "https://picsum.photos/800/450")
        if extract_youtube_id(source):
            thumb = get_youtube_thumbnail(source) or thumb
        st.image(thumb, use_container_width=True)
        if item.get("type") == "video":
            video_url = normalize_youtube_url(source) if source else source
            if video_url:
                st.video(video_url)
        else:
            st.image(source or thumb, use_container_width=True)
    
    with col2:
        st.markdown("### Summary")
        st.write(item.get("description", ""))
        
        st.markdown("### Key Actions")
        for a in item.get("actions", []):
            st.markdown(f"- **{a.get('name')}** @ `{a.get('start_time', 'N/A')}`")
        
        if item.get("transcript"):
            with st.expander("📜 Transcript"):
                st.write(item["transcript"])
        
        st.markdown("### AI Summary")
        if st.button("🤖 Generate AI summary", key="gen_summary", use_container_width=True):
            summary = get_ai_summary(
                item.get("description", "") + "\n" + item.get("transcript", ""),
                "Summarize this content and highlight key moments."
            )
            st.info(summary)
    
    # Action buttons - organized row
    st.markdown("---")
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if st.button("← Back to gallery", use_container_width=True):
            if "selected_item" in st.session_state:
                del st.session_state.selected_item
            st.rerun()
    with btn2:
        if st.session_state.get("confirm_delete_detail") == item_id:
            if st.button("✓ Yes, delete permanently", key="confirm_delete_detail_btn", use_container_width=True):
                if delete_gallery_item(item_id):
                    del st.session_state.selected_item
                    st.session_state.pop("confirm_delete_detail", None)
                    st.success("Item deleted.")
                    st.rerun()
        else:
            if st.button("🗑️ Delete item", key="delete_detail", use_container_width=True):
                st.session_state["confirm_delete_detail"] = item_id
                st.rerun()
    with btn3:
        if st.session_state.get("confirm_delete_detail") == item_id:
            if st.button("✗ Cancel", key="cancel_delete_detail", use_container_width=True):
                st.session_state.pop("confirm_delete_detail", None)
                st.rerun()


def render_upload():
    """Upload new content."""
    st.markdown("## 📤 Upload Content")
    st.caption("Contribute videos or images to the gallery (URL or file)")
    
    with st.form("upload_form", clear_on_submit=True):
        title = st.text_input("Title *", placeholder="Enter title")
        category = st.selectbox("Category", ["Cooking", "Fitness", "Technology", "Music", "Art", "Other"])
        content_type = st.selectbox("Type", ["video", "image"])
        description = st.text_area("Description", placeholder="Brief description")
        url = st.text_input("Video/Image URL (YouTube or direct link)", placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...")
        uploaded_file = st.file_uploader("Or upload a file", type=["jpg", "jpeg", "png", "gif", "mp4", "webm"], accept_multiple_files=False)
        tags = st.text_input("Tags (comma-separated)", placeholder="tag1, tag2")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if not title or not title.strip():
                st.error("Please enter a title.")
            elif content_type == "video" and not uploaded_file and not (url and url.strip()):
                st.error("For video, please enter a YouTube URL or upload a video file.")
            else:
                source_url = (url or "").strip()
                thumbnail_url = source_url
                
                # Handle file upload
                if uploaded_file:
                    save_path = UPLOADS_DIR / uploaded_file.name
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    source_url = str(save_path)
                    thumbnail_url = source_url if content_type == "image" else "https://picsum.photos/400/225"
                # Handle YouTube URL for video
                elif content_type == "video" and source_url and extract_youtube_id(source_url):
                    source_url = normalize_youtube_url(source_url)
                    thumbnail_url = get_youtube_thumbnail(source_url)
                
                if not source_url:
                    source_url = "https://picsum.photos/800/600"
                if not thumbnail_url or (content_type == "video" and extract_youtube_id(source_url)):
                    thumbnail_url = get_youtube_thumbnail(source_url) or "https://picsum.photos/400/225"
                
                item = {
                    "title": title.strip(),
                    "category": category,
                    "type": content_type,
                    "description": description.strip() if description else "",
                    "source": source_url or "https://picsum.photos/800/600",
                    "thumbnail": thumbnail_url or "https://picsum.photos/400/225",
                    "actions": [{"name": "Uploaded content", "start_time": "00:00:00", "timestamp_sec": 0}],
                    "transcript": "",
                    "tags": [t.strip() for t in (tags or "").split(",") if t.strip()],
                }
                new_id = add_gallery_item(item)
                st.success(f"Added! ID: {new_id}")
                st.balloons()
                st.rerun()


def main():
    init_session()
    
    # Header
    st.markdown("# 🎬 Interactive Media Intelligence Dashboard")
    st.markdown("*Search, explore, and discover action-packed videos and images*")
    st.divider()
    
    # Sidebar
    selected_cat, selected_type, sort_by = render_sidebar()
    
    # Selected item detail view
    if "selected_item" in st.session_state:
        items = get_gallery_items()
        match = next((i for i in items if i.get("id") == st.session_state.selected_item), None)
        if match:
            render_item_detail(match)
            return
    
    # Main content: Search toolbar
    st.markdown("#### 🔍 Search & browse")
    col_search, col_view, col_upload = st.columns([4, 1, 1])
    with col_search:
        query = st.text_input(
            "Search",
            placeholder="e.g., cooking pasta, HIIT workout, guitar chords...",
            key="search_query",
            label_visibility="collapsed"
        )
    with col_view:
        view_mode = st.radio("View", ["grid", "list"], format_func=lambda x: "🔲 Grid" if x == "grid" else "📋 List", horizontal=True, key="view_mode", label_visibility="collapsed")
    
    # Filter and sort
    items = get_gallery_items()
    if not items:
        st.warning("No items in gallery. Run `python scripts/generate_sample_data.py` or upload content.")
        render_upload()
        return
    
    filtered = filter_and_sort(items, selected_cat, selected_type, sort_by, query)
    
    st.markdown(f"### Found {len(filtered)} result(s)")
    
    # Gallery
    for item in filtered:
        render_item_card(item)
    
    # Upload section
    st.divider()
    with st.expander("📤 Upload new content", expanded=True):
        render_upload()


if __name__ == "__main__":
    main()
