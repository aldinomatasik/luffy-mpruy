import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="🏴‍☠️ KAPTEN LUFFY - Nakama Chat",
    page_icon="🏴‍☠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== CUSTOM CSS - ANIME STYLE MAXIMAL =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy:wght@400&display=swap');

* {
    margin: 0;
    padding: 0;
}

/* MAIN BACKGROUND */
.main {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    background-attachment: fixed !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    background-attachment: fixed !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

/* Remove default elements */
header {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

.stDeployButton {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

/* Animated background blobs */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(239, 68, 68, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(251, 191, 36, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 50% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* TITLE STYLING */
.title-container {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(90deg, rgba(120, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.3) 50%, rgba(120, 0, 0, 0.2) 100%);
    border-bottom: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: 0 0 20px 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15);
    margin-bottom: 20px;
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

.title-main {
    font-family: 'Luckiest Guy', cursive !important;
    font-size: 52px !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    color: #fbbf24 !important;
    text-shadow: 
        3px 3px 0px #ef4444,
        6px 6px 0px rgba(0, 0, 0, 0.5) !important;
    margin: 0 !important;
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { 
        text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 20px rgba(239, 68, 68, 0.3); 
    }
    50% { 
        text-shadow: 3px 3px 0px #f87171, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 30px rgba(239, 68, 68, 0.5); 
    }
}

.title-subtitle {
    color: #fca5a5 !important;
    font-size: 13px !important;
    margin-top: 8px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}

/* CHAT MESSAGE STYLING */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 8px 0 !important;
}

[data-testid="stChatMessageContent"] {
    border-radius: 20px !important;
    padding: 12px 16px !important;
    border: 1px solid !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 20px !important;
    animation: slideIn 0.4s ease-out;
    word-wrap: break-word !important;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* USER MESSAGE (Purple) */
[data-testid="stChatMessage"]:nth-of-type(odd) {
    text-align: right !important;
    margin-right: 0 !important;
}

[data-testid="stChatMessage"]:nth-of-type(odd) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
    border-color: rgba(168, 85, 247, 0.5) !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    color: white !important;
    display: inline-block !important;
    max-width: 85% !important;
}

/* ASSISTANT MESSAGE (Red/Orange) */
[data-testid="stChatMessage"]:nth-of-type(even) {
    text-align: left !important;
    margin-left: 0 !important;
}

[data-testid="stChatMessage"]:nth-of-type(even) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(249, 115, 22, 0.8)) !important;
    border-color: rgba(239, 68, 68, 0.5) !important;
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3) !important;
    color: white !important;
    display: inline-block !important;
    max-width: 85% !important;
}

/* CHAT CONTAINER */
[data-testid="stChatMessageContainer"] {
    background: transparent !important;
    position: relative;
}

/* Add Luffy background image */
[data-testid="stChatMessageContainer"]::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    width: 350px;
    height: 350px;
    background-image: url('https://pngall.com/wp-content/uploads/14/Luffy-Gear-5-PNG-Free-Download.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: bottom right;
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
}

/* INPUT STYLING */
.stChatInputContainer {
    background: transparent !important;
    border: none !important;
    padding: 15px 20px 30px 20px !important;
    position: relative !important;
    margin-bottom: 0 !important;
}

.stChatInputContainer input {
    background: rgba(55, 65, 81, 0.6) !important;
    border: 2px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 25px !important;
    color: white !important;
    padding: 12px 18px !important;
    font-size: 15px !important;
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

/* BUTTON STYLING */
button {
    background: linear-gradient(90deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 20px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

button:hover {
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.5) !important;
    transform: scale(1.05) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(251, 191, 36, 0.4));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.6), rgba(251, 191, 36, 0.6));
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .title-main {
        font-size: 36px !important;
    }

    [data-testid="stChatMessageContent"] {
        max-width: 90% !important;
    }

    [data-testid="stChatMessageContainer"]::after {
        width: 250px;
        height: 250px;
    }
}

@media (max-width: 480px) {
    .title-container {
        padding: 20px 15px;
    }

    .title-main {
        font-size: 28px !important;
    }

    [data-testid="stChatMessageContent"] {
        max-width: 95% !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
    }

    [data-testid="stChatMessageContainer"]::after {
        width: 200px;
        height: 200px;
    }
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("""
<div class="title-container">
    <h1 class="title-main">🏴‍☠️ KAPTEN LUFFY</h1>
    <p class="title-subtitle">GEAR 5 MODE • NAKAMA CHAT</p>
</div>
""", unsafe_allow_html=True)

# ===== API CONFIGURATION =====
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U")
genai.configure(api_key=API_KEY)

SYSTEM_INSTRUCTION = (
    "Kamu adalah Monkey D. Luffy dari One Piece. Bicara sangat energik dan antusias, "
    "sering memanggil orang sebagai 'nakama', ketawa 'Shishishi!', pakai bahasa santai (gw/lu/gue/elo), "
    "dan jangan lupa obsesi gw sama DAGING! Respon pendek-pendek tapi penuh energi. "
    "Percaya pada persahabatan dan petualangan! Selalu semangat dan positif!"
)

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_INSTRUCTION)

# ===== SESSION STATE =====
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Yo! Gw Luffy! Siapa nama lu, nakama? 🏴‍☠️ Kita bisa petualangan bareng!"
        }
    ]

# ===== DISPLAY MESSAGES =====
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['content']}**")

# ===== INPUT SECTION =====
col_mic, col_text = st.columns([1, 5])

with col_mic:
    audio_input = mic_recorder(
        start_prompt="🎤",
        stop_prompt="🍖",
        key='recorder',
        use_container_width=True
    )

with col_text:
    user_input = st.chat_input("Kirim pesan ke Kapten...")

# ===== HANDLE VOICE INPUT =====
if audio_input:
    with st.spinner("Shishishi... lagi dengar..."):
        try:
            st.session_state.messages.append({
                "role": "user",
                "content": "🎤 [Pesan Suara]"
            })
            
            response = model.generate_content([
                "Balas sebagai Luffy!",
                {"mime_type": "audio/wav", "data": audio_input['bytes']}
            ])
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            
            st.rerun()
        except Exception as e:
            st.error(f"Eh?! Ada error: {str(e)}")

# ===== HANDLE TEXT INPUT =====
elif user_input:
    with st.spinner("Shishishi... lagi mikir..."):
        try:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            response = model.generate_content(user_input)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            
            st.rerun()
        except Exception as e:
            st.error(f"Eh?! Ada error: {str(e)}")
            st.session_state.messages.pop()

# ===== FOOTER =====
st.markdown("""
<div style='text-align: center; margin-top: 30px; padding: 20px; color: rgba(200, 200, 200, 0.6); font-size: 11px;'>
    Made with ❤️ for One Piece fans | Powered by Gemini API
</div>
""", unsafe_allow_html=True)
