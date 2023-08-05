import streamlit as st
import openai
import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
import azure.ai.vision as sdk
from msrest.authentication import CognitiveServicesCredentials
import requests
import io
from PIL import Image
import cv2
import numpy as np
from modules.app_speech import speak_text

# Helper function to generate the prompt for OpenAI
def generate_prompt(question, result):
    prompt = (
        "You are a safety expert that helps identify potential dangerous situations based on the Image analysis result.\n"
        "Answer ONLY using the facts listed in the image analysis results below. Generate answers with 200 words or less.\n" 
        #"Confidence score below 0.5 is considered Low confidence. Confidence scores between 0.5 and 0.8 is considered Medium confidence, and confidence scores greater than 0.8 is considered High confidence.\n"
        "When confidence score is less than 0.5, mention this in your generated response.\n"
        "Convert confidence score to a percentage and round to 2 decimal places. For example, a confidence score of 0.5 will become confidence score of 50%.\n"
        "Do not generate answers that don't use the Image Analysis Results below.\n"
        "Start of Image Analysis Results:\n"    
        f"{result}\n"  
        "End of Image Analysis Results:\n"
        f"Q: {question}\n"  
        "A: "     
    )

    return prompt

def show_vision_demo(image_url):
    
    load_dotenv()

    # Set up OpenAI API credentials
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai_completion_engine = os.environ.get("OPENAI_API_CHAT_ENGINE")

    #Clear the question box
    st.session_state.question_image = ""

    # Generate unique key based on image URL
    key = f"analyze_image_{image_url}"
    Image_prompt = "```\n"

    if image_url:
        try:
            image_url_cleaned = image_url.replace(" ", "%20")
            image_url_cleaned = image_url_cleaned.replace("\n", "")
            # Get the Image Bytes so it can be displayed
            response = requests.get(image_url_cleaned)
            image_data = response.content
            image_stream = io.BytesIO(image_data)
            
            # Setup new Azure Computer Vision Image Analysis 4.0
            service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
                                                    os.environ["VISION_KEY"])
            
            vision_source = sdk.VisionSource(url=image_url)
            
            analysis_options = sdk.ImageAnalysisOptions()

            analysis_options.features = (
                sdk.ImageAnalysisFeature.CROP_SUGGESTIONS |
                sdk.ImageAnalysisFeature.CAPTION |
                sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
                sdk.ImageAnalysisFeature.OBJECTS |
                sdk.ImageAnalysisFeature.PEOPLE |
                sdk.ImageAnalysisFeature.TEXT |
                sdk.ImageAnalysisFeature.TAGS
            )

            # Initialize the new Vision API
            image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)
        
            # Analyze the image
            result = image_analyzer.analyze()

            if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
                
                # Convert the image to a NumPy array
                image_array = np.array(Image.open(image_stream).convert("RGB"))

                #st.checkbox("Show bounding boxes")
                if st.checkbox("Show bounding boxes"):
                    # Draw bounding boxes for dense captions
                    if result.dense_captions is not None:
                        for dense_caption in result.dense_captions:
                            x = int(dense_caption.bounding_box.x)
                            y = int(dense_caption.bounding_box.y)
                            w = int(dense_caption.bounding_box.w)
                            h = int(dense_caption.bounding_box.h)
                            start_point = (x, y)
                            end_point = (x + w, y + h)
                            color = (66, 245, 66)
                            thickness = 2

                            # Draw the bounding box on the image using OpenCV
                            image_array = cv2.rectangle(image_array, start_point, end_point, color, thickness)

                            # Set font, font scale, and color
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 0.5
                            font_color = (255, 255, 255)

                            # Calculate text size (width and height) to position the text properly
                            caption_text = dense_caption.content  # Replace this with the appropriate caption text attribute
                            (text_width, text_height), _ = cv2.getTextSize(caption_text, font, font_scale, 1)

                            # Draw the dense caption text on the image
                            text_position = (x, y - text_height if y - text_height > 0 else y + text_height)
                            cv2.putText(image_array, caption_text, text_position, font, font_scale, font_color, 1, cv2.LINE_AA)

                
                #print("image result:", result)         
                Image_prompt += f" Image height: {result.image_height}\n"
                Image_prompt += f" Image width: {result.image_width}\n"
                Image_prompt += f" Model version: {result.model_version}\n"

                if result.caption is not None:                    
                    result_caption = f"```\n'{result.caption.content}', Confidence {result.caption.confidence:.4f}\n"
                    Image_prompt += " Caption:\n"
                    Image_prompt += f"   '{result.caption.content}', Confidence {result.caption.confidence:.4f}\n"

                if result.dense_captions is not None:
                    result_dense_captions = "```\n"
                    Image_prompt += " Dense Captions:\n"
                    for caption in result.dense_captions:
                        result_dense_captions += f"'{caption.content}', Confidence: {caption.confidence:.4f}\n"
                        Image_prompt += f"   '{caption.content}', {caption.bounding_box}, Confidence: {caption.confidence:.4f}\n"
                    result_dense_captions += "```\n"

                if result.objects is not None:
                    result_objects = "```\n"
                    Image_prompt += " Objects:\n"
                    for object in result.objects:
                        result_objects += f"'{object.name}', Confidence: {object.confidence:.4f}\n"
                        Image_prompt += f"   '{object.name}', {object.bounding_box}, Confidence: {object.confidence:.4f}\n"
                    result_objects += "```\n"

                if result.tags is not None:
                    result_tags = "```\n"
                    Image_prompt += " Tags:\n"
                    for tag in result.tags:
                        result_tags += f"'{tag.name}', Confidence {tag.confidence:.4f}\n"
                        Image_prompt += f"   '{tag.name}', Confidence {tag.confidence:.4f}\n"
                    result_tags += "```\n"

                if result.people is not None:
                    result_people = "```\n"
                    Image_prompt += " People:\n"
                    for person in result.people:
                        result_people += f"'{person.bounding_box}', Confidence {person.confidence:.4f}\n"  
                        Image_prompt += f"   {person.bounding_box}, Confidence {person.confidence:.4f}\n"
                    result_people += "```\n"    

                if result.crop_suggestions is not None:
                    result_crop_suggestions = "```\n"
                    Image_prompt += " Crop Suggestions:\n"
                    for crop_suggestion in result.crop_suggestions:
                        result_crop_suggestions += f"Aspect ratio {crop_suggestion.aspect_ratio}: Crop suggestion {crop_suggestion.bounding_box}\n"
                        Image_prompt += f"   Aspect ratio {crop_suggestion.aspect_ratio}: Crop suggestion {crop_suggestion.bounding_box}\n"
                    result_crop_suggestions += "```\n"

                # Investigate why thiis is throwing an error
                # if result.text is not None:
                #     result_text = "```\n"
                #     Image_prompt += " Text:\n"
                #     for line in result.text.lines:
                #         points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                #         Image_prompt += f"Line: '{line.content}', Bounding polygon {points_string}\n"                       
                #         for word in line.words:
                #             result_text += f"Word: '{word.content}', Bounding polygon {word.bounding_box}, Confidence {word.confidence:.4f}\n"
                #             points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                #             Image_prompt += f"     Word: '{word.content}', Bounding polygon {points_string}, Confidence {word.confidence:.4f}\n"
                #     result_text += "```\n"

                result_details = sdk.ImageAnalysisResultDetails.from_result(result)
                Image_prompt += f" Result details:\n"
                Image_prompt += f"   Image ID: {result_details.image_id}"
                Image_prompt += "```\n"

               # Display image
                #st.image(Image.open(image_stream).convert("RGB"), caption="Input Image", use_column_width=True)
                img_col1, img_col2 = st.columns([4,6])
                with img_col1:
                    st.image(image_array, caption="Input Image", use_column_width=True)
                with img_col2:
                    # Display analysis results to user
                    with st.expander("Main Caption"):                        
                        #st.markdown(Image_prompt, unsafe_allow_html=True)
                        st.markdown(result_caption, unsafe_allow_html=True)
                    with st.expander("Dense Captions"):
                        st.markdown(result_dense_captions, unsafe_allow_html=True)
                    with st.expander("Objects"):
                        st.markdown(result_objects, unsafe_allow_html=True)
                    with st.expander("Tags"):
                        st.markdown(result_tags, unsafe_allow_html=True)
                    with st.expander("People"):
                        st.markdown(result_people, unsafe_allow_html=True)
                    with st.expander("Crop Suggestions"):
                        st.markdown(result_crop_suggestions, unsafe_allow_html=True)
                    # with st.expander("Text in photo"):
                    #     st.markdown(result_text, unsafe_allow_html=True)
                    with st.expander("Full Analysis Result"):
                        st.markdown(Image_prompt, unsafe_allow_html=True)

        except Exception as e:
            st.write("Error analyzing image:", e)

        text_to_speech = st.checkbox("Speak :speech_balloon:")        
        question = st.text_input("Ask a question about the image:", placeholder="(e.g. Are there any safety concerns in this photo?)", value=st.session_state.question_image)       
        prompt_question = generate_prompt(question, Image_prompt)
        #print(prompt_question)      
        #submit_question = st.button(":arrow_forward:")

        if question:  
            openai_response = openai.Completion.create(
                        engine=openai_completion_engine, \
                        prompt=prompt_question, \
                        max_tokens=256, \
                        temperature=st.session_state.temperature_state, \
                        stop=["\n"]
                    )

            answer = openai_response.choices[0].text.strip().replace("<|im_end|>", "")     

            # Define the CSS style for the semi-transparent background
            st.markdown("""
            <style>
                .answer-container {
                    background-color: rgba(96,105,117,0.5);
                    padding: 15px;
                    border-radius: 5px;
                    color: #ffffff;
                    margin-bottom: 15px;
                }
            </style>
            """, unsafe_allow_html=True)

            st.markdown(f'<div class="answer-container">{answer}</div>', unsafe_allow_html=True)
            if text_to_speech:            
                audio_data = speak_text(answer, "en-US-TonyNeural", "speak", "Friendly")
                audio_col1, audio_col2 = st.columns([3,6])
                with audio_col1:
                    st.audio(audio_data, format="audio/mp3")
                with audio_col2:
                    st.write("")