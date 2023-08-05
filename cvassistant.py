import streamlit as st
import io
from PyPDF2 import PdfReader
from modules.openai_utils import *
from modules.app_helpers import *
from modules.cv_helpers import *
from dotenv import load_dotenv
import os

load_dotenv()

set_background_image("images/orangeBG.png")

st.header("OpenAI CV Assistant")
st.write("This app uses OpenAI's GPT model to review and provide recommneations about your CV. Upload a PDF, PPT, or PPTX file containing your CV and get recommendations on how to improve it.")

with st.sidebar:
    cv_function = st.selectbox("Select a function:", ["CV Reviewer", "CV Summarizer"], help="Select a function to perform on the CV.\nCV Reviewer: Review the CV and provide feedback.\nCV Summarizer: Summarize the CV.")
    cv_custom_prompt = "" # not used for this version.

    # Footer
    st.markdown(f"<small style='color: #000000;'>CV Assistant version 0.1</small>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a PDF, PPT, or PPTX file containing a person's CV", type=["pdf", "ppt", "pptx"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    file_name = f"{uploaded_file.name}"

    st.success("File has been uploaded. Extracting text...")   
    saved_file_bytes = io.BytesIO(uploaded_file.read())

    # Extract text from the downloaded file
    if file_ext == "pdf":
        extracted_text = extract_text_from_pdf_pypdf2(saved_file_bytes)
    elif file_ext in ["ppt", "pptx"]:
        extracted_text = extract_text_from_ppt(saved_file_bytes)
    else:
        st.error("Unsupported file type. Please upload a PDF, PPT, or PPTX file.")

    with st.expander("View extracted text"):
        st.write(extracted_text)

    # Generate response based on the selected function
    response = generate_openai_responsefor_cv("", extracted_text, cv_function, cv_custom_prompt)
    st.markdown(f"<div style='background-color: rgba(7,25,51,0.5); color: #FFFFFF; border: 1px solid #ccc; padding: 1rem; margin-bottom: 1rem;'>{response}</div>", unsafe_allow_html=True)
