"""
This is an application that demonstrates how GeniusPrivacyTweak works.

It provides a chat UI on the command line, and allows you to ask an LLM questions.

This is not a chatbot, but rather a demonstration of how to use the this library.

It depends on LangSmith. We use LangSmith to prove that the data sent to the LLM is obfuscated as is the data produced by the LLM.

To use this application, you must have a valid OpenAI API key and LangSmith key in your .env file.

To run the application from the command line, type:

python app.py --query "What is the meaning of life?"
"""

import os
import sys
import time
import logging
import argparse
import subprocess

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from genius_privacy_tweak import GeniusPrivacyTweak

load_dotenv(find_dotenv())  # read local .env file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up the command line arguments
parser = argparse.ArgumentParser(description='A demonstration of GeniusPrivacyTweak.')

# initialize the tweak
tweak = GeniusPrivacyTweak(shift=int(os.getenv("GPT_SHIFT")))

# initialize the system prompt by reading in system-prompt.txt file
system_prompt = "System: " + open("system-prompt.txt", "r").read()

# initialize the training data by running jumble-text.py 
# using the english-pangram.txt file as the input
# and appending the ouptut to the system_prompt variable
# training_data = exec("python jumble-text.py english-pangram.txt")
# if jumbled-text.txt does not exist, it will be created
process = subprocess.run("python jumble-text.py english-pangrams.txt", shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
if process.returncode != 0:
    print("Error: " + process.stdout)
    sys.exit(1)
else:
    system_prompt += process.stdout

# initialize the user prompt with the value of the query parameter from the command line
user_prompt = "User: " + sys.argv[2]

# obfuscate the prompt using GeniusPrivacyTweak
tweak.input = user_prompt
obfuscated_user_prompt = tweak.translate()

# prompt = ChatPromptTemplate.from_template("chat", system_prompt=system_prompt, user_prompt=obfuscated_user_prompt)
prompt = ChatPromptTemplate.from_template(system_prompt + "\n\nAnd here is the user's query in Saraswati: {query}")
logging.debug("Prompt: %s", prompt)
model = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY", ''))
output_parser = StrOutputParser()

chain = prompt | model | output_parser

output = chain.invoke({"query": obfuscated_user_prompt})

tweak.ouptut_lang="English"
tweak.input = output
LLM_response = tweak.translate()

print("User's query in Saraswati: " + obfuscated_user_prompt)
print("System's response in Saraswati: " + output)
print("System's response in English: " + LLM_response)