import streamlit as st
import os
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Start a chat
if "chat" not in st.session_state:
    st.session_state["chat"] = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )

# Streamlit interface for chat
st.title("Google Gemini API Chat Interface")

# Initialize session state for chat history and generation config
if "history" not in st.session_state:
    st.session_state["history"] = []

if "generation_config" not in st.session_state:
    st.session_state["generation_config"] = {
        "max_output_tokens": 100, 
        "temperature": 1.0
    }

# Function to display chat messages
def display_chat_history():
    for message in st.session_state["history"]:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])

# Function to send message and get response from the model
def send_message(user_input):
    # Add user's message to history
    st.session_state["history"].append({"role": "user", "content": user_input})

    # Send message to the model and get response
    response = st.session_state["chat"].send_message(user_input)

    # Add model's response to history
    st.session_state["history"].append({"role": "assistant", "content": response.text})

# Display chat history once
display_chat_history()

# User input box
if user_input := st.chat_input("Type your message"):
    send_message(user_input)
    display_chat_history()

# Sidebar for generation configuration
st.sidebar.title("Generation Configuration")

# Preserve configuration values in session state
st.session_state["generation_config"]["max_output_tokens"] = st.sidebar.slider(
    "Max Output Tokens", 
    min_value=20, 
    max_value=1000, 
    value=st.session_state["generation_config"]["max_output_tokens"]
)

st.session_state["generation_config"]["temperature"] = st.sidebar.slider(
    "Temperature", 
    min_value=0.0, 
    max_value=2.0, 
    value=st.session_state["generation_config"]["temperature"]
)

# Example of using GenerationConfig
response = model.generate_content(
    "Tell me a story about a magic backpack.",
    generation_config=GenerationConfig(
        max_output_tokens=st.session_state["generation_config"]["max_output_tokens"],
        temperature=st.session_state["generation_config"]["temperature"],
        candidate_count=1,
    )
)

st.sidebar.write("Example response from configured generation:")
st.sidebar.write(response.text)
