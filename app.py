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
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }

    /* Fixes the white bar at the top */
    header, [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }
    .stTextInput input {
        background-color: #242424 !important;
        color: #FFFFFF !important;
        border: 1px solid #3E3E3E !important;
        border-radius: 50px !important;
        padding-left: 20px !important;
    }
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

# 2. Header UI
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
                    
                    st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">📌 {title}</a><div class="playlist-meta">Curated by {author}</div></div>', unsafe_allow_html=True)
                    st.video(f"https://www.youtube.com/playlist?list={clean_id}")
            except Exception as e:
                st.error(f"Error: {e}")

# ==================== TAB 2: SEARCH TRACKS/MOVIES ====================
with tab2:
    st.subheader("Find Songs by Name or Movie")
    search_term = st.text_input("Enter song title or movie name (e.g., 'Tum Hi Ho' or 'Animal movie'):", key="track_input")
    if st.button("Search Track", key="track_btn"):
        if search_term.strip():
            try:
                songs = yt.search(search_term, filter="songs", limit=3)
                for song in songs:
                    artists = ", ".join([a['name'] for a in song.get('artists', [])])
                    album = song.get('album', {}).get('name', 'Single')
                    video_id = song.get('videoId')
                    
                    st.markdown(f'<div class="playlist-card"><span class="playlist-title">🎵 {song["title"]}</span><div class="playlist-meta">Artist: {artists} | Album/Movie: {album}</div></div>', unsafe_allow_html=True)
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
            except Exception as e:
                st.error(f"Error searching track: {e}")

# ==================== TAB 3: ARTIST SEARCH ====================
with tab3:
    st.subheader("Explore by Artist")
    artist_term = st.text_input("Enter artist name (e.g., 'Arijit Singh', 'Diljit Dosanjh'):", key="artist_input")
    if st.button("Find Artist Tracks", key="artist_btn"):
        if artist_term.strip():
            try:
                # Appends "songs" to query to hit exact top arrays quickly
                artist_songs = yt.search(f"{artist_term} songs", filter="songs", limit=3)
                for song in artist_songs:
                    video_id = song.get('videoId')
                    st.markdown(f'<div class="playlist-card"><span class="playlist-title">🎤 {song["title"]}</span><div class="playlist-meta">Album: {song.get("album", {}).get("name", "Unknown")}</div></div>', unsafe_allow_html=True)
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
            except Exception as e:
                st.error(f"Error fetching artist songs: {e}")

# ==================== TAB 4: INDIAN TRENDING ====================
with tab4:
    st.subheader("🔥 Top Indian Language Trending Hits")
    st.write("Quick access to top trending community music clusters:")
    
    languages = {
        "Hindi / Bollywood": "Hindi Trending Hits New Songs Playlist",
        "Punjabi": "Punjabi Latest Hits Trending Playlist",
        "Tamil": "Tamil Trending New Songs Playlist",
        "Telugu": "Telugu Latest Hits Trending Playlist"
    }
    
    selected_lang = st.selectbox("Choose a language:", list(languages.keys()))
    
    if st.button("Load Trending Playlist", key="trend_btn"):
        try:
            trend_results = yt.search(languages[selected_lang], filter="playlists", limit=1)
            if trend_results:
                playlist = trend_results[0]
                clean_id = playlist.get('browseId').replace('VL', '') if playlist.get('browseId').startswith('VL') else playlist.get('browseId')
                
                st.markdown(f'<div class="playlist-card"><a href="https://music.youtube.com/playlist?list={clean_id}" target="_blank" class="playlist-title">🔥 Trending {selected_lang} Mix</a></div>', unsafe_allow_html=True)
                st.video(f"https://www.youtube.com/playlist?list={clean_id}")
            else:
                st.info("Could not fetch the chart right now. Try again shortly!")
        except Exception as e:
            st.error(f"Error loading charts: {e}")
