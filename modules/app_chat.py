import streamlit as st
from modules.app_speech import speak_text
from modules.app_helpers import *
from langchain.schema import (  
    SystemMessage,  
    HumanMessage,  
    AIMessage  
)  

def display_chat_messages(messages, token_limit):

    if len(messages) > 0:
        #messages = st.session_state.get('messages', [])  
        for i, msg in enumerate(messages[1:]):  
            if i % 2 == 0:  
                # User message  
                with st.container():  
                    col1, col2 = st.columns([1, 9])  
                    with col1:  
                        st.write("")  
                    with col2:  
                        st.markdown(f'<div style="background-color: rgba(96,105,117,0.5); border-radius: 5px; padding: 10px; margin-bottom: 10px; color: #FFFFFF; text-align: left;">🗨️&nbsp;{msg.content}<span style="margin-left: 5px;"></span></div>', unsafe_allow_html=True)  
            else:  
                # AI message              
                with st.container():  
                    col1, col2 = st.columns([9, 1])  
                    with col1:                   
                        st.markdown(f'<div style="background-color: rgba(7,25,51,0.5); border-radius: 5px; padding: 10px; margin-bottom: 10px; color: #FFFFFF;"><span style="margin-right: 5px;"></span>💡{msg.content}<div style="font-size: 0.8rem; text-align: right; margin-top: 5px;">Tokens used: {st.session_state.total_token_count}/{token_limit}</div></div>', unsafe_allow_html=True,)  
                    with col2:  
                        # Show audio button if feature is Converse with Copilot
                        aud_col1, aud_col2 = st.columns([1, 1])
                        with aud_col1:
                            speak_button = st.button("🔊", key=f"speak_button_{i}")                       
                        with aud_col2:
                            if speak_button:                            
                                audio_data = speak_text(msg.content, st.session_state.speech_speaker_state, "speak", st.session_state.voice_style_state)
                                st.audio(audio_data, format="audio/mp3")
                            else:
                                st.write("")       


                 