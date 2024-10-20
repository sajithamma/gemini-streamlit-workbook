import streamlit as st
import os
import google.generativeai as genai
from io import BytesIO
from dotenv import load_dotenv
from streamlit_mic_recorder import mic_recorder

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit interface
st.title("Google Gemini API Audio Processor")
st.write("Upload or record an audio file and ask questions, summarize, or transcribe the content.")

# Initialize session state for file references
if "uploaded_file_reference" not in st.session_state:
    st.session_state["uploaded_file_reference"] = None
if "recorded_audio_data" not in st.session_state:
    st.session_state["recorded_audio_data"] = None

# Sidebar options for audio operations
st.sidebar.title("Audio Operations")
audio_transcription = st.sidebar.checkbox("Request Transcription")
audio_summary = st.sidebar.checkbox("Request Summary")

# Option to either upload or record audio
audio_source = st.radio("Choose audio input method", ("Upload Audio", "Record Audio"))

# Function to handle file upload
def upload_audio(file, mime_type):
    with st.spinner("Uploading audio file to Gemini API..."):
        uploaded_gemini_file = genai.upload_file(file, mime_type=mime_type)
        st.session_state["uploaded_file_reference"] = uploaded_gemini_file
    st.success("Audio file uploaded successfully.")

# Callback function for microphone recording
def record_callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output["bytes"]
        st.audio(audio_bytes)

        # Use BytesIO to convert the audio bytes into a file-like object
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "output.mp3"  # Specify a name for the simulated file

        # Store recorded audio data for inline upload
        st.session_state["recorded_audio_data"] = {
            "mime_type": "audio/mp3",
            "data": audio_bytes
        }
        st.success("Audio recorded successfully.")

# If uploading audio
if audio_source == "Upload Audio":
    uploaded_file = st.file_uploader("Choose an audio file (WAV, MP3, AAC, etc.)...", type=["wav", "mp3", "aiff", "aac", "ogg", "flac"])
    if uploaded_file is not None:
        upload_audio(uploaded_file, uploaded_file.type)

# If recording audio
elif audio_source == "Record Audio":
    st.write("Click the button below to start recording.")
    
    # Microphone recording component
    mic_recorder(key="my_recorder", callback=record_callback)

# Prompt input (works independently of file upload)
user_prompt = st.text_input("Ask a question about the audio file or request an analysis:")

# Generate content or perform analysis
if user_prompt and st.button("Generate Response"):
    if st.session_state["recorded_audio_data"]:
        # Use inline data method for recorded audio
        audio_data = st.session_state["recorded_audio_data"]
        response = model.generate_content([
            user_prompt,
            {
                "mime_type": "audio/mp3",
                "data": audio_data["data"]
            }
        ])
        st.success("Response received from recorded audio:")
        st.write(response.text)
    elif st.session_state["uploaded_file_reference"]:
        file_reference = st.session_state["uploaded_file_reference"]
        with st.spinner("Processing audio..."):
            if audio_transcription:
                transcription_prompt = "Please transcribe the audio content."
                response = model.generate_content([file_reference, transcription_prompt])
                st.success("Audio Transcription:")
                st.write(response.text)
            elif audio_summary:
                summary_prompt = "Please summarize the audio content."
                response = model.generate_content([file_reference, summary_prompt])
                st.success("Audio Summary:")
                st.write(response.text)
            else:
                response = model.generate_content([file_reference, user_prompt])
                st.success("Response received:")
                st.write(response.text)
    else:
        st.warning("Please upload or record an audio file.")

# Sidebar: List and delete files
if st.sidebar.button("List Files"):
    st.sidebar.write("Files uploaded via API:")
    for f in genai.list_files():
        st.sidebar.write(f"- {f.name}")

if st.sidebar.button("Delete All Files"):
    for f in genai.list_files():
        f.delete()
    st.sidebar.write("All files deleted.")
