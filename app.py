import streamlit as st
import requests

# App title and header
st.set_page_config(page_title="🩺 Health Assistant Chatbot")
st.title("💬 Health Assistant")
st.caption("Ask your medical questions below:")

# Set up session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI Health Assistant. How can I help you today?"}
    ]

# Function to generate AI response
def generate_response(user_input):
    headers = {
        "Authorization": f"Bearer {st.secrets['openrouter_api_key']}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful and experienced medical assistant."},
            *st.session_state.messages,
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        assistant_message = response.json()["choices"][0]["message"]["content"]
        return assistant_message
    except Exception as e:
        return "❌ Sorry, something went wrong. Please check your API key or internet connection."

# Display conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input and reply
user_prompt = st.chat_input("Type your question...")
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_reply = generate_response(user_prompt)
            st.markdown(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
