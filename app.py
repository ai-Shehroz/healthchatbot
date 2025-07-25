import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
import base64

# ---------- Configuration ----------
st.set_page_config(page_title="AI Healthcare Assistant", page_icon="💬", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .stTextInput > div > div > input {
        color: white;
    }
    .stApp {
        background-color: #121212;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- App Header ----------
logo_url = "https://raw.githubusercontent.com/ao-shehroz/healthchatbot/main/logo.png"  # replace with your logo URL if needed
st.markdown(f"<img src='{logo_url}' width='120'>", unsafe_allow_html=True)
st.title("💊 AI Healthcare Assistant")
st.markdown("Ask any health-related question and get instant help.")
st.caption("App developed by Shehroz Khan Rind")

# ---------- API Setup ----------
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "mistralai/mistral-7b-instruct:free"

# ---------- Session State for Chat ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful medical assistant. Provide information, not diagnosis or prescriptions."}
    ]

# ---------- Show Conversation ----------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Voice Input ----------
st.markdown("#### 🎙️ Voice Input (Optional)")
audio = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="⏹ Stop", just_once=True)

user_input = None
if audio:
    st.audio(audio["bytes"], format="audio/wav")
    st.success("You can now type or paste your transcribed query.")
    # You can integrate Whisper API to convert audio to text here

# ---------- Text Input ----------
prompt = st.chat_input("Type your health-related question...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        payload = {
            "model": MODEL,
            "messages": st.session_state.messages
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        result = response.json()

        reply = result["choices"][0]["message"]["content"]
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
