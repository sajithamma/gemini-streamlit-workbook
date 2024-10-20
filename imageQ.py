import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit interface
st.title("Google Gemini API Image Tester with Streaming and Chat Message Format")
st.write("Upload an image and ask a question about it. The output will be streamed as a chat message.")

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Question input
image_question = st.text_input("Enter your question about the image:", "Tell me about this instrument")

# Generate response
if st.button("Generate Response") and uploaded_image is not None:
    # Open the uploaded image
    image = Image.open(uploaded_image)

    # Create a chat message container outside the function
    with st.chat_message("assistant"):
        message_container = st.empty()  # Define the container once

    # Function to stream and display the response using st.chat_message and markdown
    def display_streaming_response(response_stream, container):
        message = ""
        for chunk in response_stream:
            message += chunk.text + "\n\n"
            container.markdown(message)  # Update the existing container with markdown

    # Generate the response with streaming enabled
    response_stream = model.generate_content([image_question, image], stream=True)
    
    st.success("Streaming response:")
    display_streaming_response(response_stream, message_container)

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
else:
    st.write("Please upload an image and enter a question.")
