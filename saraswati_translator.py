"""Does bidirectional translation from English to Saraswati and vice versa"""
import logging
import string
import unicodedata
from typing import Dict, List, Sequence, Any

logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    format='%(name)s - %(levelname)s - %(message)s'
)

class SaraswatiTranslator(object):
    def __init__(self, input="hello", output_lang="Saraswati", shift=13):
        self.input = input
        self.output_lang = output_lang
        self.shift = shift

    def translate(self):
        """Translates the input text from English to Saraswati or vice versa"""
        if self.output_lang == "Saraswati":
            return self.to_saraswati()
        elif self.output_lang == "English":
            return self.to_english()
        else:
            raise ValueError("Invalid language")
    
    def to_saraswati(self):
        """Translates the input text from English to Saraswati (Ceaser cipher)"""
        jumbled_chars = []
        for char in self.input:
            jumbled_char = self.swap_character(char, self.shift)
            jumbled_chars.append(jumbled_char)
        return "".join(jumbled_chars)
    
    def to_english(self):
        """Translates the input text from Saraswati to English (Ceaser cipher)"""
        jumbled_chars = []
        for char in self.input:
            jumbled_char = self.swap_character(char, -self.shift)
            jumbled_chars.append(jumbled_char)
        return "".join(jumbled_chars)

    @staticmethod
    def swap_character(char: str = 'á', shift: int = 13):
        """Swaps a character with another character a certain number of positions away"""
        current_codepoint = ord(char)
        target_codepoint = ord(char) + shift

        # Only continue if the character is a letter
        if 'L' not in unicodedata.category(char):
            return char

        unicode_range_start, unicode_range_end = SaraswatiTranslator.get_valid_unicode_range(char)
        logging.debug(f"unicode_range_start: {unicode_range_start}, unicode_range_end: {unicode_range_end}")
        logging.debug(f"char {char} ({ord(char)})")

        if shift < 0:
            while current_codepoint >= target_codepoint:
                logging.debug(f"current_codepoint: {current_codepoint}, target_codepoint: {target_codepoint}")
                if 'L' not in unicodedata.category(chr(current_codepoint)):
                    # logging.debug("Skipping non-letter: %d", current_codepoint)
                    target_codepoint -= 1
                # wrap to end of letters if necessary
                if current_codepoint < unicode_range_start:
                    points_walked_so_far = ord(char) - current_codepoint
                    points_remaining = abs(shift) - points_walked_so_far
                    current_codepoint = unicode_range_end
                    target_codepoint = current_codepoint - points_remaining
                    logging.debug(f"END current_codepoint: {current_codepoint}, target_codepoint: {target_codepoint}, points_walked_so_far: {points_walked_so_far}, points_remaining: {points_remaining}")
                else:
                    current_codepoint -= 1
                    logging.debug(f"current_codepoint: {current_codepoint}, target_codepoint: {target_codepoint}")
        else:
            while current_codepoint <= target_codepoint:
                if 'L' not in unicodedata.category(chr(current_codepoint)):
                    # logging.debug("Skipping non-letter: %d", current_codepoint)
                    target_codepoint += 1
                # wrap to beginning of letters if necessary
                if current_codepoint > unicode_range_end:
                    points_walked_so_far = current_codepoint - ord(char)
                    points_remaining = shift - points_walked_so_far
                    current_codepoint = unicode_range_start
                    target_codepoint = current_codepoint + points_remaining
                    logging.debug(f"current_codepoint: {current_codepoint}, target_codepoint: {target_codepoint}, points_walked_so_far: {points_walked_so_far}, points_remaining: {points_remaining}")
                else:
                    current_codepoint += 1
                    logging.debug(f"current_codepoint: {current_codepoint}, target_codepoint: {target_codepoint}")

                
        
        jumbled_char = chr(target_codepoint)
        logging.debug(f"Shifted {char} ({ord(char)}) to {jumbled_char} {(ord(jumbled_char))}")

        return jumbled_char

    @staticmethod
    def get_valid_unicode_range(input="A"):
        """Returns the start and end code points as a tuple for uppdercase and lowercase English letters"""
        if input.isupper():
            return (65, 90)
        else:
            return (97, 122)