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
st.title("Google Gemini API Image Tester")
st.write("Upload an image and ask a question about it.")

# Image upload
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Question input
image_question = st.text_input("Enter your question about the image:", "Tell me about this instrument")

# Generate response
if st.button("Generate Response") and uploaded_image is not None:
    # Open the uploaded image
    image = Image.open(uploaded_image)
    
    # Generate response using the image and the question
    response = model.generate_content([image_question, image])
    
    st.success("Response received:")
    st.write(response.text)

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_column_width=True)
else:
    st.write("Please upload an image and enter a question.")
