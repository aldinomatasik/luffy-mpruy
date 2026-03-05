import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️", layout="centered")

# --- 2. CSS MAGIC (MOBILE APP STYLE) ---
st.markdown("""
<style>
/* Background Full Gambar Luffy Gear 5 */
.stApp {
    background-image: url("https://wallpapercave.com/wp/wp12204555.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Overlay Gelap biar chat kebaca */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Gelap transparan */
    z-index: -1;
}

/* Font ala Anime */
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

.p-title {
    color: #ffcc00; /* Warna kuning emas */
    text-shadow: 3px 3px #ff0000; /* Shadow merah */
    text-align: center;
    font-family: 'Luckiest Guy', cursive;
    font-size: 50px !important;
}

/* Styling Bubble Chat ala Image Reference */
[data-testid="stChatMessage"] {
    border-radius: 15px !important;
    padding: 10px 15px !important;
    margin-bottom: 10px !important;
    max-width: 85%;
}

/* Bubble Chat User (Mirip ungu di gambar Ace) */
[data-testid="stChatMessage"]:nth-of-type(odd) {
    background-color: rgba(123, 104, 238, 0.8) !important; /* Ungu transparan */
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3);
    float: right;
    clear: both;
}

/* Bubble Chat Luffy (Merah Neon) */
[data-testid="stChatMessage"]:nth-of-type(even) {
    background-color: rgba(255, 69, 0, 0.8) !important; /* Oranye/Merah transparan */
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3);
    float: left;
    clear: both;
}

/* Sembunyikan Header Streamlit */
header {visibility: hidden;}
.stDeployButton {display:none;}

/* Styling Input Chat di bawah */
.stChatInputContainer {
    padding-bottom: 20px !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# Judul (Kayak nama 'Zayne' di gambar Ace)
st.markdown('<h1 class="p-title">🏴‍☠️ KAPTEN LUFFY</h1>', unsafe_allow_html=True)

# --- 3. PASANG API KEY ---
API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
genai.configure(api_key=API_KEY)

instruction = (
    "Kamu adalah Monkey D. Luffy. Bicara sangat semangat, panggil 'Nakama', "
    "ketawa 'Shishishi!', pake bahasa santai (gw/lu), dan hobi makan DAGING!"
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. TAMPILKAN CHAT ---
LUFFY_AVATAR = "https://i.pinimg.com/originals/e4/20/7b/e4207b98d363768f564f260195543c72.png"

for message in st.session_state.messages:
    avatar = LUFFY_AVATAR if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f"**{message['content']}**")

# --- 5. INPUT DI BAWAH (MIC & TEKS) ---
st.write("---")
col_mic, col_text = st.columns([1, 4])

with col_mic:
    audio_input = mic_recorder(
        start_prompt="🎤",
        stop_prompt="🍖",
        key='recorder'
    )

with col_text:
    query = st.chat_input("Kirim pesan ke Kapten...")

# --- 6. LOGIKA BALASAN ---
if audio_input:
    with st.spinner("..."):
        response = model.generate_content([
            "Balas sebagai Luffy!",
            {"mime_type": "audio/wav", "data": audio_input['bytes']}
        ])
        st.session_state.messages.append({"role": "user", "content": "🎤 [Pesan Suara]"})
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

elif query:
    st.session_state.messages.append({"role": "user", "content": query})
    response = model.generate_content(query)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()
