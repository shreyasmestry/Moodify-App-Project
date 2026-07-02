import streamlit as st
import streamlit.components.v1 as components
from ytmusicapi import YTMusic
from textblob import TextBlob

# Initialize YouTube Music Client
@st.cache_resource
def get_yt_client():
    return YTMusic()

yt = get_yt_client()

# 1. Page Configuration
st.set_page_config(page_title="Moodify Pro", page_icon="⚡", layout="wide")

# 2. Seamless Theme Fusion CSS 
st.markdown("""
    <style>
    html, body, .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stAppViewBlockContainer"], 
    .block-container, 
    [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #121212 !important;
        color: #FFFFFF !important;
        font-family: "Circular Sp", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    header, [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: rgba(0,0,0,0) !important;
        background: transparent !important;
        color: #FFFFFF !important;
    }
    
    #stDecoration {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #1c1c1c;
    }
    [data-testid="stSidebarNav"] { display: none; } 

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: #E5E5E5 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 6px 0px !important;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] [data-checked="true"] label {
        color: #1DB954 !important;
    }

    .main-panel-box {
        width: 100%;
    }

    .stTextInput input {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid transparent !important;
        border-radius: 50px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
    
    .stButton>button {
        background-color: #1DB954 !important;
        color: #000000 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 12px 32px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        transition: transform 0.1s ease;
    }
    .stButton>button:hover {
        background-color: #1ED760 !important;
        transform: scale(1.04);
        color: #000000 !important;
    }
    
    .playlist-card {
        background-color: #181818;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .playlist-title {
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 700;
        text-decoration: none !important;
    }
    .playlist-meta {
        color: #b3b3b3;
        font-size: 13px;
    }
    .sidebar-link {
        display: flex;
        align-items: center;
        padding: 8px 0px;
        color: #b3b3b3;
        font-weight: bold;
        text-decoration: none;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to embed playlists using an iframe safely
def embed_youtube_playlist(playlist_id):
    iframe_code = f"""
    <iframe width="100%" height="450" 
        src="https://www.youtube.com/embed/videoseries?list={playlist_id}" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen
        style="border-radius: 12px;">
    </iframe>
    """
    components.html(iframe_code, height=460)

# ==================== NAVIGATION PANEL (SIDEBAR) ====================
with st.sidebar:
    st.markdown("<h1 style='color: #1DB954; padding: 15px 0px; font-size: 46px; font-weight: 900; margin-bottom: 10px;'>⚡ Moodify</h1>", unsafe_allow_html=True)
    
    nav_option = st.radio(
        "Navigation",
        ["🧠 Mood AI", "🔍 Search Tracks/Movies", "🧑‍🎤 Artist Search", "🔥 Indian Trending"],
        label_visibility="collapsed"
    )
    
    st.write("---")
    st.markdown("<p style='color: #b3b3b3; font-size: 11px; letter-spacing: 1px;'>YOUR LIBRARY</p>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-link'>➕ Create Playlist</a>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-link'>❤️ Liked Songs</a>", unsafe_allow_html=True)

# ==================== MAIN PANEL WINDOW ====================
st.markdown('<div class="main-panel-box">', unsafe_allow_html=True)

if nav_option == "🧠 Mood AI":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800; margin-bottom: 20px;'>🧠 Mood AI Dashboard</h1>", unsafe_allow_html=True)
    user_input = st.text_input("How are you feeling right now?", key="mood_input", placeholder="What's your mood vibe?")
    
    if st.button("Get Music", key="mood_btn"):
        if user_input.strip() == "":
            st.warning("Please enter your mood first!")
        else:
            analysis = TextBlob(user_input)
            polarity = analysis.sentiment.polarity
            
            if polarity < -0.1:
                search_query = "sad acoustic rainy day mix"
                status_msg = "💎 Finding something reflective and comforting..."
            elif polarity > 0.1:
                search_query = "upbeat high energy party dance mix"
                status_msg = "🔥 Finding something to boost the vibes!"
            else:
                search_query = "lofi chill ambient relaxed mix"
                status_msg = "☕ Finding a relaxed, mellow soundtrack..."
                
            st.markdown(f"<p style='color: #1DB954; font-weight: bold; font-size: 14px;'>{status_msg}</p>", unsafe_allow_html=True)
            
            try:
                results = yt.search(search_query, filter="playlists", limit=2)
                for playlist in results:
                    title = playlist.get('title', 'Mood Mix')
                    author = playlist.get('author', 'YouTube Music')
                    clean_id = playlist.get('browseId')
                    
                    if clean_id.startswith('VL'):
                        clean_id = clean_id[2:]
                        
                    st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">📌 {title}</a><div class="playlist-meta">Curated by {author}</div></div>', unsafe_allow_html=True)
                    
                    # Use the upgraded iframe component helper
                    embed_youtube_playlist(clean_id)
            except Exception as e:
                st.error(f"Error: {e}")

elif nav_option == "🔍 Search Tracks/Movies":
    st.markdown("<h1 style='font-size: 32px; font-weight: 800; margin-bottom: 20px;'>🔍 Search Tracks & Movies</h1>", unsafe_allow_html=True)
    search_term = st.text_input("Search for songs or movies...", key="track_input", placeholder="What do you want to listen to?")
    
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
    st.markdown("<h1 style='font-size: 32px; font-weight: 800; margin-bottom: 20px;'>🧑‍🎤 Artist Profiles</h1>", unsafe_allow_html=True)
    artist_term = st.text_input("Search for an artist...", key="artist_input", placeholder="Enter artist name...")
    
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
    st.markdown("<h1 style='font-size: 32px; font-weight: 800; margin-bottom: 20px;'>🔥 Hot Hits India</h1>", unsafe_allow_html=True)
    
    languages = {
        "Hindi / Bollywood": "Trending Music Hindi",
        "Punjabi": "Trending Music Punjabi",
        "Tamil": "Trending Music Tamil",
        "Telugu": "Trending Music Telugu",
        "Marathi": "Trending Music Marathi",
        "Kannada": "Trending Music Kannada",
        "Malayalam": "Trending Music Malayalam",
        "Bhojpuri": "Trending Music Bhojpuri"
    }
    
    selected_lang = st.selectbox("Select Language Market", list(languages.keys()))
    
    if st.button("Play Chart", key="trend_btn"):
        try:
            trend_results = yt.search(languages[selected_lang], filter="playlists", limit=1)
            if trend_results:
                playlist = trend_results[0]
                clean_id = playlist.get('browseId')
                
                if clean_id.startswith('VL'):
                    clean_id = clean_id[2:]
                
                st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">🔊 Hot Hits {selected_lang}</a></div>', unsafe_allow_html=True)
                
                # Use the upgraded iframe component helper
                embed_youtube_playlist(clean_id)
            else:
                st.info("Chart parsing unavailable right now.")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
