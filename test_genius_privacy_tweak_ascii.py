"""This test varifies that the jumble-text.py and unjumble-text.py scripts work correctly."""
import pytest

from genius_privacy_tweak import GeniusPrivacyTweak

@pytest.fixture
def gpt(input="text", output_lang="Saraswati"):
    return GeniusPrivacyTweak(input="text", output_lang="Saraswati")

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

def test_gpt_english_to_saraswati():
    """Test that the saraswati translator can translate from English to Saraswati"""
    gpt = GeniusPrivacyTweak(
        input="Today",
        output_lang="Saraswati"
    )
    assert gpt.translate() == "Gbqnl"

def test_gpt_saraswati_to_english_13():
    """Test that the saraswati translator can translate from Saraswati to English"""
    gpt = GeniusPrivacyTweak(
        input="Gbqnl",
        output_lang="English",
        shift=13
    )
    assert gpt.translate() == "Today"

def test_gpt_saraswati_to_english_4():
    """Test that the saraswati translator can translate from Saraswati to English"""
    gpt = GeniusPrivacyTweak(
        input="Xshec",
        output_lang="English",
        shift=4
    )
    assert gpt.translate() == "Today"

def test_gpt_saraswati_to_english_22():
    """Test that the saraswati translator can translate from Saraswati to English"""
    gpt = GeniusPrivacyTweak(
        input="Pkzwu",
        output_lang="English",
        shift=22
    )
    assert gpt.translate() == "Today"

def test_translation_supports_symbols_and_punctuation():
    """Test that the saraswati translator can translate symbols and punctuation"""
    gpt = GeniusPrivacyTweak(
        input="Today is the first day of the rest of your life. first@today.com!",
        output_lang="Saraswati"
    )
    assert gpt.translate() == "Gbqnl vf gur svefg qnl bs gur erfg bs lbhe yvsr. svefg@gbqnl.pbz!"

@pytest.mark.skip(reason="Not implemented yet")
def test_translation_supports_utf8():
    """Test that the saraswati translator can translate utf-8 characters, including accented characters and emojis"""
    gpt = GeniusPrivacyTweak(
        input="Today is the first day of the rest of your life. áÁñÑçÇ¿ 🎉",
        output_lang="Saraswati"
    )
    assert gpt.translate() == "gµqnÈ vÂ Ãur svÁÂÃ qnÈ µs Ãur ÁrÂÃ µs ÈµÄÁ yvsr. îÎÿßôÔ¿ 🎉"