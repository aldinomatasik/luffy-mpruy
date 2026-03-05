import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️", layout="wide")

# --- 2. BUMBU CSS MAGIC (DESAIN BARU) ---
st.markdown("""
<style>
/* Background Gradasi Laut Malam */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: white;
}

/* Font ala Anime */
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

.p-title {
    color: #ff4b4b;
    text-shadow: 4px 4px #000;
    text-align: center;
    font-family: 'Luckiest Guy', cursive;
    font-size: 65px !important;
    margin-top: -20px;
}

/* Styling Bubble Chat User */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 15px;
    margin-bottom: 10px;
}

/* Styling Bubble Chat Luffy (Merah) */
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: rgba(255, 75, 75, 0.2) !important;
    border: 1px solid #ff4b4b;
}

/* Menghilangkan header default streamlit */
header {visibility: hidden;}

/* Tombol Mic Styling */
.stButton>button {
    background-color: #ff4b4b !important;
    color: white !important;
    border-radius: 50px !important;
}
</style>
""", unsafe_allow_html=True)

# Judul Utama
st.markdown('<h1 class="p-title">🍖 KAPTEN LUFFY AI 🏴‍☠️</h1>', unsafe_allow_html=True)

# --- 3. PASANG API KEY ---
API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
genai.configure(api_key=API_KEY)

instruction = (
    "Kamu adalah Monkey D. Luffy dari One Piece. "
    "Bicara sangat semangat, panggil user 'Nakama', ketawa 'Shishishi!', "
    "gunakan bahasa Indonesia santai (gw/lu), dan selalu lapar DAGING!"
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. TAMPILKAN CHAT ---
LUFFY_AVATAR = "https://i.pinimg.com/originals/e4/20/7b/e4207b98d363768f564f260195543c72.png"

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        avatar = LUFFY_AVATAR if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(f"**{message['content']}**")

# --- 5. INPUT DI BAWAH ---
st.write("---")
cols = st.columns([1, 4])

with cols[0]:
    st.write("🎙️ Klik & Ngomong:")
    audio_input = mic_recorder(
        start_prompt="REKAM 🎤",
        stop_prompt="KIRIM 🍖",
        key='recorder'
    )

with cols[1]:
    query = st.chat_input("Ngobrol apa kita hari ini, Nakama?")

# --- 6. LOGIKA BALASAN ---
if audio_input:
    with st.spinner("Luffy lagi dengerin..."):
        response = model.generate_content([
            "Balas sebagai Luffy!",
            {"mime_type": "audio/wav", "data": audio_input['bytes']}
        ])
        st.session_state.messages.append({"role": "user", "content": "🎤 [Pesan Suara]"})
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

elif query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.spinner("Luffy lagi lari nyari daging..."):
        response = model.generate_content(query)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()
