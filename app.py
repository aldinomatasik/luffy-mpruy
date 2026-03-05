import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️", layout="wide")

# --- 2. TAMPILAN KEREN (ANTI ABU-ABU) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
    }
    .p-title {
        color: #ff4b4b;
        text-shadow: 3px 3px #000;
        text-align: center;
        font-family: 'Comic Sans MS', cursive;
        font-size: 50px !important;
    }
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="p-title">🍖 KAPTEN LUFFY AI 🏴‍☠️</h1>', unsafe_allow_html=True)

# --- 3. PASANG API KEY (OTAK LUFFY) ---
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

# --- 4. TAMPILKAN RIWAYAT CHAT ---
LUFFY_AVATAR = "https://i.pinimg.com/originals/e4/20/7b/e4207b98d363768f564f260195543c72.png"

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(LUFFY_AVATAR if message["role"]=="assistant" else "👤")):
        st.markdown(message["content"])

# --- 5. INPUT (MIC & TEKS) ---
st.write("🎙️ Klik buat ngomong langsung ke Luffy:")
audio_input = mic_recorder(
    start_prompt="Mulai Ngomong 🎤",
    stop_prompt="Berhenti & Kirim 🍖",
    key='recorder'
)

query = st.chat_input("Atau ketik pesan buat Kapten...")

# --- 6. LOGIKA BALASAN ---
if audio_input:
    with st.spinner("Luffy lagi dengerin..."):
        # Gemini dengerin audio langsung
        response = model.generate_content([
            "Balas sebagai Luffy dalam bahasa Indonesia santai!",
            {"mime_type": "audio/wav", "data": audio_input['bytes']}
        ])
        st.session_state.messages.append({"role": "user", "content": "🎤 [Pesan Suara]"})
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

elif query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=LUFFY_AVATAR):
        response = model.generate_content(query)
        st.markdown(f"### {response.text}")
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
