"""
This is a python script that reads in a text file and jumbles the text in each line.
The jumbled text is then written to a new file.
The words are jumbled using a Ceasar Cipher. The number of characters to shift is
stored in an environment variable called SHIFT. If SHIFT is not set, the default
value of 13 is used.
Once the text is jumbled, the cipher is run again but this time, instead of shifting
the characters, the words are shifted. The number of words to shift is the same as
the number of characters to shift.
The text file to read is specified as a parameter to the script.
The jumbled text and the original text are stored as a json object in the file.
The format for the json object is:
{
    "training_set": [
        {
            "input": "text",
            "output": "text"
        },
        {
            "input": "text",
            "output": "text"
        }
    ]
}
"""

import os
import sys
import json
import string
import logging

from genius_privacy_tweak import GeniusPrivacyTweak

logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    format='%(name)s - %(levelname)s - %(message)s'
)

# Get the number of characters to shift from the environment variable SHIFT
# If SHIFT is not set, use the default value of 13
shift = int(os.getenv("GPT_SHIFT", 13))

# Get the file to read from the command line
if len(sys.argv) != 2:
    print("Usage: python jumble-text.py <filename>")
    sys.exit(1)
filename = sys.argv[1]

# Open the file to read, reading one line at a time
f = open(filename, "r")
lines = f.readlines()
f.close()

# loop through each line and jumble the text
jumbled_lines = []

sw = GeniusPrivacyTweak(output_lang="Saraswati", shift=shift)

for line in lines:
    # remove the newline character
    line = line.strip()
    sw.input = line
    jumbled_lines.append(sw.translate())
    logging.info("Logged %s", line)

# write the jumbled and original text to the json object
training_set = []
for i in range(len(lines)):
    training_set.append({"e": lines[i].strip(), "s": jumbled_lines[i]})
json_object = {"training_set": training_set}

json_string = json.dumps(json_object, ensure_ascii=False)

# write the json object to a file
f = open("jumbled-text.json", "w")
f.write(str(json_string))
f.close()

# print the json object to the console
print(json_string)

