import streamlit as st
import pdfplumber
import base64
import itertools
import base64
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from PyPDF2 import PdfReader
from modules.openai_utils import *
from modules.app_helpers import *
from modules.app_logging import *
import os
from dotenv import load_dotenv
from pptx import Presentation
from dotenv import load_dotenv
import logging

load_dotenv()

def extract_text_from_ppt(ppt_file):
    prs = Presentation(ppt_file)
    text = ""

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text
        text += "\n"
    return text

def extract_text_from_pdf_pypdf2(source_file):
    reader = PdfReader(source_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text() + "\n"  
    return text

def extract_text_from_pdf(source_file):
    with pdfplumber.open(source_file) as pdf:
        text = ""
        for page in pdf.pages:
            words = page.extract_words()

            # Sort words by their top and left coordinates
            sorted_words = sorted(words, key=lambda word: (-word['top'], word['x0']))

            # Group words based on their top coordinates
            grouped_words = itertools.groupby(sorted_words, key=lambda word: word['top'])

            # Combine words in each group, separated by spaces
            lines = []
            for _, word_group in grouped_words:
                line = ' '.join(word['text'] for word in word_group)
                lines.append(line)

            # Combine lines into a single string, separated by newlines
            page_text = '\n'.join(lines)
            text += page_text + "\n\n"
    return text

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
# Function to upload a file to Azure Blob Storage
def upload_file_to_azure_blob_storage(file, file_name, AZURE_STORAGE_CONNECTION_STRING, container_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)

        # Upload the file. Overwrite if exists
        blob_client.upload_blob(file, overwrite=True)

        return True
    except Exception as e:
        print(e)
        print(f"Failed to upload file to Azure Blob Storage: {e}")
        return False

# Function to download a file from Azure Blob Storage
def download_file_from_azure_blob_storage(file_name, AZURE_STORAGE_CONNECTION_STRING, container_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file_name)

        # Download the file
        downloaded_file = blob_client.download_blob()
        return downloaded_file.readall()
    except Exception as e:
        print(f"Failed to download file from Azure Blob Storage: {e}")
        return None
    
# Create a function that generates a prompt for OpenAI's GPT model based on the selected CV function
def generate_prompt_cv_function(cv_function, cv_custom_prompt=""):
    prompt = ""
    if cv_custom_prompt != "":
        prompt = cv_custom_prompt + "\n\n"
    else:
        if cv_function == "CV Reviewer":       
            prompt = (
                "Provide detailed feedback and additional recommendations about contents of the CV below. "
                "State if the CV is well-written or not.\n"                
                "This individual will work closely with cross-functional teams to design, develop, and maintain innovative software solutions"
                "Analyze the content of the CV based on the following recommendations:\n"        
                " - The CV should be clear and concise.\n"
                " - The CV should highlight the most important and relevant achievements.\n"
                " - The CV should be written in English.\n"
                " - The CV should have a Professional Background.\n"
                " - The CV should be written in a professional tone.\n"        
                " - The CV should contain at least 1 IT relevant experience.\n"
                " - The CV should contain at least 2 IT relevant skills.\n"
                " - The CV should contain at least 1 IT relevant certification.\n"   
                " - The CV should contain any prior experience, even if they're not IT related.\n"  
                " - The CV should contain educational achievements and awards.\n\n"
                "Recommend brevity to make the CV easier to read and more appleaing to the readers.\n\n"
                "Finally, choose 3 areas found in the CV and rewrite them to improve the content.\n\n")
        elif cv_function == "CV Summarizer":
            prompt = (
                    "Summarize in bullet points the contents of the CV below.\n"
                    "Include the most important information about the person's CV.\n"
                    "Use complete sentences and proper grammar.\n"
                    "Mention all Achievements, Technical Skills, Certifications, and Experience of the person.\n")
        elif cv_function == "CV Analyzer":
            prompt = """
                    You are evaluating the CV of Software Engineering Candidates.\n                    
                    The ideal candidate will have a strong background in software development.\n                    
                    This individual will work closely with cross-functional teams to design, develop, and maintain innovative software solutions that meet business requirements and align with the company's strategic goals.\n
                    Responsibilities:\n
                    -Design, develop, test, and maintain software applications using modern development methodologies and best practices.\n
                    -Collaborate with product owners, project managers, and business analysts to gather, analyze, and prioritize requirements and convert them into functional specifications.\n
                    -Contribute to the development of application architecture, ensuring scalability, performance, and maintainability.\n 
                    -Integrate software components and third-party applications, ensuring seamless data exchange and system interoperability.\n
                    -Debug and resolve software defects and issues, providing root cause analysis and implementing corrective actions.\n
                    -Participate in code reviews, ensuring adherence to coding standards and best practices.\n
                    -Continuously improve development processes, tools, and methodologies to enhance software quality and team efficiency.\n
                    -Keep up-to-date with emerging technologies, industry trends, and best practices to continuously improve technical skills.\n
                    -Provide technical guidance and support to junior team members as needed.\n
                    -Assist in the creation and maintenance of technical documentation, including design documents, user guides, and system manuals.\n\n
                    Respond with "Qualified" if the candidate meets the above criteria based on their CV and provide your rationale why the candidate is qualified.\n
                    Response with "Not Qualified" if the candidate does not meet the above criteria based on their CV the criteria and provide your rationale why the candidate is not qualified.           

                    """
        elif cv_function == "CV QnA":
            prompt = "Follow the instructions below. Answer the questions based on the contents of the CV.\n"

    return prompt