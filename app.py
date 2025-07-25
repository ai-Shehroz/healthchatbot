import streamlit as st
import requests
import os
import tempfile
import speech_recognition as sr
import pyttsx3

# ------------------ SETTINGS ------------------
st.set_page_config(page_title="Health Chatbot", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; color: #00FFAA;'>🤖 Health Chatbot - Developed by Shehroz Khan Rind</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ------------------ VOICE ENGINE ------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ------------------ API ------------------
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ SPEECH-TO-TEXT ------------------
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "API unavailable."

# ------------------ TEXT-TO-SPEECH ------------------
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# ------------------ CHATBOT FUNCTION ------------------
def ask_ai(message_list):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": message_list
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ------------------ CHAT UI ------------------
st.markdown("""
    <style>
    .stTextInput, .stButton, .stChatMessage {color: white !important;}
    .stTextInput>div>input {background-color: #1e1e1e; color: white;}
    .block-container {background-color: #111111;}
    </style>
    """, unsafe_allow_html=True)

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ VOICE INPUT ------------------
with st.sidebar:
    st.markdown("🎙️ **Voice Input**")
    audio_file = st.file_uploader("Upload voice message (.wav)", type=["wav"])
    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(audio_file.read())
            audio_path = tmp_file.name
        user_input = transcribe_audio(audio_path)
        st.success(f"You said: {user_input}")
    else:
        user_input = st.chat_input("Type your message here...")

# ------------------ PROCESS INPUT ------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = ask_ai(st.session_state.messages)
        st.markdown(response)
        speak_text(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
