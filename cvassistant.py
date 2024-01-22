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

# Save the states of the sidebar and main page
if "override_cv_function_prompt" not in st.session_state:
    st.session_state.override_cv_function_prompt = ""
if "azure_openai_url" not in st.session_state:
    st.session_state.azure_openai_url = ""
if "azure_openai_key" not in st.session_state:
    st.session_state.azure_openai_key = ""
if "azure_openai_deployment_model" not in st.session_state:
    st.session_state.azure_openai_deployment_model = ""

st.header("OpenAI CV Assistant")
st.write("This app uses OpenAI's GPT model to review and provide recommneations about your CV. Upload a PDF, PPT, or PPTX file containing your CV and get recommendations on how to improve it.")

with st.sidebar:
    with st.expander("Azure OpenAI Settings", expanded=False):
        # Add text boxes so users can enter their own OpenAI URL and Key
        st.subheader("Azure OpenAI Settings")
        st.write("Enter your OpenAI API URL and Key. If you don't have one, apply for access using this [link](https://avanade.sharepoint.com/:w:/r/sites/AustralianSETC/Shared%20Documents/General/GenAI/Applying%20for%20Azure%20OpenAI%20access.docx?d=w65dc8725565c4430a5777d55137ef79b&csf=1&web=1&e=aHW5Im).")
        openai_url = st.text_input("OpenAI API URL", "", help="Enter your OpenAI API URL. If you don't have one, you can get one from the OpenAI website.",placeholder="https://servicename.openai.azure.com/")
        openai_key = st.text_input("OpenAI API Key", "", help="Enter your OpenAI API Key. If you don't have one, you can get one from the OpenAI website.", type="password")
        openai_deployment_model = st.text_input("OpenAI Deployment Model", "", help="Enter your OpenAI Deployment Model. If you don't have one, you need to create a deployment.",placeholder="gpt-35-turbo")
        
        # Save the Azure OpenAI settings to the session state
        st.session_state.azure_openai_url = openai_url
        st.session_state.azure_openai_key = openai_key
        st.session_state.azure_openai_deployment_model = openai_deployment_model
    
    cv_function = st.selectbox("Select a function:", ["CV Reviewer", "CV Summarizer"], help="Select a function to perform on the CV.\nCV Reviewer: Review the CV and provide feedback.\nCV Summarizer: Summarize the CV.")
    
    # Create an expander for the CV Reviewer function    
    with st.expander("Overrides", expanded=True):
        cv_function_prompt = generate_prompt_cv_function(cv_function)   
        override_cv_function_prompt = st.text_area("Override the CV Reviewer prompt:", cv_function_prompt, help="Override the default prompt for the CV Reviewer function. This prompt will be used to generate the response from OpenAI's GPT model.")
        
    apply_override = st.button("Apply", help="Apply the override prompt to the CV Reviewer function.")
    if apply_override:
        st.session_state.override_cv_function_prompt = override_cv_function_prompt
        #st.markdown(st.session_state.override_cv_function_prompt, unsafe_allow_html=True)

    use_default = st.button("Use Default", help="Use the default prompt for the CV Reviewer function.")
    if use_default:
        st.session_state.override_cv_function_prompt = generate_prompt_cv_function(cv_function)
        override_cv_function_prompt=st.session_state.override_cv_function_prompt
        #st.markdown(cv_function_prompt, unsafe_allow_html=True)

    print(st.session_state.override_cv_function_prompt)

    # Footer
    st.markdown(f"<small style='color: #000000;'>CV Assistant version 0.1</small>", unsafe_allow_html=True)

# Try catch block to handle errors   
uploaded_file = st.file_uploader("Upload a PDF, PPT, or PPTX file containing a person's CV", type=["pdf", "ppt", "pptx"])

if uploaded_file is not None:
    st.success("File has been accepted. Click Apply to extract the text and analyze the contents.")  

if st.session_state.azure_openai_url == "" or st.session_state.azure_openai_key == "" or st.session_state.azure_openai_deployment_model == "":
    st.error("Please enter your Azure OpenAI settings in the sidebar.")

if apply_override and uploaded_file is not None and st.session_state.azure_openai_url != "" and st.session_state.azure_openai_key != "" and st.session_state.azure_openai_deployment_model != "":
    file_ext = uploaded_file.name.split(".")[-1].lower()
    file_name = f"{uploaded_file.name}"
     
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
    response = generate_openai_responsefor_cv(extracted_text, st.session_state.override_cv_function_prompt)
    print(response)
    # display the response in plain text
    with st.expander("View response", expanded=True):
        st.markdown(f"<div style='background-color: rgba(7,25,51,0.5); color: #FFFFFF; border: 1px solid #ccc; padding: 1rem; margin-bottom: 1rem;'>{response}</div>", unsafe_allow_html=True)
    
