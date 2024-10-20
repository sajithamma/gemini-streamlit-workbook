import streamlit as st
import os
import google.generativeai as genai

#load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit interface
st.title("Google Gemini API Tester")
st.write("Test the Google Gemini API by entering a prompt below.")

# User input
user_input = st.text_area("Enter your prompt here:", "Explain how AI works")

# Generate response
if st.button("Generate Response"):
    response = model.generate_content(user_input)
    st.success("Response received:")
    st.write(response.text)
