import streamlit as st
import base64
from langchain.chat_models import AzureChatOpenAI
import os
import requests
import time
import pytz
import cv2
from datetime import datetime

def set_background_image(image_path):  
    with open(image_path, "rb") as f:  
        img_bytes = f.read()  
        img_b64 = base64.b64encode(img_bytes).decode()  
        background_image = f"data:image/jpeg;base64,{img_b64}"  
  
    st.markdown(  
        f"""  
        <style>  
        .stApp {{  
            background-image: url("{background_image}");  
            background-size: cover;  
            background-repeat: no-repeat;  
        }}  
        </style>  
        """,  
        unsafe_allow_html=True  
    )  

def get_prompt_system_message(assistant_name, expertise, personality, character, current_datetime_str, suggested_questions):  
    if suggested_questions:
        suggested_questions_str = "Generate three Suggested follow up questions related to the user's question."
    else:  
        suggested_questions_str = ""
    
    return f"Your name is {assistant_name}. You are an expert on the following Topics: {expertise}.\n"\
        f"Your personality is a {personality} assistant who helps users with their inquiries about the Topics mentioned.\n"\
        f"Respond to the user's questions as if you are {character}\n{suggested_questions_str}\n\n"\
        f"Avoid responding to questions that are not related to the topics mentioned.\n\n"\
        f"The current date and time is {current_datetime_str}."

### Create a function to configure AzureChatOpenAI module
def set_azurechatopenai(temperature_slider, max_tokens_input):
            # Initialize the chatbot
        chat = AzureChatOpenAI(  
            openai_api_base=os.environ.get("OPENAI_API_BASE"),  
            openai_api_version=os.environ.get("OPENAI_API_CHAT_VERSION"),  
            deployment_name=os.environ.get("OPENAI_API_ENGINE"),  
            openai_api_key=os.environ.get("OPENAI_API_KEY"),  
            openai_api_type="azure",  
            temperature=temperature_slider, #0.7,  
            max_tokens=max_tokens_input #2048  
        )
        return chat


### Create a function to set the date and time in AEST for the chatbot
def get_current_time_aest():
    now = datetime.now(pytz.utc)  # Get the current time in UTC  
    aest = pytz.timezone('Australia/Sydney')  # Define the AEST timezone  
    now_aest = now.astimezone(aest)  # Convert the time to AEST  
    current_datetime_str = now_aest.strftime("%Y-%m-%d %H:%M:%S")  
    return current_datetime_str

# Write a function that returns a greeting message based on the time of the day
def get_greeting_message():
    now = datetime.now(pytz.utc)  # Get the current time in UTC  
    aest = pytz.timezone('Australia/Sydney')  # Define the AEST timezone  
    now_aest = now.astimezone(aest)  # Convert the time to AEST  
    current_time = now_aest.strftime("%H:%M:%S")  
    current_hour = int(current_time.split(":")[0])
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
    
def draw_transparent_rectangle(image, start_point, end_point, color, thickness, alpha=0.5):
    overlay = image.copy()
    cv2.rectangle(overlay, start_point, end_point, color, thickness)
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

def display_logo(logo_path):
    with open(logo_path, "rb") as f:  
        img_bytes = f.read()  
        img_b64 = base64.b64encode(img_bytes).decode()  
        logo_image = f"data:image/jpeg;base64,{img_b64}"  

        #image = image.open(logo_path)
        #logo = logo_image.resize((60, 60 ))
        st.image(logo_image, width=60)