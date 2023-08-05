import openai
import os
from modules.cv_helpers import *

# The Completion Engine to use for OpenAI
openai_completion_engine = os.environ.get("OPENAI_API_CHAT_ENGINE_35")


# Helper function to generate the prompt the CV Reviewer app
def generate_prompt_cv_reviewer(prompt, data, function, custom_prompt=""):

    cv_function_prompt = generate_prompt_cv_function(function, custom_prompt)
    
    prompt = (
        f"{cv_function_prompt}\n" 
        "# Start of CV:\n"  
        f"{data}"
        "# End of CV:"
    )

    # print(prompt)

    return prompt

def generate_openai_responsefor_cv(prompt, data, cv_function, cv_custom_prompt, max_tokens=800):
    
    # Set up OpenAI API credentials
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = os.environ.get("OPENAI_API_CHAT_VERSION") 
    openai.api_key = os.environ.get("OPENAI_API_KEY")    
    
    #print(data)
    prompt_question = generate_prompt_cv_reviewer(prompt, data, cv_function, cv_custom_prompt)
    #print(prompt_question)
    response = openai.Completion.create(
        engine=os.environ.get("OPENAI_API_ENGINE"),
        prompt=prompt_question,
        temperature=0.1,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None      
    )
    #return response.choices[0].text.strip()
    answer = response.choices[0].text
    #print(response)
    return answer

