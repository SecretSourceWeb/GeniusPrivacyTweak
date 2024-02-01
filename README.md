# Genius Privacy Tweak (GPT)

This is a python module that can be used to obfuscate data sent to LLMs. It uses a technique known as [Homomorphic Encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) to obfuscate data in a way that the LLM can still create valid completions while the data itself is gibberish. This works because an LLM is just a completion engine and does not need to understand the data it is completing. It just needs to be able to predict what comes next.

Different LLMs will have different levels of success with this technique. For example, GPT-4 does a pretty good job of completing obfuscated data, but GPT-3.5 does not. That said, depending on your fine tuning and the data you are obfuscating, you may be able to get good results with GPT-3.5 or other LLMs.

The idea for this project came from my experimentation with [the Microsoft Presidio project](https://python.langchain.com/docs/guides/privacy/presidio_data_anonymization/reversible). I was unhappy with the results I was getting from Presidio. Specifically, processing time was significantly increased, like 2x or more (mostly more) and it included calls to the LLM prior to submitting the data. I wondered if I could use something like [pig latin](https://en.wikipedia.org/wiki/Pig_Latin) to obfuscate PII but rather than bother pulling out just those pieces of PII, just obfuscate everything. I also wanted to see if I could do it in a way that was not easily reversible. Currently this project uses a [Ceaser cipher](https://en.wikipedia.org/wiki/Caesar_cipher) because it produces English-ish (similar to English) output. The current implementation only supports ASCII characters. The cipher can be decrypted via brute force because, in the current implementation, the maximum shift is 25 characters (although you can shift in either direction). In spite of these shortcomings, I believe this module provides the protection most people require (good enough).

## Setup

This project has a Dockerfile to make testing easy. You can build the docker image and bring up the container by running the following command:

```bash
docker-compose up -d
```

and then enter the container by running the following command:

```bash
docker exec -ti $(docker ps | grep 'geniusprivacytweak' | cut -d' ' -f1) /bin/bash
```

In order to make this work reliably, you need to fine tune an existing model. You can generate the training data by running the following command:

```bash
python jumple-text.py <filename-of-english-words>
```

This will output a file called jumbled-text.json.

