# A Python Streamlit-based WebApp integrated with Azure OpenAI
This experimental web app uses the Streamlit web development framework and integrates with Azure OpenAI. 
Configured to use GPT-3.5 Turbo, but if you get access to GPT-4 deployments, just update the OpenAI Endpoint and key

## Streamlit
Visit the official website: https://streamlit.io/

## Pre-requisites
- Python 3.11.3 and pip. You can download the latest version of Python from the official website (https://www.python.org/downloads/). 
- An Azure Subscription with Azure OpenAI Service provisioned.
- OpenAI model deployment. (https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
- Create a deployment model called "chat"
- Visual Studio Code

## How to run locally
1. Clone this repository and open the folder in VS Code

2. Open VS Code Terminal window and execute: 

```python -m venv venv ```
   This will create a Virtual Environment for the Python app

3. Execute: 

```.\venv\Scripts\activate```

   Your Terminal code will show (venv), which means you're now inside the virtual environment

4. Install the dependencies by running (this could take a few minutes):

```pip install -r requirements.txt```

3. Rename the ```.env.txt``` file found in the root directory to ```.env```.

Replace the values for API_BASE AND API_KEY  (The values must come from your Azure OpenAI Service)

4. Run ```streamlit run cvassistant.py``` in the VS Code terminal

The web app will launch on your default browser.

5. Select a function: CV Reviewer or CV Summarizer

