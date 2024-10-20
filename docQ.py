import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit interface
st.title("Google Gemini API Document Processor")
st.write("Upload a document (PDF) and ask questions about its content or generate a summary.")

# Initialize session state for file reference
if "uploaded_file_reference" not in st.session_state:
    st.session_state["uploaded_file_reference"] = None

# File upload
uploaded_file = st.file_uploader("Choose a document (PDF)...", type=["pdf"])

# Handle file upload
if uploaded_file is not None:
    if st.session_state["uploaded_file_reference"] is None:
        with st.spinner("Uploading file to Gemini API..."):
            # Upload the PDF to Gemini API with mime_type set to 'application/pdf'
            sample_pdf = genai.upload_file(uploaded_file, mime_type="application/pdf")
            st.session_state["uploaded_file_reference"] = sample_pdf  # Store the file reference in session state
        st.success("File uploaded successfully.")
    

# User prompt (works independently of file upload)
user_prompt = st.text_input("Ask a question about the document or just a general question:")

# Generate response
if user_prompt and st.button("Generate Response"):
    if st.session_state["uploaded_file_reference"] is not None:
        # Use the uploaded file for document-specific queries
        response = model.generate_content([user_prompt, st.session_state["uploaded_file_reference"]])
    else:
        # Fallback to normal text query without a file
        response = model.generate_content(user_prompt)
    
    # Display the response
    st.success("Response received:")
    st.write(response.text)

# Sidebar: File metadata and operations
st.sidebar.title("File Operations")

if st.sidebar.button("List Files"):
    st.sidebar.write("Files uploaded via API:")
    for f in genai.list_files():
        st.sidebar.write(f"- {f.name}")

# File deletion (example)
if st.sidebar.button("Delete All Files"):
    for f in genai.list_files():
        f.delete()
    st.sidebar.write("All files deleted.")
