import streamlit as st
from ytmusicapi import YTMusic
from textblob import TextBlob

# Initialize YouTube Music Client
@st.cache_resource
def get_yt_client():
    return YTMusic()

yt = get_yt_client()

# 1. Page Configuration & Custom Theme CSS
st.set_page_config(page_title="Moodify Pro", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    /* Main app background and text color */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    
    /* Fixes the white bar at the top */
    header, [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    
    /* Input field styling */
    .stTextInput input {
        background-color: #242424 !important;
        color: #FFFFFF !important;
        border: 1px solid #3E3E3E !important;
        border-radius: 50px !important;
        padding-left: 20px !important;
    }
    
    /* Green Spotify-like button styling */
    .stButton>button {
        background-color: #1DB954 !important;
        color: #FFFFFF !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.04);
        background-color: #1ED760 !important;
    }
    
    /* Playlists Container Box */
    .playlist-card {
        background-color: #181818;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #282828;
    }
    .playlist-title {
        color: #1DB954 !important;
        font-size: 18px !important;
        font-weight: bold;
        text-decoration: none;
    }
    .playlist-meta {
        color: #B3B3B3;
        font-size: 14px;
        margin-bottom: 10px;
    }
    
    /* Simple tab design alignment */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #181818;
        border-radius: 4px;
        color: #B3B3B3;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1DB954 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Header UI (Text-based Green Logo)
st.markdown("<h1 style='color: #1DB954; text-align: center; font-size: 42px;'>⚡ MOODIFY</h1>", unsafe_allow_html=True)
st.write("---")

# 3. Setting Up Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🧠 Mood AI", "🔍 Search Tracks/Movies", "🧑‍🎤 Artist Search", "🔥 Indian Trending"])

# ==================== TAB 1: MOOD AI ====================
with tab1:
    st.subheader("Vibe Check Recommender")
    user_input = st.text_input("How are you feeling right now?", key="mood_input")
    if st.button("Get Music", key="mood_btn"):
        if user_input.strip() == "":
            st.warning("Please enter your mood first!")
        else:
            analysis = TextBlob(user_input)
            polarity = analysis.sentiment.polarity
            
            if polarity < -0.1:
                search_query = "sad acoustic rainy day music playlist"
                status_msg = "💎 Finding something reflective and comforting..."
            elif polarity > 0.1:
                search_query = "upbeat high energy party dance music playlist"
                status_msg = "🔥 Finding something to boost the vibes!"
            else:
                search_query = "lofi chill ambient relaxed music playlist"
                status_msg = "☕ Finding a relaxed, mellow soundtrack..."
                
            st.markdown(f"<p style='color: #1DB954; font-weight: bold;'>{status_msg}</p>", unsafe_allow_html=True)
            
            try:
                results = yt.search(search_query, filter="playlists", limit=2)
                for playlist in results:
                    title = playlist.get('title', 'Mood Mix')
                    author = playlist.get('author', 'YouTube Music')
                    clean_id = playlist.get('browseId').replace('VL', '') if playlist.get('browseId').startswith('VL') else playlist.get('browseId')
                    
                    st.markdown(f'<div
