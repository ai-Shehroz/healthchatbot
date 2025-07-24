import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot by TheArtificialLab.com")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "sk-or-your-api-key-here"  # Replace with your OpenRouter API key

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        full_response = ""

        # Send request to OpenRouter API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        }

        response = requests.post(API_URL, headers=headers, json=data)
        assistant_reply = response.json()["choices"][0]["message"]["content"]

        full_response += assistant_reply
        msg_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
