import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import io

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️", layout="wide")

# --- 2. URL ASSET GAMBAR BARU (Biar Gak Abu-abu!) ---
# Background: Gambar kru Topi Jerami kumpul
BACKGROUND_URL = "https://w0.peakpx.com/wallpaper/950/749/HD-wallpaper-one-piece-group-wano-arc.jpg"
# Avatar Luffy: Gambar Luffy nyengir
LUFFY_AVATAR_URL = "https://i.pinimg.com/originals/e4/20/7b/e4207b98d363768f564f260195543c72.png"
USER_AVATAR = "👤"

# --- 3. BUMBU CSS MAGIC (Upgrade Tampilan Total!) ---
st.markdown(f"""
    <style>
    /* Background Utama Halaman */
    .stApp {{
        background-image: url("{BACKGROUND_URL}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    
    /* Overlay biar teks kelihatan jelas di atas background rame */
    .stAppOverlay {{
        background-color: rgba(0, 0, 0, 0.4); /* Hitam transparan */
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1;
    }}

    /* Styling Judul Utama ala Anime */
    .p-title {{
        color: #ff0000;
        text-shadow: 5px 5px #000000;
        font-family: 'Luckiest Guy', cursive;
        text-align: center;
        font-size: 70px !important;
        margin-top: -30px;
        margin-bottom: 30px;
    }}
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    
    /* Container untuk Mic & Chat Input di bawah */
    .stChatFloatingInputContainer {{
        background: rgba(0,0,0,0.7) !important;
        border-radius: 25px;
        padding: 15px;
        border: 2px solid #ffcc00;
    }}

    /* Styling Bubble Chat User */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 20px 20px 0px 20px;
        border: 2px solid #ffcc00; /* Warna emas */
        color: black !important;
        margin-left: 50px;
    }}

    /* Styling Bubble Chat Luffy (Assistant) */
    [data-testid="stChatMessage"] + [data-testid="stChatMessage"] {{
        background-color: rgba(255, 75, 75, 0.9) !important; /* Warna merah Luffy */
        border-radius: 20px 20px 20px 0px;
        border: 2px solid #ffffff;
        color: white !important;
        margin-right: 50px;
        margin-left: 0px;
    }}
    
    /* Avatar Image styling biar bulet */
    [data-testid="stChatMessage"] .stAvatar img {{
        border-radius: 50%;
        border: 2px solid white;
    }}

    /* Styling Text Input */
    .stTextInput input {{
        color: white !important;
        background-color: rgba(255,255,255,0.1) !important;
        border-radius: 10px;
    }}
    </style>
    <div class="stAppOverlay"></div>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="p-title">🍖 KAPTEN LUFFY AI 🏴‍☠️</h1>', unsafe_allow_html=True)

# --- 4. KONFIGURASI API GEMINI (Jangan Lupa Diisi!) ---
API_KEY = "MASUKKAN_API_KEY_GEMINI_KAMU" 
if API_KEY == "MASUKKAN_API_KEY_GEMINI_KAMU":
    st.error("Woi Nakama! API Key Gemini-nya belum diisi di kode! Shishishi!")
    st.stop()
genai.configure(api_key=API_KEY)

# Instruksi Kepribadian Luffy
instruction = (
    "Kamu adalah Monkey D. Luffy dari One Piece. "
    "Bicaralah sangat semangat, ceria, polos, panggil user 'Nakama', ketawa 'Shishishi!', "
    "gunakan bahasa Indonesia santai (gw/lu), dan selalu lapar DAGING!"
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. TAMPILKAN RIWAYAT CHAT DENGAN FOTO KARAKTER ---
for message in st.session_state.messages:
    # Pilih Avatar berdasarkan peran
    current_avatar = LUFFY_AVATAR_URL if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=current_avatar):
        st.markdown(message["content"])

# --- 6. CONTAINER INPUT (MIC & TEKS) ---
# Kita taruh mic dan chat input di bagian bawah halaman
input_container = st.container()

with input_container:
    # Label Mic
    st.write("### 🎙️ Ngomong sama Luffy (Tahan untuk Rekam):")
    # Mic Recorder Component
    audio_input = mic_recorder(
        start_prompt="Mulai Ngomong 🎤",
        stop_prompt="Berhenti & Kirim 🍖",
        key='recorder'
    )
    
    # Chat Input Teks biasa
    query = st.chat_input("Atau ketik di sini, Nakama...")

# --- 7. LOGIKA PROSES RESPONS LUFFY ---
luffy_reply = ""

# A. Jika user pake Mic (Voice Input)
if audio_input:
    with st.spinner("Lagi lari sambil dengerin kamu..."):
        # Ambil data audio dan kirim ke Gemini
        audio_bytes = audio_input['bytes']
        # Gemini bisa baca audio langsung!
        response = model.generate_content([
            "Dengarkan audio ini dan balas sebagai Luffy dalam bahasa Indonesia santai!",
            {"mime_type": "audio/wav", "data": audio_bytes}
        ])
        
        # Simpan pesan user (label suara) dan jawaban Luffy
        st.session_state.messages.append({"role": "user", "content": "🎤 [Pesan Suara]"})
        luffy_reply = response.text
        st.session_state.messages.append({"role": "assistant", "content": luffy_reply})
        st.rerun() # Refresh biar chat langsung muncul

# B. Jika user ngetik biasa (Text Input)
elif query:
    # Simpan dan tampilkan chat user
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(query)

    # Dapatkan respons teks dari Luffy (Gemini)
    with st.chat_message("assistant", avatar=LUFFY_AVATAR_URL):
        with st.spinner("Lagi mikir impian jadi Raja Bajak Laut..."):
            response = model.generate_content(query)
            luffy_reply = response.text
            st.markdown(f"### {luffy_reply}")
            
            # --- NEXT: INTEGRASI SUARA KELUAR (Voice Output) DI SINI ---
            # st.audio(suara_luffy_hasil_api)

    # Simpan respons Luffy ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": luffy_reply})
