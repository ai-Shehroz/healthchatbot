import streamlit as st
import requests

st.set_page_config(page_title="AI Medical Assistant", page_icon="🩺", layout="wide")

st.markdown("<h1 style='text-align: center;'>🩺 Medical Assistant Chatbot</h1>", unsafe_allow_html=True)
st.markdown("This AI bot helps ask medical questions in a conversational flow. Enter your symptoms or concerns below.")

# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful medical assistant. Ask the user relevant questions to help understand their medical concern, one at a time."},
        {"role": "assistant", "content": "Hello! 👋 I’m your AI medical assistant. What symptoms or health concerns would you like to discuss today?"}
    ]

# Display previous messages
for msg in st.session_state.messages[1:]:  # Skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your response or question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to OpenRouter API
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": st.session_state.messages,
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
