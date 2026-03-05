import streamlit as st
import google.generativeai as genai

# --- SETTING DASHBOARD ---
st.set_page_config(page_title="Luffy AI - Nakama Chat", page_icon="🏴‍☠️")

# --- CSS BIAR KEREN ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍖 LUFFY AI: KAPTEN BAJAK LAUT")

# --- MASUKIN API KEY KAMU DI SINI ---
# Pastikan kamu sudah ganti tulisan di bawah pakai API Key asli kamu!
API_KEY = "MASUKKAN_API_KEY_KAMU_DI_SINI"
genai.configure(api_key=API_KEY)

instruction = "Kamu adalah Luffy dari One Piece. Bicara sangat semangat, panggil user 'Nakama', ketawa 'Shishishi!', dan selalu lapar DAGING!"
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ngobrol apa sama Kapten?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
