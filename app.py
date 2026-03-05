import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="🏴‍☠️ KAPTEN LUFFY",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy:wght@400&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100vh; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
}

[data-testid="stDecoration"], header, footer, .stDeployButton, #MainMenu { display: none !important; }

[data-testid="stMain"] { flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 0 !important; }
.block-container { flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 0 !important; width: 100%; }

.title-container {
    text-align: center;
    padding: clamp(15px, 4vw, 25px);
    background: linear-gradient(90deg, rgba(120,0,0,0.4) 0%, rgba(0,0,0,0.3) 50%, rgba(120,0,0,0.2) 100%);
    border-bottom: 2px solid rgba(239,68,68,0.3);
    backdrop-filter: blur(10px);
    flex-shrink: 0;
    width: 100%;
}

.title-main {
    font-family: 'Luckiest Guy', cursive !important;
    font-size: clamp(28px, 8vw, 52px) !important;
    color: #fbbf24 !important;
    text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0,0,0,0.5) !important;
    margin: 0 !important;
}

.title-subtitle {
    color: #fca5a5 !important;
    font-size: clamp(10px, 2.5vw, 13px) !important;
    margin-top: 5px !important;
}

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: clamp(4px, 1vw, 8px) 0 !important;
}

[data-testid="stChatMessageContent"] {
    border-radius: 20px !important;
    padding: clamp(8px, 1.5vw, 14px) !important;
    border: 1px solid !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 20px !important;
    font-size: clamp(12px, 2vw, 15px) !important;
}

[data-testid="stChatMessage"]:nth-of-type(odd) {
    display: flex !important;
    justify-content: flex-end !important;
}

[data-testid="stChatMessage"]:nth-of-type(odd) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.8), rgba(139,92,246,0.8)) !important;
    border-color: rgba(168,85,247,0.5) !important;
    box-shadow: 0 8px 20px rgba(99,102,241,0.3) !important;
    color: white !important;
    max-width: 80% !important;
}

[data-testid="stChatMessage"]:nth-of-type(even) {
    display: flex !important;
    justify-content: flex-start !important;
}

[data-testid="stChatMessage"]:nth-of-type(even) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(239,68,68,0.8), rgba(249,115,22,0.8)) !important;
    border-color: rgba(239,68,68,0.5) !important;
    box-shadow: 0 8px 20px rgba(239,68,68,0.3) !important;
    color: white !important;
    max-width: 80% !important;
}

[data-testid="stChatMessageContainer"] {
    flex: 1 !important;
    overflow-y: auto !important;
    padding: clamp(10px, 2vw, 20px) !important;
}

.input-area {
    flex-shrink: 0;
    padding: clamp(10px, 2vw, 15px);
    background: linear-gradient(to top, rgba(0,0,0,0.5), rgba(0,0,0,0.2));
    border-top: 1px solid rgba(239,68,68,0.2);
    width: 100%;
}

.stChatInputContainer { width: 100%; flex: 1; }
.stChatInputContainer input {
    background: rgba(55,65,81,0.6) !important;
    border: 2px solid rgba(239,68,68,0.3) !important;
    border-radius: 25px !important;
    color: white !important;
    padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 16px) !important;
    font-size: clamp(12px, 1.8vw, 14px) !important;
    backdrop-filter: blur(10px) !important;
}

.stChatInputContainer input:focus {
    background: rgba(55,65,81,0.8) !important;
    border-color: rgba(239,68,68,0.6) !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.3) !important;
}

.stChatInputContainer input::placeholder { color: rgba(200,200,200,0.6) !important; }

button {
    background: linear-gradient(90deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 25px !important;
    color: white !important;
    font-weight: 600 !important;
    height: 44px !important;
    flex-shrink: 0 !important;
}

button:hover {
    box-shadow: 0 0 25px rgba(239,68,68,0.5) !important;
    transform: scale(1.05) !important;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239,68,68,0.4), rgba(251,191,36,0.4));
    border-radius: 4px;
}

@media (max-width: 768px) {
    [data-testid="stChatMessageContent"] { max-width: 85% !important; }
}

@media (max-width: 480px) {
    [data-testid="stChatMessageContent"] { max-width: 90% !important; }
    .title-main { text-shadow: 2px 2px 0px #ef4444, 4px 4px 0px rgba(0,0,0,0.5) !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-container"><h1 class="title-main">🏴‍☠️ KAPTEN LUFFY</h1><p class="title-subtitle">GEAR 5 MODE • NAKAMA CHAT</p></div>', unsafe_allow_html=True)

API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="Kamu adalah Monkey D. Luffy. Bicara energik, panggil nakama, ketawa 'Shishishi!', bahasa santai, obsesi daging. Respon pendek-pendek penuh energi.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Yo! Gw Luffy! Siapa nama lu, nakama? 🏴‍☠️"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['content']}**")

st.markdown('<div class="input-area">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    audio = mic_recorder(start_prompt="🎤", stop_prompt="🍖", key='rec', use_container_width=True)
with col2:
    text = st.chat_input("Kirim pesan...")
st.markdown('</div>', unsafe_allow_html=True)

if audio:
    try:
        st.session_state.messages.append({"role": "user", "content": "🎤 [Voice]"})
        resp = model.generate_content([{"mime_type": "audio/wav", "data": audio['bytes']}])
        st.session_state.messages.append({"role": "assistant", "content": resp.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)[:50]}")

elif text:
    try:
        st.session_state.messages.append({"role": "user", "content": text})
        resp = model.generate_content(text)
        st.session_state.messages.append({"role": "assistant", "content": resp.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)[:50]}")
        st.session_state.messages.pop()
