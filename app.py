import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="🩺 AI Medical Assistant", page_icon="💊")

# Title and description
st.title("🩺 Medical Assistant Chatbot")
st.markdown("This AI assistant helps answer your medical-related questions and guides you through a conversation to better understand your symptoms.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI medical assistant. Greet the user and start asking about their symptoms like pain, fever, cough, or any health concerns."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Describe your symptoms or ask a health question...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare API request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    try:
        # Send request to OpenRouter
        response = requests.post(url, headers=headers, json=payload)
        assistant_reply = response.json()["choices"][0]["message"]["content"]

        # Show assistant reply
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

        # Save reply to history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    except Exception as e:
        st.error("⚠️ Failed to get response from the medical assistant.")
        st.exception(e)
