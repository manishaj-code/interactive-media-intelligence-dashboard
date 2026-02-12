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
)
from services.ai_service import search_semantic, get_ai_summary

# Page config
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
        
        # Create playlist
        new_pl = st.text_input("Create new playlist", key="new_playlist")
        if st.button("Create Playlist") and new_pl:
            save_playlist(new_pl.strip(), [])
            st.success(f"Created '{new_pl}'")
            st.rerun()
        
        st.divider()
        st.markdown("### 📤 Upload")
        st.caption("Use the upload section below")
    
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
    thumbnail = item.get("thumbnail", "https://picsum.photos/400/225")
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
            
            # Actions row
            r1, r2, r3 = st.columns(3)
            with r1:
                rating = st.slider("Rate", 1, 5, int(avg_rating or 3), key=f"rate_{item_id}")
                if st.button("Save rating", key=f"save_rate_{item_id}"):
                    save_rating(item_id, rating)
                    st.success("Saved!")
            
            playlists = get_playlists()
            with r2:
                pl_name = st.selectbox(
                    "Add to playlist",
                    [""] + list(playlists.keys()),
                    key=f"pl_{item_id}"
                )
                if pl_name and st.button("Add", key=f"add_pl_{item_id}"):
                    add_to_playlist(pl_name, item_id)
                    st.success("Added!")
            
            with r3:
                if st.button("View details", key=f"view_{item_id}"):
                    st.session_state.selected_item = item_id
                    st.rerun()
        
        st.divider()


def render_item_detail(item):
    """Render full item detail view."""
    item_id = item.get("id", "")
    st.markdown(f"## {item.get('title', '')}")
    st.caption(f"📂 {item.get('category')} | {item.get('type', 'video').upper()}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(item.get("thumbnail", "https://picsum.photos/800/450"), use_container_width=True)
        if item.get("type") == "video":
            st.video(item.get("source", ""))
        else:
            st.image(item.get("source", item.get("thumbnail")), use_container_width=True)
    
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
        if st.button("Generate AI summary", key="gen_summary"):
            summary = get_ai_summary(
                item.get("description", "") + "\n" + item.get("transcript", ""),
                "Summarize this content and highlight key moments."
            )
            st.info(summary)
    
    if st.button("← Back to gallery"):
        if "selected_item" in st.session_state:
            del st.session_state.selected_item
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
        url = st.text_input("Video/Image URL (YouTube embed or direct image link)", placeholder="https://...")
        uploaded_file = st.file_uploader("Or upload a file", type=["jpg", "jpeg", "png", "gif", "mp4", "webm"], accept_multiple_files=False)
        tags = st.text_input("Tags (comma-separated)", placeholder="tag1, tag2")
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if not title or not title.strip():
                st.error("Please enter a title.")
            else:
                source_url = url.strip() if url else ""
                thumbnail_url = source_url
                
                # Handle file upload
                if uploaded_file:
                    save_path = UPLOADS_DIR / uploaded_file.name
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    # Use relative path for local files - Streamlit can serve from data folder
                    source_url = str(save_path)
                    thumbnail_url = source_url if content_type == "image" else "https://picsum.photos/400/225"
                
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
    
    # Main content: Search
    col_search, col_view = st.columns([3, 1])
    with col_search:
        query = st.text_input(
            "🔍 Search actions, topics, or keywords",
            placeholder="e.g., cooking pasta, HIIT workout, guitar chords...",
            key="search_query"
        )
    with col_view:
        view_mode = st.radio("View", ["grid", "list"], horizontal=True, key="view_mode")
    
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
