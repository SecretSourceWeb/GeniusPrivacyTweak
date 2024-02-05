# Genius Privacy Tweak (GPT)

This is a Proof of Concept (PoC) that can be used to obfuscate data sent to LLMs. It uses a technique known as [Homomorphic Encryption](https://en.wikipedia.org/wiki/Homomorphic_encryption) to obfuscate data in a way that the LLM can still create valid completions while the data itself is gibberish. This works because an LLM is just a completion engine and does not need to understand the data it is completing. It just needs to be able to predict what comes next.

## Example

**User query:** "I've created a proof of concept for obfuscating PII when sending it to an LLM and will release it as open source. Will this help my company get business?"

**User query in ficticious language:** "J'wf dsfbufe b qsppg pg dpodfqu gps pcgvtdbujoh QJJ xifo tfoejoh ju up bo MMN boe xjmm sfmfbtf ju bt pqfo tpvsdf. Xjmm uijt ifmq nz dpnqboz hfu cvtjoftt?"

**LLM's response in ficticious language:** "J'wf dsfbufe b qsppg pg dpodfqu gps pcgvtdbujoh QJJ xifo tfoejoh ju up bo LLN boe xjmm sfmfbtf ju bt pqfo tpvsdf. Xjmm uijt ifmq nz dpnqboz hfu cvtjoftt?

Yft, sfmfbtjoh zpvs qsppg pg dpodfqu bt pqfo tpvsdf dbo qptjujwfmz jnqbdu zpvs dpnqboz't bcjmjuz up hfu cvtjoftt jo tfwfsbm xbzt. Ju fodpvsbhft dpmmbcpsbujpo boe jowftunfou gspn uif efwfmpqfs dpnnvojuz, jodsfbtft wjtjcjmjuz, boe dbo mfbe up ofx qbsuofstijqt ps dvtupnfs sfmbujpotijqt. Bttvnjoh uif qsppg pg dpodfqu jt xfmm-sfdfjwfe, ju dbo bmtp ifmq ftubcmjti zpvs dpnqboz bt b mfbefs jo joevtusz joeopwbujpo."

**LLM's response in English:** "I've created a proof of concept for obfuscating PII when sending it to an KKM and will release it as open source. Will this help my company get business?

Xes, releasing your proof of concept as open source can positively impact your company's ability to get business in several ways. It encourages collaboration and investment from the developer community, increases visibility, and can lead to new partnerships or customer relationships. Assuming the proof of concept is well-received, it can also help establish your company as a leader in industry indnovation."

----

The example above was created using GPT-4. Different LLMs will have different levels of success with this technique. For example, GPT-4 does a pretty good job of completing obfuscated data, but GPT-3.5 does not. That said, depending on your prompt and the data you are obfuscating, you may be able to get good results with GPT-3.5 or other LLMs.

## Background

This came to me because one day I was thinking about how to protect PII in a way that was not easily reversible. I had been toying with the idea for a while and thought, "The problem reminds me of speaking pig latin in front of children." and then it occurred to me: GPT is simply a pattern recognition engine, and a really complex and powerful one at that. I'll bet I could obfuscate the data in such a way that it would still be able to predict the next word in a sentence. I was right. It works. It's not perfect, but it's good enough for most people's needs.

The idea for this project came from my experimentation with [the Microsoft Presidio project](https://python.langchain.com/docs/guides/privacy/presidio_data_anonymization/reversible). I was unhappy with the results I was getting from Presidio. Specifically, processing time was significantly increased, like 2x or more (mostly more) and it included calls to the LLM prior to submitting the data. I wondered if I could use something like [pig latin](https://en.wikipedia.org/wiki/Pig_Latin) to obfuscate PII but rather than bother pulling out just those pieces of PII, just obfuscate everything. I also wanted to see if I could do it in a way that was not easily reversible. Currently this project uses a [Ceaser cipher](https://en.wikipedia.org/wiki/Caesar_cipher) because it produces English-ish (similar to English) output. The current implementation only supports ASCII characters. The cipher can be decrypted via brute force because, in the current implementation, the maximum shift is 25 characters (although you can shift in either direction). In spite of these shortcomings, I believe this module provides the protection most people require (good enough).

We haven't done much testing but what little we've done shows that some "shift" values work better than others. For example, shifting by 1 or 13 seems to work pretty well but shifting by 7, for example, returns very poor results.

We've tried including training data in the system prompt to help the LLM figure out how many places the data has been shifted, but this doesn't seem to help. That said, we wonder if using this on a fine tuned model might improve results, especially for numbers like 7. We haven't tried that yet.

This project is sponsored by [Secret Source Technology - A tech team you'll love working with](https://www.secret-source.eu/). We offer dev team augmentation, custom software development, and consulting services. We have a team of 20+ developers, designers, and project managers. We have been in business for over 10 years and have worked with clients all over the world. We are experts in Python, React, TypeScript, Node, Express, NestJS, Laravel, C# .Net Core and much more, and more. We can help you with your next project. [Contact us today!](https://www.secret-source.eu/connect/)

![Secret Source Technology - A tech team you'll love working with](https://media.licdn.com/dms/image/D4D16AQGH4LVPJ5oboQ/profile-displaybackgroundimage-shrink_350_1400/0/1688397476732?e=1712188800&v=beta&t=lFnHVi7IDnSsCPdA64nD54zuRFZVYMZ0fGGrf12U1ks)

## Setup

This project has a Dockerfile to make testing easy. You need to create a `.env` file in the root of the project. Copy and past `env.sample` and change the values to make your life easy.

You can build the docker image and bring up the container by running the following command:

```bash
docker-compose up -d
```

and then enter the container by running the following command:

```bash
docker exec -ti $(docker ps | grep 'geniusprivacytweak' | cut -d' ' -f1) /bin/bash
```

Once inside the container, you can run the following command to test the module:

```bash
python demo.py --query "Do LLMs support Homomorphic Encryption?"
```

