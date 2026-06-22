import streamlit as st
from ytmusicapi import YTMusic
from textblob import TextBlob

# Initialize YouTube Music Client
@st.cache_resource
def get_yt_client():
    return YTMusic()

yt = get_yt_client()

# 1. Page Configuration
st.set_page_config(page_title="Spotify", page_icon="🎵", layout="wide")

# 2. Advanced CSS Injector for Core Spotify Layout & Theming
st.markdown("""
    <style>
    /* Absolute global theme properties */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: "Circular Sp", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    
    /* Clean up native Streamlit decorative overlays & toolbars */
    header, [data-testid="stHeader"], [data-testid="stToolbar"], #stDecoration {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* Custom Sidebar Left Panel Wrapper Overrides */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #121212;
        width: 260px !important;
    }
    
    /* Main Content Container Cards background padding layout matching Spotify main panel */
    [data-testid="stSidebarNav"] { display: none; } /* Hide default nav items */
    
    .main-panel-box {
        background: linear-gradient(to bottom, #222222 0%, #121212 40%) !important;
        background-color: #121212 !important;
        border-radius: 8px;
        padding: 24px;
        min-height: 85vh;
        margin-top: -30px;
    }

    /* Spotify pill inputs */
    .stTextInput input {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid transparent !important;
        border-radius: 50px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        transition: border 0.2s ease-in-out;
    }
    .stTextInput input:focus {
        border: 1px solid #ffffff !important;
        box-shadow: none !important;
    }
    
    /* Select Dropdowns */
    div[data-baseweb="select"] > div {
        background-color: #2a2a2a !important;
        border-radius: 4px !important;
        border: none !important;
        color: #fff !important;
    }
    
    /* True Spotify Green Buttons */
    .stButton>button {
        background-color: #1DB954 !important;
        color: #000000 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 12px 32px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: transform 0.1s ease, background-color 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1ED760 !important;
        transform: scale(1.04);
        color: #000000 !important;
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Spotify Track / Album Container Row Cards */
    .playlist-card {
        background-color: #181818;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid transparent;
        transition: background-color 0.3s ease;
    }
    .playlist-card:hover {
        background-color: #282828;
    }
    .playlist-title {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 700;
        text-decoration: none !important;
    }
    .playlist-title:hover {
        color: #1DB954 !important;
    }
    .playlist-meta {
        color: #b3b3b3;
        font-size: 13px;
        margin-top: 4px;
    }
    
    /* Custom Static Sidebar Links Styling */
    .sidebar-link {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        color: #b3b3b3;
        font-weight: bold;
        text-decoration: none;
        font-size: 14px;
        transition: color 0.2s ease;
    }
    .sidebar-link:hover {
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== NAVIGATION PANEL (SIDEBAR) ====================
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff; padding: 10px 16px; font-size: 24px;'>🎵 Spotify</h2>", unsafe_allow_html=True)
    st.write("")
    
    # Simple Radio Selector designed to simulate a real platform navigation list
    nav_option = st.radio(
        "Navigation",
        ["🧠 Mood AI", "🔍 Search Tracks/Movies", "🧑‍🎤 Artist Search", "🔥 Indian Trending"],
        label_visibility="collapsed"
    )
    
    st.write("---")
    st.markdown("<p style='color: #b3b3b3; font-size: 11px; padding: 0 16px;'>YOUR LIBRARY</p>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-link'>➕ Create Playlist</a>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-link'>❤️ Liked Songs</a>", unsafe_allow_html=True)

# ==================== MAIN PANEL WINDOW ====================
st.markdown('<div class="main-panel-box">', unsafe_allow_html=True)

# Dynamic view injection depending on what sidebar link is active
if nav_option == "🧠 Mood AI":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800;'>Vibe Check Recommender</h1>", unsafe_allow_html=True)
    user_input = st.text_input("How are you feeling right now?", key="mood_input", placeholder="What's your mood?")
    
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
                
            st.markdown(f"<p style='color: #1DB954; font-weight: bold; font-size: 14px;'>{status_msg}</p>", unsafe_allow_html=True)
            
            try:
                results = yt.search(search_query, filter="playlists", limit=2)
                for playlist in results:
                    title = playlist.get('title', 'Mood Mix')
                    author = playlist.get('author', 'YouTube Music')
                    clean_id = playlist.get('browseId').replace('VL', '') if playlist.get('browseId').startswith('VL') else playlist.get('browseId')
                    
                    st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">📌 {title}</a><div class="playlist-meta">Curated by {author}</div></div>', unsafe_allow_html=True)
                    st.video(f"https://www.youtube.com/playlist?list={clean_id}")
            except Exception as e:
                st.error(f"Error: {e}")

elif nav_option == "🔍 Search Tracks/Movies":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800;'>Search</h1>", unsafe_allow_html=True)
    search_term = st.text_input("Search for songs or movies...", key="track_input", placeholder="Artists, songs, or podcasts")
    
    if st.button("Search Track", key="track_btn"):
        if search_term.strip():
            try:
                songs = yt.search(search_term, filter="songs", limit=3)
                for song in songs:
                    artists = ", ".join([a['name'] for a in song.get('artists', [])])
                    album = song.get('album', {}).get('name', 'Single')
                    video_id = song.get('videoId')
                    
                    st.markdown(f'<div class="playlist-card"><span class="playlist-title">🎵 {song["title"]}</span><div class="playlist-meta">{artists} • {album}</div></div>', unsafe_allow_html=True)
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
            except Exception as e:
                st.error(f"Error: {e}")

elif nav_option == "🧑‍🎤 Artist Search":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800;'>Artist Profiles</h1>", unsafe_allow_html=True)
    artist_term = st.text_input("Search for an artist...", key="artist_input", placeholder="Who do you want to listen to?")
    
    if st.button("Find Artist Tracks", key="artist_btn"):
        if artist_term.strip():
            try:
                artist_songs = yt.search(f"{artist_term} songs", filter="songs", limit=3)
                for song in artist_songs:
                    video_id = song.get('videoId')
                    st.markdown(f'<div class="playlist-card"><span class="playlist-title">🎤 {song["title"]}</span><div class="playlist-meta">Album: {song.get("album", {}).get("name", "Unknown")}</div></div>', unsafe_allow_html=True)
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
            except Exception as e:
                st.error(f"Error: {e}")

elif nav_option == "🔥 Indian Trending":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800;'>🔥 Hot Hits India</h1>", unsafe_allow_html=True)
    st.write("Catch up on the most popular trending charts across languages:")
    
    languages = {
        "Hindi / Bollywood": "Hindi Trending Hits New Songs Playlist",
        "Punjabi": "Punjabi Latest Hits Trending Playlist",
        "Tamil": "Tamil Trending New Songs Playlist",
        "Telugu": "Telugu Latest Hits Trending Playlist",
        "Marathi": "Marathi Trending Hits New Songs Playlist",
        "Kannada": "Kannada Latest Hits Trending Playlist",
        "Malayalam": "Malayalam Trending New Songs Playlist",
        "Bhojpuri": "Bhojpuri New Trending Hits Playlist"
    }
    
    selected_lang = st.selectbox("Select Language Market", list(languages.keys()))
    
    if st.button("Play Chart", key="trend_btn"):
        try:
            trend_results = yt.search(languages[selected_lang], filter="playlists", limit=1)
            if trend_results:
                playlist = trend_results[0]
                clean_id = playlist.get('browseId').replace('VL', '') if playlist.get('browseId').startswith('VL') else playlist.get('browseId')
                
                st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">🔊 Hot Hits {selected_lang}</a></div>', unsafe_allow_html=True)
                st.video(f"https://www.youtube.com/playlist?list={clean_id}")
            else:
                st.info("Chart parsing unavailable right now.")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
