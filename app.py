import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. SETTING HALAMAN ---
st.set_page_config(
    page_title="Luffy AI - Nakama Chat",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS MAGIC (ANIME STYLE - FLEKSIBEL & CANTIK) ---
st.markdown("""
<style>
/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');

/* Remove default styling */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    overflow: hidden;
}

[data-testid="stAppViewContainer"] {
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(239, 68, 68, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(251, 191, 36, 0.05) 0%, transparent 50%);
    background-attachment: fixed;
}

/* Header Styling */
.header-container {
    background: linear-gradient(90deg, rgba(120, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.3) 50%, rgba(120, 0, 0, 0.2) 100%);
    border-bottom: 2px solid rgba(239, 68, 68, 0.3);
    padding: 20px;
    border-radius: 0 0 20px 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15);
    animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
    from {
        transform: translateY(-30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Title */
.p-title {
    color: #fbbf24;
    text-shadow: 
        3px 3px 0px #ef4444,
        6px 6px 0px rgba(0, 0, 0, 0.5);
    text-align: center;
    font-family: 'Luckiest Guy', cursive;
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 2px;
    margin: 0;
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { text-shadow: 3px 3px 0px #f87171, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 30px rgba(239, 68, 68, 0.5); }
}

.subtitle {
    color: #fca5a5;
    text-align: center;
    font-size: 13px;
    margin-top: 5px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Chat Container */
.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 200px);
    gap: 12px;
    padding: 20px;
    overflow-y: auto;
    background-image: 
        url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(239,68,68,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="none"/><use href="%23grid"/></pattern></svg>');
    position: relative;
}

.chat-container::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 300px;
    background-image: url('https://pngall.com/wp-content/uploads/14/Luffy-Gear-5-PNG-Free-Download.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: bottom right;
    opacity: 0.15;
    pointer-events: none;
    z-index: 0;
}

/* Custom scrollbar untuk chat */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(251, 191, 36, 0.4));
    border-radius: 4px;
    border: 2px solid transparent;
    background-clip: padding-box;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.6), rgba(251, 191, 36, 0.6));
    background-clip: padding-box;
}

/* Chat Bubbles - User (Purple/Indigo) */
.stChatMessage:has([data-testid="stChatMessageContent"]):nth-child(odd) {
    margin-left: auto !important;
    margin-right: 10px !important;
}

[data-testid="stChatMessage"]:nth-child(odd) {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
    border: 1px solid rgba(168, 85, 247, 0.5) !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    color: white !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    max-width: 75% !important;
    margin-left: auto !important;
    animation: slideInRight 0.4s ease-out;
}

/* Chat Bubbles - Assistant (Red/Orange Luffy) */
[data-testid="stChatMessage"]:nth-child(even) {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(249, 115, 22, 0.8)) !important;
    border: 1px solid rgba(239, 68, 68, 0.5) !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    color: white !important;
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3) !important;
    max-width: 75% !important;
    margin-right: auto !important;
    animation: slideInLeft 0.4s ease-out;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Sembunyikan elemen default Streamlit */
header {
    visibility: hidden !important;
    display: none !important;
}

.stDeployButton {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    display: none !important;
}

/* Input Area Styling */
.stChatInputContainer {
    background: transparent !important;
    border: none !important;
    padding: 15px 20px 30px 20px !important;
    position: relative;
}

.stChatInputContainer input {
    background: rgba(55, 65, 81, 0.6) !important;
    border: 2px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 25px !important;
    color: white !important;
    padding: 12px 18px !important;
    font-size: 15px !important;
    font-family: inherit !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
}

.stChatInputContainer input:focus {
    background: rgba(55, 65, 81, 0.8) !important;
    border-color: rgba(239, 68, 68, 0.6) !important;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.3) !important;
}

.stChatInputContainer input::placeholder {
    color: rgba(200, 200, 200, 0.6) !important;
}

/* Icon buttons styling */
button[kind="primary"] {
    background: linear-gradient(90deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 20px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

button[kind="primary"]:hover {
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.5) !important;
    transform: scale(1.05) !important;
}

/* Responsiveness */
@media (max-width: 768px) {
    .p-title {
        font-size: 36px;
    }

    [data-testid="stChatMessage"]:nth-child(odd),
    [data-testid="stChatMessage"]:nth-child(even) {
        max-width: 90% !important;
    }

    .chat-container {
        height: calc(100vh - 180px);
    }
}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
st.markdown("""
<div class="header-container">
    <h1 class="p-title">🏴‍☠️ KAPTEN LUFFY</h1>
    <p class="subtitle">GEAR 5 MODE • NAKAMA CHAT</p>
</div>
""", unsafe_allow_html=True)

# --- 4. SETUP API KEY (GUNAKAN ENVIRONMENT VARIABLE) ---
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U")
genai.configure(api_key=API_KEY)

system_instruction = (
    "Kamu adalah Monkey D. Luffy dari One Piece. Bicara sangat energik dan antusias, "
    "sering memanggil orang sebagai 'nakama', ketawa 'Shishishi!', pakai bahasa santai (gw/lu/gue/elo), "
    "dan jangan lupa obsesi gw sama DAGING! Respon pendek-pendek tapi penuh energi. "
    "Percaya pada persahabatan dan petualangan!"
)

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# --- 5. INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Yo! Gw Luffy! Siapa nama lu, nakama? Kita bisa petualangan bareng! 🏴‍☠️"
        }
    ]

# --- 6. DISPLAY CHAT ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

LUFFY_AVATAR = "🏴‍☠️"
USER_AVATAR = "👤"

for message in st.session_state.messages:
    avatar = LUFFY_AVATAR if message["role"] == "assistant" else USER_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(f"**{message['content']}**")

st.markdown('</div>', unsafe_allow_html=True)

# --- 7. INPUT HANDLING ---
col_input = st.columns([1])[0]

with col_input:
    user_input = st.chat_input(
        "Kirim pesan ke Kapten Luffy...",
        key="chat_input"
    )

    if user_input:
        # Tambah user message ke history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Generate response dari Gemini
        try:
            response = model.generate_content(user_input)
            
            # Tambah assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Shishishi! Ada error nih: {str(e)}"
            })

        st.rerun()

# Optional: Mic input (uncomment jika sudah install streamlit_mic_recorder)
# with col_mic:
#     audio_input = mic_recorder(
#         start_prompt="🎤 REC",
#         stop_prompt="⏹️ STOP",
#         key='recorder'
#     )
#
#     if audio_input:
#         st.session_state.messages.append({
#             "role": "user",
#             "content": "🎤 [Pesan Suara]"
#         })
#
#         response = model.generate_content([
#             "Balas sebagai Luffy!",
#             {"mime_type": "audio/wav", "data": audio_input['bytes']}
#         ])
#
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response.text
#         })
#
#         st.rerun()
