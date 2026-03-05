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
@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy:wght@400&display=swap');

body, html { margin: 0; padding: 0; height: 100vh; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f1e 0%, #1a0f2e 50%, #0f1a1a 100%) !important;
    padding: 0 !important;
}

[data-testid="stDecoration"] { display: none !important; }
header { display: none !important; }
footer { display: none !important; }

[data-testid="stMain"] { padding: 0 !important; }

.stChatMessage { background: transparent !important; padding: 0 !important; margin: 8px 0 !important; }

.stChatMessageContent {
    border-radius: 20px !important;
    padding: 12px 16px !important;
    border: 1px solid rgba(200, 200, 200, 0.2) !important;
    font-size: 15px !important;
}

.stChatMessage:nth-child(odd) .stChatMessageContent {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
    color: white !important;
    margin-left: auto !important;
    width: fit-content !important;
    max-width: 75% !important;
}

.stChatMessage:nth-child(even) .stChatMessageContent {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.8), rgba(249, 115, 22, 0.8)) !important;
    color: white !important;
    margin-right: auto !important;
    width: fit-content !important;
    max-width: 75% !important;
}

[data-testid="stChatMessageContainer"] {
    background: transparent !important;
    padding: 20px !important;
}

.stChatInput {
    margin-top: 20px !important;
    padding: 15px 20px !important;
    background: rgba(0, 0, 0, 0.3) !important;
    border-top: 1px solid rgba(239, 68, 68, 0.2) !important;
}

.stChatInputContainer input {
    background: rgba(55, 65, 81, 0.6) !important;
    border: 2px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 25px !important;
    color: white !important;
    padding: 12px 18px !important;
    backdrop-filter: blur(10px) !important;
}

.stChatInputContainer input:focus {
    background: rgba(55, 65, 81, 0.8) !important;
    border-color: rgba(239, 68, 68, 0.6) !important;
}

.stChatInputContainer input::placeholder {
    color: rgba(200, 200, 200, 0.6) !important;
}

button {
    background: linear-gradient(90deg, #ef4444, #f97316) !important;
    border: none !important;
    border-radius: 25px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    height: auto !important;
}

button:hover {
    box-shadow: 0 0 25px rgba(239, 68, 68, 0.5) !important;
    transform: scale(1.05) !important;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(239, 68, 68, 0.4), rgba(251, 191, 36, 0.4));
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, rgba(120,0,0,0.4) 0%, rgba(0,0,0,0.3) 50%, rgba(120,0,0,0.2) 100%); border-bottom: 2px solid rgba(239,68,68,0.3); backdrop-filter: blur(10px);">
    <h1 style="font-family: 'Luckiest Guy', cursive; font-size: 48px; color: #fbbf24; text-shadow: 3px 3px 0px #ef4444, 6px 6px 0px rgba(0,0,0,0.5); margin: 0;">🏴‍☠️ KAPTEN LUFFY</h1>
    <p style="color: #fca5a5; font-size: 13px; margin: 5px 0 0 0; letter-spacing: 1px;">GEAR 5 MODE • NAKAMA CHAT</p>
</div>
""", unsafe_allow_html=True)

API_KEY = "AIzaSyC9YzN9A8fMoEhnx1wdrfdSf2JWozvv_9U"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Yo! Gw Luffy! Siapa nama lu, nakama? 🏴‍☠️ Kita petualangan bareng!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

col_mic, col_input = st.columns([1, 5], gap="small")

with col_mic:
    audio_input = mic_recorder(
        start_prompt="🎤",
        stop_prompt="🍖",
        key='recorder',
        use_container_width=True
    )

with col_input:
    user_input = st.chat_input("Kirim pesan ke Kapten...")

if audio_input:
    with st.spinner("Shishishi... lagi dengar..."):
        try:
            st.session_state.messages.append({
                "role": "user",
                "content": "🎤 [Pesan Suara]"
            })
            
            response = model.generate_content([
                "Balas sebagai Monkey D. Luffy dari One Piece yang sangat energik, santai, dan obsesi daging!",
                {"mime_type": "audio/wav", "data": audio_input['bytes']}
            ])
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

elif user_input:
    with st.spinner("Shishishi... lagi mikir..."):
        try:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            prompt = f"""Kamu adalah Monkey D. Luffy dari One Piece. Karakteristik:
- Sangat energik dan antusias
- Sering panggil orang 'nakama'
- Ketawa 'Shishishi!'
- Pakai bahasa santai (gw, lu, gue, elo)
- Obsesi sama DAGING!
- Respon pendek-pendek tapi penuh energi
- Percaya pada persahabatan dan petualangan

User: {user_input}

Balas sebagai Luffy!"""
            
            response = model.generate_content(prompt)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
            
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if st.session_state.messages:
                st.session_state.messages.pop()
