import streamlit as st
from ytmusicapi import YTMusic
from textblob import TextBlob

# Initialize YouTube Music Client
@st.cache_resource
def get_yt_client():
    return YTMusic()

yt = get_yt_client()

# 1. Page Configuration & Spotify-like Dark Theme CSS
st.set_page_config(page_title="Moodify (YT Edition)", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    /* Main app background and text color */
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    
    /* Input field styling */
    .stTextInput input {
        background-color: #242424 !important;
        color: #FFFFFF !important;
        border: 1px solid #3E3E3E !important;
        border-radius: 50px !important;
        padding-left: 20px !important;
    }
    
    /* Red YouTube Music button styling */
    .stButton>button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.04);
        background-color: #CC0000 !important;
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
        color: #FF0000 !important;
        font-size: 18px !important;
        font-weight: bold;
        text-decoration: none;
    }
    .playlist-meta {
        color: #B3B3B3;
        font-size: 14px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Header UI
st.markdown("<h1 style='color: #FF0000; text-align: center;'>🎵 Moodify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B3B3B3;'>Powered completely free by YouTube Music</p>", unsafe_allow_html=True)
st.write("---")

# 3. Input Area
user_input = st.text_input("", placeholder="How are you feeling right now?")

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    submit_button = st.button("Get Music")

# 4. Logic Execution
if submit_button:
    if user_input.strip() == "":
        st.warning("Please enter your mood first!")
    else:
        # Sentiment Analysis
        analysis = TextBlob(user_input)
        polarity = analysis.sentiment.polarity
        
        # Determine search keywords based on sentiment score
        if polarity < -0.1:
            search_query = "sad acoustic rainy day music playlist"
            status_msg = "💎 Finding something reflective and comforting..."
        elif polarity > 0.1:
            search_query = "upbeat high energy party dance music playlist"
            status_msg = "🔥 Finding something to boost the vibes!"
        else:
            search_query = "lofi chill ambient relaxed music playlist"
            status_msg = "☕ Finding a relaxed, mellow soundtrack..."
            
        st.markdown(f"<p style='color: #FF0000; font-weight: bold;'>{status_msg}</p>", unsafe_allow_html=True)
        
        # Fetching playlists from YouTube Music
        try:
            # We filter specifically for community or official playlists matching the mood query
            results = yt.search(search_query, filter="playlists", limit=3)
            
            st.write("") # Spacer
            st.markdown("### 🎧 Curated Playlists for You:")
            
            if not results:
                st.info("No explicit playlists found. Try phrasing your mood slightly differently!")
            
            for playlist in results:
                title = playlist.get('title', 'Mood Mix')
                author = playlist.get('author', 'YouTube Music')
                playlist_id = playlist.get('browseId')
                
                # Format standard web-playable URL
                # YTMusic outputs browseIds starting with 'VL' or standard text formats
                clean_id = playlist_id.replace('VL', '') if playlist_id.startswith('VL') else playlist_id
                web_url = f"https://music.youtube.com/playlist?list={clean_id}"
                embed_url = f"https://www.youtube.com/watch?v={clean_id}" # Used for local player
                
                # Render UI container card
                st.markdown(f"""
                <div class="playlist-card">
                    <a href="{web_url}" target="_blank" class="playlist-title">📌 {title}</a>
                    <div class="playlist-meta">Curated by {author}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Player Embed
                # Streamlit automatically generates a media block if given a valid playlist link format
                st.video(f"https://www.youtube.com/playlist?list={clean_id}")
                st.write("---")
                
        except Exception as e:
            st.error(f"Error fetching music: {e}")
