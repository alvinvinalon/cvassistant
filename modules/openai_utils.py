import openai
import os
import tiktoken
from modules.cv_helpers import *

# The Completion Engine to use for OpenAI
openai_completion_engine = os.environ.get("OPENAI_API_CHAT_ENGINE_35")


# Helper function to generate the prompt the CV Reviewer app
def generate_prompt_cv_reviewer(prompt, data, function, custom_prompt=""):

    cv_function_prompt = generate_prompt_cv_function(function, custom_prompt)
    
    prompt = (
        f"{cv_function_prompt}\n\n" 
        "# Start of CV contents:\n"  
        f"{data}"
        "# End of CV content:"
    )

    # print(prompt)

    return prompt

def generate_openai_responsefor_cv(prompt, data, cv_function, cv_custom_prompt, max_tokens=800):
    
    # Set up OpenAI API credentials
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = os.environ.get("OPENAI_API_CHAT_VERSION") 
    openai.api_key = os.environ.get("OPENAI_API_KEY")    
    
    prompt_question = generate_prompt_cv_reviewer(prompt, data, cv_function, cv_custom_prompt)    

    #print("prompt: ", prompt_question) 
    token_count = count_tokens(prompt_question)
    print("token count: ", token_count)
    
    response = openai.Completion.create(
        engine=os.environ.get("OPENAI_API_ENGINE"),
        prompt=prompt_question,
        temperature=0.5,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None      
    )    
    answer = response.choices[0].text    
    print("answer: ", answer)
    # remove <|im_end|> from the answer
    answer = answer.replace("<|im_end|>", "")
    return answer

def count_tokens(text):
    token_count = tiktoken.count_tokens(text)
    return token_count

# input_query = "Your input query goes here"
# token_count = count_tokens(input_query)
# print("Token count:", token_count)
