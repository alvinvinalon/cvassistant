import streamlit as st
from langchain.schema import (  
    SystemMessage,  
    HumanMessage,  
    AIMessage  
) 
import os
from dotenv import load_dotenv 


def initialize_state():
    load_dotenv()
    if "personality" not in st.session_state:
        st.session_state.personality_state = "Professional"
    if "character" not in st.session_state:
        st.session_state.character_state = "an A.I. Assitant"
    if "assistant_name_state" not in st.session_state:
        st.session_state.assistant_name_state = "Savi"
    if "total_token_count" not in st.session_state:
        st.session_state.total_token_count = 0
    if "assistant_name_state" not in st.session_state.assistant_name_state:
        st.session_state.assistant_name_state = "Savi"
    if "user_input_state" not in st.session_state:
        st.session_state.user_input_state = ""
    if "image_gen_input_state" not in st.session_state:
        st.session_state.image_gen_input_state = ""
    if "temperature_state" not in st.session_state:
        st.session_state.temperature_state = "0.7"
    if "max_tokens_state" not in st.session_state:
        st.session_state.max_tokens_state = "800"
    if "suggested_questions_state" not in st.session_state:
        st.session_state.suggested_questions_state = False
    if "feature_state" not in st.session_state:
        st.session_state.feature_state = "GPT-4 CoPilot"
    if "question_state" not in st.session_state:
        st.session_state.question_state = ""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "gpt_version_state" not in st.session_state:
        st.session_state.gpt_version_state = "GPT-3.5"

    # Set states for OPENAI Settings (GPT-3.5)
    if "openai_api_base_state" not in st.session_state:
        st.session_state.openai_api_base_state = os.environ.get("OPENAI_API_BASE_35")
    if "openai_api_key_state" not in st.session_state:
        st.session_state.openai_api_key_state = os.environ.get("OPENAI_API_KEY_35")
    if "openai_engine_state" not in st.session_state:
        st.session_state.openai_engine_state = os.environ.get("OPENAI_API_ENGINE_35")
    if "openai_chat_engine_state" not in st.session_state:
        st.session_state.openai_chat_engine_state = os.environ.get("OPENAI_API_CHAT_ENGINE_35")

# Create a function that clears the textarea and state of the textarea input
def clear_textarea_input():
    st.session_state.user_input_state = ""
    st.session_state.image_gen_input_state = ""

def clear_chat_session(prompt_system_message):
    st.session_state.messages = []
    initialize_state()
    st.session_state.messages = [  
        SystemMessage(content=prompt_system_message)  
        ]
    st.session_state.total_token_count = 0 