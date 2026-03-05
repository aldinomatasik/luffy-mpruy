import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️", layout="wide")

# --- 2. BUMBU CSS MAGIC ---
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.alphacoders.com/131/1316075.jpeg");
        background-size: cover;
        background-attachment: fixed;
    }
    .p-title {
        color: #ff0000;
        text-shadow: 4px 4px #000000;
        font-family: 'Luckiest Guy', cursive;
        text-align: center;
        font-size: 60px !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    
    /* Styling Mic Recorder Button */
    .stCamera { display: none; }
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: rgba(0,0,0,0.6);
        padding: 20px;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="p-title">🍖 KAPTEN LUFFY AI 🏴‍☠️</h1>', unsafe_allow_html=True)

# --- 3. KONFIGURASI API GEMINI ---
API_KEY = "MASUKKAN_API_KEY_GEMINI_KAMU" # GANTI INI!
genai.configure(api_key=API_KEY)

instruction = (
    "Kamu adalah Monkey D. Luffy dari One Piece. "
    "Bicaralah sangat semangat, panggil user 'Nakama', ketawa 'Shishishi!', "
    "gunakan bahasa Indonesia santai (gw/lu), dan selalu lapar DAGING!"
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. FITUR REKAM SUARA (SPEECH-TO-TEXT) ---
st.write("### 🎙️ Ngomong sama Luffy (Tahan untuk Rekam):")
audio_input = mic_recorder(
    start_prompt="Mulai Ngomong 🎤",
    stop_prompt="Berhenti & Kirim 🍖",
    key='recorder'
)

# --- 5. TAMPILKAN CHAT ---
USER_AVATAR = "👤"
LUFFY_AVATAR = "https://i.pinimg.com/originals/e4/20/7b/e4207b98d363768f564f260195543c72.png"

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=(LUFFY_AVATAR if message["role"]=="assistant" else USER_AVATAR)):
        st.markdown(message["content"])

# --- 6. LOGIKA PROSES (SUARA ATAU TEKS) ---
query = st.chat_input("Atau ketik di sini, Nakama...")

# Kalau user pake Mic
if audio_input:
    with st.spinner("Lagi dengerin kamu..."):
        # Gemini bisa baca file audio langsung!
        audio_bytes = audio_input['bytes']
        audio_parts = [{"mime_type": "audio/wav", "data": audio_bytes}]
        
        # Minta Gemini buat transkripsi & jawab sekaligus
        response = model.generate_content([
            "Dengarkan audio ini dan balas sebagai Luffy dalam bahasa Indonesia!",
            audio_parts[0]
        ])
        query = "(Mengirim pesan suara...)" # Label buat di chat
        luffy_reply = response.text
        
        # Simpan ke memori
        st.session_state.messages.append({"role": "user", "content": "🎤 [Pesan Suara]"})
        st.session_state.messages.append({"role": "assistant", "content": luffy_reply})
        st.rerun()

# Kalau user ngetik biasa
if query and query != "(Mengirim pesan suara...)":
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(query)

    with st.chat_message("assistant", avatar=LUFFY_AVATAR):
        response = model.generate_content(query)
        luffy_reply = response.text
        st.markdown(f"### {luffy_reply}")
        
        # --- NEXT: INTEGRASI VOICE OUTPUT DI SINI ---
        # st.audio(suara_hasil_generate)

    st.session_state.messages.append({"role": "assistant", "content": luffy_reply})
