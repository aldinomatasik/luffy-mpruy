import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="🏴‍☠️ KAPTEN LUFFY - Nakama Chat",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CUSTOM CSS - FULLY RESPONSIVE =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy:wght@400&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100vh;
    overflow: hidden !important;
}

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    background-attachment: fixed !important;
    height: 100vh !important;
    width: 100vw !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
    gap: 0 !important;
}

[data-testid="stDecoration"] { display: none !important; }
header { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
#MainMenu { visibility: hidden !important; }

/* Background effects */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(239, 68, 68, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(251, 191, 36, 0.05) 0%, transparent 50%),
        radial-gradient(circle at 50% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stMain"] {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 0 !important;
    width: 100%;
    gap: 0 !important;
}

.block-container {
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
}

/* TITLE - RESPONSIVE */
.title-container {
    text-align: center;
    padding: clamp(15px, 5vw, 25px);
    background: linear-gradient(90deg, rgba(120, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0.3) 50%, rgba(120, 0, 0, 0.2) 100%);
    border-bottom: 2px solid rgba(239, 68, 68, 0.3);
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(239, 68, 68, 0.15);
    animation: slideDown 0.6s ease-out;
    flex-shrink: 0;
    width: 100%;
}

@keyframes slideDown {
    from { transform: translateY(-30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.title-main {
    font-family: 'Luckiest Guy', cursive !important;
    font-size: clamp(28px, 8vw, 52px) !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    color: #fbbf24 !important;
    text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0, 0, 0, 0.5) !important;
    margin: 0 !important;
    animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
    0%, 100% { text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { text-shadow: 3px 3px 0px #f87171, 6px 6px 0px rgba(0, 0, 0, 0.5), 0 0 30px rgba(239, 68, 68, 0.5); }
}

.title-subtitle {
    color: #fca5a5 !important;
    font-size: clamp(10px, 2.5vw, 13px) !important;
    margin-top: clamp(3px, 1vw, 8px) !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: clamp(4px, 1vw, 8px) 0 !important;
    width: 100% !important;
}

[data-testid="stChatMessageContent"] {
    border-radius: 20px !important;
    padding: clamp(8px, 2vw, 16px) !important;
    border: 1px solid !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 20px !important;
    animation: slideIn 0.4s ease-out;
    word-wrap: break-word !important;
    font-size: clamp(12px, 2.5vw, 16px) !important;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* USER MESSAGE */
[data-testid="stChatMessage"]:nth-of-type(odd) {
    display: flex !important;
    justify-content: flex-end !important;
    padding-right: clamp(5px, 3vw, 20px) !important;
}

[data-testid="stChatMessage"]:nth-of-type(odd) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
    border-color: rgba(168, 85, 247, 0.5) !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3) !important;
    color: white !important;
    max-width: min(85%, 600px) !important;
}

/* ASSISTANT MESSAGE */
[data-testid="stChatMessage"]:nth-of-type(even) {
    display: flex !important;
    justify-content: flex-start !important;
    padding-left: clamp(5px, 3vw, 20px) !important;
}

[data-testid="stChatMessage"]:nth-of-type(even) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(249, 115, 22, 0.8)) !important;
    border-color: rgba(239, 68, 68, 0.5) !important;
    box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3) !important;
    color: white !important;
    max-width: min(85%, 600px) !important;
}

/* CHAT CONTAINER */
[data-testid="stChatMessageContainer"] {
    background: transparent !important;
    position: relative !important;
    flex: 1 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: clamp(10px, 3vw, 30px) !important;
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
}

/* Luffy background */
[data-testid="stChatMessageContainer"]::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    width: clamp(100px, 20vw, 350px);
    height: clamp(100px, 20vw, 350px);
    background-image: url('https://pngall.com/wp-content/uploads/14/Luffy-Gear-5-PNG-Free-Download.png');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: bottom right;
    opacity: 0.1;
    pointer-events: none;
}

/* INPUT SECTION */
.input-section {
    flex-shrink: 0;
    padding: clamp(10px, 2vw, 20px);
    background: linear-gradient(to top, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.2));
    border-top: 1px solid rgba(239, 68, 68, 0.2);
    width: 100%;
    gap: clamp(8px, 2vw, 12px) !important;
    display: flex !important;
    align-items: flex-end !important;
    justify-content: center !important;
}

.stChatInputContainer {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    flex: 1 !important;
    min-width: 200px !important;
}

.stChatInputContainer input {
    background: rgba(55, 65, 81, 0.6) !important;
    border: 2px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 25px !important;
    color: white !important;
    padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 18px) !important;
    font-size: clamp(12px, 2vw, 15px) !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    width: 100% !important;
    height: 44px !important;
}

.stChatInputContainer input:focus {
    background: rgba(55, 65, 81, 0.8) !important;
    border-color: rgba(239, 68, 68, 0.6) !important;
    box-shadow: 0 0 20px rgba(239, 68, 68, 0.3) !important;
}

.stChatInputContainer input::placeholder {
    color: rgba(200, 200, 200, 0.6) !important;
}

/* COLUMNS */
[data-testid="stHorizontalBlock"] {
    gap: clamp(8px, 2vw, 12px) !important;
    align-items: flex-end !important;
    width: 100% !important;
}

[data-testid="stColumn"] {
    padding: 0 !important;
}

/* BUTTONS */
button {
    background: linear-gradient(90deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 25px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: clamp(8px, 1.5vw, 12px) clamp(10px, 2vw, 16px) !important;
    transition: all 0.3s ease !important;
    height: 44px !important;
    min-width: 44px !important;
    flex-shrink: 0 !important;
    font-size: clamp(12px, 1.5vw, 14px) !important;
}

button:hover {
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.5) !important;
    transform: scale(1.05) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(251, 191, 36, 0.4));
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.6), rgba(251, 191, 36, 0.6));
}

/* TABLET */
@media (max-width: 1024px) {
    [data-testid="stChatMessageContent"] {
        max-width: 75% !important;
    }
}

/* MOBILE */
@media (max-width: 768px) {
    [data-testid="stChatMessageContent"] {
        max-width: 85% !important;
    }

    .input-section {
        gap: clamp(6px, 1.5vw, 10px) !important;
    }

    button {
        height: 40px !important;
        min-width: 40px !important;
    }
}

/* SMALL PHONE */
@media (max-width: 480px) {
    .title-main {
        text-shadow: 2px 2px 0px #ef4444, 4px 4px 0px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stChatMessageContent"] {
        max-width: 92% !important;
        border-radius: 15px !important;
    }

    .input-section {
        padding: clamp(8px, 1.5vw, 12px);
    }

    button {
        padding: 8px 10px !important;
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
API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
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
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col_mic, col_input = st.columns([1, 4], gap="small")

with col_mic:
    audio_input = mic_recorder(
        start_prompt="🎤",
        stop_prompt="🍖",
        key='recorder',
        use_container_width=True
    )

with col_input:
    user_input = st.chat_input("Kirim pesan ke Kapten...")

st.markdown('</div>', unsafe_allow_html=True)

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
