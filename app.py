import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="KAPTEN LUFFY",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Nunito:wght@600;700&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a1a 0%, #150a25 40%, #0a1520 100%) !important;
}

[data-testid="stDecoration"], header, footer { display: none !important; }
[data-testid="stMain"] { padding: 0 !important; }

/* Chat messages */
.stChatMessage { background: transparent !important; padding: 0 !important; margin: 8px 0 !important; }

.stChatMessage:nth-child(odd) .stChatMessageContent {
    background: linear-gradient(135deg, rgba(99,102,241,0.85), rgba(139,92,246,0.85)) !important;
    color: white !important;
    margin-left: auto !important;
    width: fit-content !important;
    max-width: 72% !important;
    border-radius: 20px 20px 4px 20px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
}

.stChatMessage:nth-child(even) .stChatMessageContent {
    background: linear-gradient(135deg, rgba(239,68,68,0.8), rgba(249,115,22,0.8)) !important;
    color: white !important;
    margin-right: auto !important;
    width: fit-content !important;
    max-width: 72% !important;
    border-radius: 20px 20px 20px 4px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(239,68,68,0.3) !important;
}

[data-testid="stChatMessageContainer"] {
    background: transparent !important;
    padding: 20px !important;
}

/* Input area - the key fix: mic sits inside input bar next to send */
[data-testid="stBottom"] {
    background: rgba(10,10,26,0.9) !important;
    border-top: 1px solid rgba(239,68,68,0.2) !important;
    backdrop-filter: blur(20px) !important;
    padding: 10px 16px 16px !important;
}

.stChatInputContainer {
    background: rgba(30,20,50,0.8) !important;
    border: 2px solid rgba(239,68,68,0.35) !important;
    border-radius: 50px !important;
    padding: 4px 4px 4px 16px !important;
    box-shadow: 0 4px 30px rgba(239,68,68,0.15) !important;
}

.stChatInputContainer textarea {
    background: transparent !important;
    border: none !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stChatInputContainer textarea::placeholder { color: rgba(252,165,165,0.5) !important; }

.stChatInputContainer textarea:focus { box-shadow: none !important; border: none !important; }

/* Send button */
.stChatInputContainer button {
    background: linear-gradient(135deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    box-shadow: 0 0 16px rgba(239,68,68,0.4) !important;
}

/* Mic button - compact, placed inline */
.mic-wrapper .stButton > button {
    background: linear-gradient(135deg, rgba(239,68,68,0.3), rgba(249,115,22,0.3)) !important;
    border: 1.5px solid rgba(239,68,68,0.5) !important;
    border-radius: 50% !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    padding: 0 !important;
    font-size: 18px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.mic-wrapper .stButton > button:hover {
    background: linear-gradient(135deg, #ef4444, #f97316) !important;
    box-shadow: 0 0 20px rgba(239,68,68,0.5) !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239,68,68,0.4), rgba(251,191,36,0.4));
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:16px 24px;
     background:linear-gradient(90deg,rgba(120,0,0,.5),rgba(0,0,0,.4),rgba(120,0,0,.3));
     border-bottom:2px solid rgba(239,68,68,.3); backdrop-filter:blur(20px);">
  <h1 style="font-family:'Luckiest Guy',cursive; font-size:clamp(28px,5vw,48px);
      color:#fbbf24; text-shadow:3px 3px 0 #ef4444,6px 6px 0 rgba(0,0,0,.5); margin:0; letter-spacing:2px;">
      🏴‍☠️ KAPTEN LUFFY
  </h1>
  <p style="color:#fca5a5; font-size:11px; margin:4px 0 0; letter-spacing:3px;
     font-family:'Nunito',sans-serif;">⚡ GEAR 5 MODE &bull; NAKAMA CHAT ⚡</p>
</div>
""", unsafe_allow_html=True)

# ── Model setup ──────────────────────────────────────────────────────────────
API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

LUFFY_PROMPT = (
    "Kamu adalah Monkey D. Luffy dari One Piece. "
    "Sangat energik, santai, obsesi daging, panggil orang 'nakama', ketawa 'Shishishi!'. "
    "Balas singkat penuh energi sebagai Luffy! Gunakan bahasa Indonesia santai dan gaul."
)

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Yo! Gw Luffy! Siapa nama lu, nakama? 🏴‍☠️ Kita petualangan bareng!"}
    ]

# ── Render chat ───────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Bottom input row: [mic] [chat_input → send] ───────────────────────────────
# We place the mic recorder INSIDE a narrow column that visually sits
# right next to Streamlit's chat_input via columns trick.
col_mic, col_chat = st.columns([1, 11], gap="small")

with col_mic:
    st.markdown('<div class="mic-wrapper">', unsafe_allow_html=True)
    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="🔴",
        key="recorder",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_chat:
    user_input = st.chat_input("Kirim pesan ke Kapten...")

# ── Handle voice ──────────────────────────────────────────────────────────────
if audio:
    try:
        st.session_state.messages.append({"role": "user", "content": "🎤 [Voice message]"})
        resp = model.generate_content([
            LUFFY_PROMPT + " User kirim voice message, balas semangat!",
            {"mime_type": "audio/wav", "data": audio["bytes"]},
        ])
        st.session_state.messages.append({"role": "assistant", "content": resp.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error audio: {str(e)[:60]}")

# ── Handle text ───────────────────────────────────────────────────────────────
elif user_input:
    try:
        st.session_state.messages.append({"role": "user", "content": user_input})
        prompt = f"{LUFFY_PROMPT}\nUser: {user_input}\nBalas singkat penuh energi sebagai Luffy!"
        resp = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": resp.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)[:60]}")
        st.session_state.messages.pop()
