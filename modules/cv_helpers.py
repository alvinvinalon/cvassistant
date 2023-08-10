import streamlit as st
import pdfplumber
import base64
import itertools
import base64
from PyPDF2 import PdfReader
from modules.openai_utils import *
from modules.app_helpers import *
from dotenv import load_dotenv
from pptx import Presentation
from dotenv import load_dotenv

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
    
# Create a function that generates a prompt for OpenAI's GPT model based on the selected CV function
def generate_prompt_cv_function(cv_function, cv_custom_prompt=""):
    prompt = ""
    if cv_custom_prompt != "":
        prompt = cv_custom_prompt + "\n\n"
    else:
        if cv_function == "CV Reviewer":       
            # Update this prompt to include the CV Reviewer instructions.
            prompt = (
                "You are an expert Career Adviser.\n"
                "Provide detailed feedback and additional recommendations about contents of the CV below. "
                "State if the CV is well-written or not.\n"                
                "The owner of the CV is a Sofware Engineer with various experience in the IT industry.\n\n"
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
                "Here's an example response:\n"
                "[Well-Written CV]:This CV is well-written and concise. It highlights the most important and relevant achievements.\n"
                "[Not a Well-Written CV]: This CV is not well-written as it lacks the most important and relevant achievements.\n"
                "[Areas for Improvement]:\n"
                "1. [provide recommended rewrite for first area that can be improved].\n"
                "2. [provide recommended rewrite for second area that can be improved].\n"
                "3. [provide recommended rewrite for second area that can be improved].\n"
                "[Conclusion]: This is an example conclusion.\n\n"
                "Recommend brevity to make the CV easier to read and more appleaing to the readers.\n"
                "Finally, choose 3 areas found in the CV and rewrite them to improve the content.")
        elif cv_function == "CV Summarizer":
            prompt = (
                    "Below is a CV content. Summarize in bullet points the contents of the CV below.\n"
                    "Include the most important information about the person's CV.\n"
                    "Use complete sentences and proper grammar.\n"
                    "Extract all Achievements, Technical Skills, Certifications, and Experience of the person.\n\n"
                    "Example of response:\n"
                    "[Summary of Professional Background]:\n"
                    "[Summary of Technical Skills]:\n"
                    "1. Technical Skill in bullet list\n"
                    "2. Certifications in bullet list\n"
                    "3. Experience in bullet list\n"
                    "4. [All other relevant information] in bullet list\n\n")
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