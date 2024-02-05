"""This test varifies that the jumble-text.py and unjumble-text.py scripts work correctly."""
import pytest

from genius_privacy_tweak import GeniusPrivacyTweak

@pytest.fixture
def gpt(input="text"):
    return GeniusPrivacyTweak()

def test_gpt_swaps_character_correctly():
    """
    Test that a character is swapped correctly.
    Valid unicode code points are:
    - 65 to 90 uppercase letters (26)
    - 97 to 122 lowercase letters (26)
    """
    assert GeniusPrivacyTweak.swap_character(char='.', shift=13) == "."
    assert GeniusPrivacyTweak.swap_character(char='D', shift=13) == "Q"
    assert GeniusPrivacyTweak.swap_character(char='h', shift=-13) == "u"
    assert GeniusPrivacyTweak.swap_character(char='@', shift=-13) == "@"

def test_characters_before_beginning_or_after_end_of_alphabet_are_wrapped():
    """
    Test that characters before the beginning or after the end of the alphabet are wrapped.
    In reality we're just making sure that character prior to 'a' are wrapped to 'z' and
    characters after 'z' are wrapped to 'a'. This only tests ASCII.
    """
    # after end of alphabet wrap to beginning
    assert GeniusPrivacyTweak.swap_character(char='X', shift=4) == "B"
    # This on starts on the last letter, testing for off-by-one errors
    assert GeniusPrivacyTweak.swap_character(char='z', shift=3) == "c"
    # This one lands on the first letter, testing for off-by-one errors
    assert GeniusPrivacyTweak.swap_character(char='X', shift=3) == "A"

    # Start on the first and land on the last
    assert GeniusPrivacyTweak.swap_character(char='a', shift=25) == "z"
    
    # Start on the first and end on the first (basically, never going to happen but testing for off-by-one errors)
    assert GeniusPrivacyTweak.swap_character(char='a', shift=26) == "a"
    # Start on the last and land on the first
    assert GeniusPrivacyTweak.swap_character(char='z', shift=1) == "a"
    # before beginning of alphabet wrap to end (reverse shifting)
    assert GeniusPrivacyTweak.swap_character(char='B', shift=-4) == "X"
    assert GeniusPrivacyTweak.swap_character(char='c', shift=-3) == "z"
    assert GeniusPrivacyTweak.swap_character(char='A', shift=-3) == "X"

    # Issue with 'Gbqnl' being translated as 'Tod{y'
    assert GeniusPrivacyTweak.swap_character(char='n', shift=13) == "a"

def test_gpt_encode_english():
    """Test that the obfuscator can encode from English"""
    gpt = GeniusPrivacyTweak(
        input="Today"
    )
    assert gpt.encode() == "Gbqnl"

def test_gpt_decode_to_english_13():
    """Test that the obfuscator can decode to English shifted by 13"""
    gpt = GeniusPrivacyTweak(
        input="Gbqnl",
        shift=13
    )
    assert gpt.decode() == "Today"

def test_gpt_decode_to_english_4():
    """Test that the obfuscator can decode to English shifted by 4"""
    gpt = GeniusPrivacyTweak(
        input="Xshec",
        shift=4
    )
    assert gpt.decode() == "Today"

def test_gpt_decode_to_english_22():
    """Test that the obfuscator can decode to English shifted by 22"""
    gpt = GeniusPrivacyTweak(
        input="Pkzwu",
        shift=22
    )
    assert gpt.decode() == "Today"

def test_gpt_decode_to_english_minus_1():
    """Test that the obfuscator can decode to English shifted by -1"""
    gpt = GeniusPrivacyTweak(
        input="Snczx",
        shift=-1
    )
    assert gpt.decode() == "Today"

def test_obfuscating_skips_symbols_and_punctuation():
    """Test that the obfuscator skips symbols and punctuation"""
    gpt = GeniusPrivacyTweak(
        input="Today is the first day of the rest of your life. first@today.com!",
    )
    assert gpt.encode() == "Gbqnl vf gur svefg qnl bs gur erfg bs lbhe yvsr. svefg@gbqnl.pbz!"
