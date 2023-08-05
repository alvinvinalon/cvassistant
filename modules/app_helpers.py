import streamlit as st
import base64
from langchain.chat_models import AzureChatOpenAI
import os
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