import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model with code execution enabled
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools="code_execution"
)

# Streamlit interface
st.title("Gemini Code Interpreter - Chat with Code Execution")
st.write("Ask any coding-related question and let the model generate and run code for you.")

# Initialize session state for chat
if "chat" not in st.session_state:
    st.session_state["chat"] = model.start_chat()

# Function to handle chat and code execution
def send_message_to_model(user_message):
    response = st.session_state["chat"].send_message(user_message)
    return response.text

# User input
user_input = st.text_input("Enter your prompt (e.g., 'Calculate the sum of the first 50 prime numbers'):")

# Display the conversation history
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

for message in st.session_state["conversation"]:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])

# Handle user input
if user_input and st.button("Send"):
    # Add the user input to the conversation
    st.session_state["conversation"].append({"role": "user", "content": user_input})
    
    # Send message to the Gemini model with code execution enabled
    response_text = send_message_to_model(user_input)
    
    # Add the model's response to the conversation
    st.session_state["conversation"].append({"role": "assistant", "content": response_text})
    
    # Display the updated conversation
    for message in st.session_state["conversation"]:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])

# Sidebar for resetting conversation
if st.sidebar.button("Reset Conversation"):
    st.session_state["conversation"] = []
    st.experimental_rerun()
