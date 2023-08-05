import streamlit as st 
from modules.app_helpers import set_background_image


def init():  
    if not st.session_state.get("configured", False):  
        st.set_page_config(  
            page_title="Azure Cognitive Services Demos",  
            page_icon="🤖",  
            layout="wide",  
            initial_sidebar_state="collapsed",  
            menu_items={"Get help": "https://learn.microsoft.com/en-us/azure/?product=popular"},  
        )  
        st.session_state.configured = True
        
    set_background_image("images/50060303.jpg")

def import_custom_font(font_url):
    st.markdown(f"<link href='{font_url}' rel='stylesheet' type='text/css'>", unsafe_allow_html=True)

