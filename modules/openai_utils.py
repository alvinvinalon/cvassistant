import openai
import os
import tiktoken
from modules.cv_helpers import *

# Helper function to generate the prompt the CV Reviewer app
def generate_prompt_cv_reviewer(data, cv_function_prompt):

    prompt=""
    
    prompt = (
        f"{cv_function_prompt}\n" 
        "# Start of CV contents:\n"  
        f"{data}"
        "# End of CV content:"
    )

    # print(prompt)

    return prompt

def generate_openai_responsefor_cv(data, cv_function_prompt, max_tokens=2500):
    
    # Set up OpenAI API credentials
    openai.api_type = "azure"
    openai.api_base = st.session_state.azure_openai_url
    openai.api_key = st.session_state.azure_openai_key   
    openai.api_version = "2023-03-15-preview"
        
    prompt_question = generate_prompt_cv_reviewer( data, cv_function_prompt)    
    
    response = openai.Completion.create(
        engine=st.session_state.azure_openai_deployment_model,
        prompt=prompt_question,
        temperature=0.3,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None      
    )    
    answer = response.choices[0].text    
    token_count = response['usage']['total_tokens']
    print("token count: ", token_count) 
    #print("answer: ", answer)
    # remove <|im_end|> from the answer
    answer = answer.replace("<|im_end|>", "")
    return answer