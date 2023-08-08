# A Python Streamlit-based WebApp integrated with Azure OpenAI
This experimental web app uses the Streamlit web development framework and integrates with Azure OpenAI. 
Can be configured to use GPT-3.5 Turbo, but if you get access to GPT-4 deployments, just update the OpenAI Endpoint and key

## Streamlit
Visit the official website: https://streamlit.io/

## Pre-requisites
- Python 3.11.3 and pip. You can download the latest version of Python from the official website (https://www.python.org/downloads/). 
- An Azure Subscription with Azure OpenAI Service provisioned.
- OpenAI model deployment. (https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
- Create a deployment model called "chat" or use your own name (make sure you update it in the .env file.)
- Visual Studio Code

## How to run locally
1. Clone this repository and open the folder in VS Code

2. Open VS Code Terminal window and execute: 

```python -m venv venv ```

   This will create a Virtual Environment for the Python app

3. While in the Terminal window, execute: 

```.\venv\Scripts\activate```

   Your Terminal code will show (venv), which means you're now inside the virtual environment.

4. Install the dependencies by running the command below (this could take a few minutes):

```pip install -r requirements.txt```

3. Rename the ```.env.txt``` file found in the root directory to ```.env```.

Replace the values for OPENAI_API_BASE AND OPENAI_API_KEY  (The values must come from your Azure OpenAI Service)

4. In the terminal window, execute:
   
```streamlit run cvassistant.py``` 

(make sure your ```venv``` is activated)
The web app will launch on your default browser.

5. Select a function: CV Reviewer or CV Summarizer from the left side-bar.

6. To upload your CV, click on the 'Browse Files' button and select your file. Please note that the application currently only supports PPT, PPTX, and PDF file types.

Once you've uploaded your file, the application will extract the text and provide feedback on the contents. This will help you identify areas for improvement and ensure your CV is as effective as possible.

