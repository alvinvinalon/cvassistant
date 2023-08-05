import streamlit as st
import os
import requests
import base64
import time
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import (  
    SystemMessage,  
    HumanMessage,  
    AIMessage  
)  
import openai
from modules.app_state import *
from modules.app_helpers import *
from dotenv import load_dotenv

### Create a function to configure AzureChatOpenAI module
def set_azurechatopenai(temperature_slider, max_tokens_input, openai_api_base, openai_api_version, deployment_name, openai_api_key):
       
        #print the openAI settings
        print("OpenAI API Base: ", openai_api_base)
        print("OpenAI API Version: ", openai_api_version)
        print("OpenAI API Engine: ", deployment_name)
        #print("OpenAI API Key: ", os.environ.get("OPENAI_API_KEY"))

        # Initialize the chatbot
        chat = AzureChatOpenAI(  
            openai_api_base=openai_api_base,  
            openai_api_version=openai_api_version,  
            deployment_name=deployment_name,  
            openai_api_key=openai_api_key,  
            openai_api_type="azure",  
            temperature=temperature_slider,  
            max_tokens=max_tokens_input
        )
        return chat

def generate_response(prompt):    
    chat=set_azurechatopenai(st.session_state.temperature_state, st.session_state.max_tokens_state, st.session_state.openai_api_base_state, "2023-03-15-preview", st.session_state.openai_engine_state, st.session_state.openai_api_key_state)
    st.session_state.messages.append(HumanMessage(content=prompt)) 
    #print("Messages: ", st.session_state.messages)
    with st.spinner("Thinking..."):  
        try:                
            response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))   
            token_count = chat.get_num_tokens_from_messages(st.session_state.messages)
            st.session_state.total_token_count = token_count
        except Exception as error:
            response = "Looks like something went wrong: " + str(error)    
            st.session_state.messages.append(AIMessage(content=response))

# Function to call OPENAI
def generate_optimized_dalle_prompt(prompt):  

    load_dotenv()
    # Set up OpenAI API credentials. Uses GPT-3.5 and Text Davinci to create an optimized prompt.
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    openai.api_base = os.environ.get("OPENAI_API_BASE_35")
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.environ.get("OPENAI_API_KEY_35")
    openai_completion_engine = os.environ.get("OPEN_API_COMPLETION_ENGINE_35")

    # Remove any periods in the prompt
    prompt = prompt.replace(".", "")

    # Prompt Optimization
    
    optimized_prompt = "Rewrite this DALL-E prompt '"+prompt+"'. The new statement should produce a photo realistic and visually stunning image using your own creativity. " \
                    "The new prompt should always start with 'Generate an image of'. The statement should include new creative ideas. Create only one sentence for the prompt and do not include any other statements or explanations."
        
    print("Optimized Prompt: ", optimized_prompt)

    response = openai.Completion.create(
        engine=openai_completion_engine,
        prompt=optimized_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=1,
    )

    dalle_response = response.choices[0].text.strip()
    response = dalle_response.replace("DALL-E Prompt: ", "")
    return response

# Create a function to generate an image using DALL-E and REST API
def generate_image_rest(prompt):
    api_base = os.environ.get("DALLE_OPENAI_API_BASE")
    api_key = os.environ.get("DALLE_OPENAI_API_KEY")
    api_version = '2023-06-01-preview'
    url = f"{api_base}openai/images/generations:submit?api-version={api_version}"
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    submission = requests.post(url, headers=headers, json=body)
    #print("URL:", url)

    operation_location = submission.headers['operation-location']
    status = ""

    try:
        while (status != "succeeded"):
            time.sleep(1)
            response = requests.get(operation_location, headers=headers)
            status = response.json()['status']
        image_url = response.json()['result']['data'][0]['url']
        # Download the image and return it as bytes  
        image_response = requests.get(image_url)  
        image_bytes = image_response.content  
        #print("Image bytes:", image_bytes[:100])  # Print the first 100 bytes of the image 
    except Exception as error:
        image_bytes = "Looks like something went wrong: " + str(error)

    return image_bytes

# Function for DALL-E Image Generation
def generate_image(prompt):
    st.session_state.messages.append(HumanMessage(content=prompt))   
    with st.spinner("Generating image..."):
        #Call The Chat model to generate a detailed DALL-E Prompt based on the prompt.
        #dalle_optimized_prompt = generate_optimized_dalle_prompt(prompt)
        #print(dalle_optimized_prompt)
        image_bytes = generate_image_rest(prompt)  
        image_data_uri = f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"  
        st.session_state.messages.append(AIMessage(content=image_data_uri))    