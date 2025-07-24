import streamlit as st
import requests

st.set_page_config(page_title="🩺 HealthChatbot by Shehroz", layout="centered")

st.title("🩺 HealthChatbot - Ask Your Medical Questions")
st.write("This AI chatbot answers your general medical queries. For emergencies, consult a real doctor.")

# Input box
user_input = st.text_input("You:", placeholder="Type your health-related question here...")

# Securely load API key from Streamlit secrets
API_KEY = st.secrets["OPENROUTER_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://theartificiallab.com",  # optional
    "X-Title": "HealthChatbot"
}

# Function to send message to OpenRouter
def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}\n{response.text}"

# Handle user input
if user_input:
    with st.spinner("Thinking..."):
        result = ask_openrouter(user_input)
        st.success(result)
