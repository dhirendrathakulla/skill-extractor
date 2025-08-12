sudo docker build -t ner-api .
sudo docker run -p 8010:8010 ner-api



NER API (FastAPI + HuggingFace + dictionary)
A high-performance Named Entity Recognition (NER) API built with FastAPI, HuggingFace Transformers, and dictionary. It extracts named entities and relevant phrases from text input while filtering out irrelevant or uninformative tokens like "who", "what", etc.


 Features
Named entity recognition using HuggingFace's dslim/bert-base-NER

Phrase extraction using dictionary noun chunks and noun/proper noun tokens

Stopword and irrelevant word filtering via excluded_words.py

Deduplication of overlapping or substring phrases

Phrase frequency tracking (optional use case)

Clean API response with entity group, phrase, confidence score, and position

