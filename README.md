# Saraswati Translator

This is a tool that converts a user's query into a ficticious language that looks like English, but isn't. Instead, it is just jumbled up text. Technically, it is _not_ jumbled (random) but rather follows a pattern that an LLM can understand given a little training or fine tuning. This could be considered a cipher, but one of the simplest kind, probably hackable with enough brute force, somewhat like md5.

I am creating this module as a way of obfuscating data being sent to LLMs without crippling the LLM's ability to understand the data and respond. This project is inspired by [the Microsoft Presidio project](https://python.langchain.com/docs/guides/privacy/presidio_data_anonymization/reversible). As LLMs are just completion engines and they clearly understand a wide variety of inputs, I am hoping that this tool will be able to obfuscate data in a way that is not easily reversible, but still understandable by the LLM.

The approach uses something similar to a Ceaser cipher in which the user defines the number of characters (and direction) to shift the alphabet.