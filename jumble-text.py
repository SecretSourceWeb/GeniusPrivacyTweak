"""
This is a python script that reads in a text file and jumbles the text in each line.
The jumbled text is then written to a new file.
The words are jumbled using a Ceasar Cipher. The number of characters to shift is
stored in an environment variable called GPT_SHIFT. If GPT_SHIFT is not set, the default
value of 13 is used.
Once the text is jumbled, the cipher is run again but this time, instead of shifting
the characters, the words are shifted. The number of words to shift is the same as
the number of characters to shift.
The text file to read is specified as a parameter to the script.
The jumbled text and the original text are stored as a plain text in the file.
The format for the text is:
Training set:

    e: original text
    s: jumbled text
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

sw = GeniusPrivacyTweak(shift=shift)

for line in lines:
    # remove the newline character
    line = line.strip()
    sw.input = line
    jumbled_lines.append(sw.encode())
    logging.debug("Logged %s", line)

# write the jumbled and original text to the json object
training_set = []
for i in range(len(lines)):
    training_set.append("e: " + lines[i].strip() + "\ns: " + jumbled_lines[i] + "\n\n")
    logging.debug("training_set length %s", len(training_set))

# write the jumbled text to a file
f = open("jumbled-text.txt", "w")
translations = "".join(training_set)
f.write("Training Set:\n\n" + translations)
f.close()

