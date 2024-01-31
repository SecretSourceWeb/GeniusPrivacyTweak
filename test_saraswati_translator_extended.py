"""This test varifies that the jumble-text.py and unjumble-text.py scripts work correctly."""
import pytest

from translator.saraswati_translator import SaraswatiTranslator

@pytest.fixture
def saraswati_translator(input="text", output_lang="Saraswati"):
    return SaraswatiTranslator(input="text", output_lang="Saraswati")

def test_saraswati_translator_swaps_character_correctly():
    """
    Test that a character is swapped correctly.
    Valid unicode code points are:
    - 65 to 90 uppercase letters (26)
    - 97 to 122 lowercase letters (26)
    - 192 to 214 (23), 216 to 246 (31) and 248 to 255 (8) accented letters
    - 256 to 328 (73) accented letters
    - 330 to 447 (118) accented letters
    """
    assert SaraswatiTranslator.swap_character(char='á', shift=13) == "î"
    assert SaraswatiTranslator.swap_character(char='.', shift=13) == "."
    assert SaraswatiTranslator.swap_character(char='ê', shift=13) == "ø"
    assert SaraswatiTranslator.swap_character(char='X', shift=13) == "k"
    assert SaraswatiTranslator.swap_character(char='P', shift=13) == "c"
    assert SaraswatiTranslator.swap_character(char='w', shift=-13) == "j"
    assert SaraswatiTranslator.swap_character(char='g', shift=-13) == "T"

def test_characters_before_beginning_or_after_end_of_alphabet_are_wrapped():
    """
    Test that characters before the beginning or after the end of the alphabet are wrapped.
    In reality we're just making sure that character prior to 'a' are wrapped to 'z' and
    characters after 'z' are wrapped to 'a', but we're testing the full range of unicode.
    """
    # after end of alphabet wrap to beginning
    assert SaraswatiTranslator.swap_character(char='Ź', shift=13) == "G"
    assert SaraswatiTranslator.swap_character(char='ž', shift=2) == "A"
    # before beginning of alphabet wrap to end (reverse shifting)
    assert SaraswatiTranslator.swap_character(char='M', shift=-13) == "ſ"
    assert SaraswatiTranslator.swap_character(char='A', shift=-1) == "ſ"
    assert SaraswatiTranslator.swap_character(char='A', shift=-10) == "Ŷ"

def test_saraswati_translator_english_to_saraswati():
    """Test that the saraswati translator can translate from English to Saraswati"""
    saraswati_translator = SaraswatiTranslator(
        input="Today",
        output_lang="Saraswati"
    )
    assert saraswati_translator.translate() == "gµqnÈ"

def test_saraswati_translator_saraswati_to_english():
    """Test that the saraswati translator can translate from Saraswati to English"""
    saraswati_translator = SaraswatiTranslator(
        input="gµqnÈ",
        output_lang="English"
    )
    assert saraswati_translator.translate() == "Today"

def test_translation_supports_symbols_and_punctuation():
    """Test that the saraswati translator can translate symbols and punctuation"""
    saraswati_translator = SaraswatiTranslator(
        input="Today is the first day of the rest of your life. first@today.com",
        output_lang="Saraswati"
    )
    assert saraswati_translator.translate() == "gµqnÈ vÂ Ãur svÁÂÃ qnÈ µs Ãur ÁrÂÃ µs ÈµÄÁ yvsr. svÁÂÃ@ÃµqnÈ.pµz"

def test_translation_supports_utf8():
    """Test that the saraswati translator can translate utf-8 characters, including accented characters and emojis"""
    saraswati_translator = SaraswatiTranslator(
        input="Today is the first day of the rest of your life. áÁñÑçÇ¿ 🎉",
        output_lang="Saraswati"
    )
    assert saraswati_translator.translate() == "gµqnÈ vÂ Ãur svÁÂÃ qnÈ µs Ãur ÁrÂÃ µs ÈµÄÁ yvsr. îÎÿßôÔ¿ 🎉"