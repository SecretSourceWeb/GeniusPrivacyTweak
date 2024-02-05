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
system_prompt += ""

# initialize the user prompt with the value of the query parameter from the command line
user_prompt = sys.argv[2]

# obfuscate the prompt using GeniusPrivacyTweak
tweak.input = user_prompt
obfuscated_user_prompt = tweak.encode()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", obfuscated_user_prompt)
    ]
)
logging.debug("Prompt: %s", prompt)
model = ChatOpenAI(
    temperature=0, 
    model=os.getenv("LLM", 'gpt-3.5-turbo'), 
    openai_api_key=os.getenv("OPENAI_API_KEY", ''),
    model_kwargs={"top_p": 1, "frequency_penalty": 0.5}
)
output_parser = StrOutputParser()

chain = prompt | model | output_parser

output = chain.invoke({"query": obfuscated_user_prompt})

tweak.input = output
LLM_response = tweak.decode()

print("\nUser's query in English: " + user_prompt)
print("\nUser's query in Saraswati: " + obfuscated_user_prompt)
print("\nSystem's response in Saraswati: " + output)
print("\nSystem's response in English: " + LLM_response + "\n")