import streamlit as st
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit interface
st.title("Google Gemini API Vision and Video Processor")
st.write("Upload an image or video and ask questions, summarize, or perform content analysis.")

# Initialize session state for file references
if "uploaded_file_reference" not in st.session_state:
    st.session_state["uploaded_file_reference"] = None

# File upload (images and videos)
uploaded_file = st.file_uploader("Choose an image (JPEG, PNG) or a video (MP4, AVI, etc.)...", type=["jpeg", "png", "mp4", "avi", "mpeg", "mov", "webm"])

# Sidebar options
st.sidebar.title("File Operations")
bounding_box_request = st.sidebar.checkbox("Request Bounding Box for Image")
video_transcription = st.sidebar.checkbox("Request Video Transcription with Timestamps")
video_summary = st.sidebar.checkbox("Request Video Summary and Quiz")

# Handle file upload
if uploaded_file is not None:
    if st.session_state["uploaded_file_reference"] is None:
        mime_type = uploaded_file.type
        with st.spinner("Uploading file to Gemini API..."):
            # Upload the image or video to Gemini API with the correct mime_type
            uploaded_gemini_file = genai.upload_file(uploaded_file, mime_type=mime_type)
            st.session_state["uploaded_file_reference"] = uploaded_gemini_file
        st.success("File uploaded successfully.")
    else:
        st.info("File is already uploaded. You can now ask questions or request analysis.")

# Prompt input (works independently of file upload)
user_prompt = st.text_input("Ask a question about the image/video or request an analysis:")

# Generate content or perform analysis
if user_prompt and st.button("Generate Response"):
    file_reference = st.session_state["uploaded_file_reference"]

    if file_reference is not None:
        # Handle image-related prompts
        if "image" in file_reference.mime_type:
            if bounding_box_request:
                # Request bounding box for an object in the image
                response = model.generate_content([file_reference, user_prompt])
                st.success("Bounding Box Coordinates:")
                st.write(response.text)
            else:
                # Normal content generation for images
                response = model.generate_content([file_reference, user_prompt])
                st.success("Response received:")
                st.write(response.text)
        
        # Handle video-related prompts
        elif "video" in file_reference.mime_type:
            with st.spinner("Processing video..."):
                # Check if the file is processed and active
                while file_reference.state.name == "PROCESSING":
                    time.sleep(10)
                    file_reference = genai.get_file(file_reference.name)
                if file_reference.state.name == "FAILED":
                    st.error("Failed to process the video.")
                else:
                    if video_transcription:
                        # Request video transcription with visual descriptions and timestamps
                        transcription_prompt = "Transcribe the audio, giving timestamps. Also provide visual descriptions."
                        response = model.generate_content([file_reference, transcription_prompt], request_options={"timeout": 600})
                        st.success("Video Transcription:")
                        st.write(response.text)
                    elif video_summary:
                        # Request video summary and quiz generation
                        summary_prompt = "Summarize this video. Then create a quiz with answer key based on the information in the video."
                        response = model.generate_content([file_reference, summary_prompt], request_options={"timeout": 600})
                        st.success("Video Summary and Quiz:")
                        st.write(response.text)
                    else:
                        # Normal video content generation
                        response = model.generate_content([file_reference, user_prompt], request_options={"timeout": 600})
                        st.success("Response received:")
                        st.write(response.text)
    else:
        st.warning("Please upload a valid file.")

# Sidebar: List and delete files
if st.sidebar.button("List Files"):
    st.sidebar.write("Files uploaded via API:")
    for f in genai.list_files():
        st.sidebar.write(f"- {f.name}")

if st.sidebar.button("Delete All Files"):
    for f in genai.list_files():
        f.delete()
    st.sidebar.write("All files deleted.")
