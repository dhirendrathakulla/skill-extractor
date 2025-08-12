import spacy
from data.excluded_words import excluded_words  # your custom list
import re

# Load model and prepare excluded words
nlp = spacy.load("en_core_web_sm")
excluded_words_set = set(word.lower() for word in excluded_words)

def extract_filtered_noun_chunks(text):
    doc = nlp(text)
    spacy_phrases = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        phrase_lower = phrase.lower()
        word_count = len(phrase.split())
        if (
            1 <= word_count <= 2
            and phrase_lower not in excluded_words_set
            and phrase_lower not in nlp.Defaults.stop_words
        ):
            spacy_phrases.add(phrase)
    return list(spacy_phrases)




