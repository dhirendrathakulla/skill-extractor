from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, Pipeline
from typing import List, Optional
import logging
import spacy
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import threading

# -----------------------------------
# Logger setup
# -----------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ner-api")

# -----------------------------------
# FastAPI App
# -----------------------------------
app = FastAPI(title="NER API", version="1.3")

# -----------------------------------
# Pydantic Models
# -----------------------------------
class NERRequest(BaseModel):
    text: str

class NEREntity(BaseModel):
    entity_group: str
    word: str
    score: float
    start: Optional[int] = None
    end: Optional[int] = None

class NERResponse(BaseModel):
    entities: List[NEREntity]

# -----------------------------------
# Load Models at Startup
# -----------------------------------
try:
    logger.info("Loading NER model...")
    ner_pipeline: Pipeline = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)
    logger.info("NER model loaded.")

    logger.info("Loading spaCy NLP model...")
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy NLP model loaded.")
except Exception as e:
    logger.exception("Model loading failed.")
    raise RuntimeError(f"Failed to load models: {e}")

# -----------------------------------
# Globals for dynamic filtering
# -----------------------------------
phrase_counter = Counter()
phrase_lock = threading.Lock()

# -----------------------------------
# Helper: Deduplicate substrings
# -----------------------------------
def deduplicate_phrases(entities: List[NEREntity]) -> List[NEREntity]:
    """
    Remove duplicates and substrings (case-insensitive), keeping longest phrases first.
    """
    sorted_entities = sorted(entities, key=lambda e: len(e.word), reverse=True)
    result = []
    seen = []

    for entity in sorted_entities:
        lw = entity.word.lower()
        if not any(lw in s for s in seen if lw != s):
            result.append(entity)
            seen.append(lw)
    return result

# -----------------------------------
# Dynamic phrase frequency update
# -----------------------------------
def update_phrase_counts(phrases: List[str]):
    with phrase_lock:
        phrase_counter.update([p.lower() for p in phrases])

# -----------------------------------
# API Route
# -----------------------------------
@app.post("/ner", response_model=NERResponse)
async def extract_entities(request: NERRequest):
    logger.info(f"Received text (first 100 chars): {request.text[:100]}")
    try:
        # HuggingFace NER
        raw_results = ner_pipeline(request.text)

        # spaCy phrase extraction
        doc = nlp(request.text)
        spacy_phrases = set()

        # Load custom excluded words
        from excluded_words import excluded_words
        excluded_words_set = set(word.lower() for word in excluded_words)

        # POS tags to exclude
        excluded_pos = {"PRON", "DET", "ADP", "CCONJ", "SCONJ", "PART", "INTJ", "SYM"}

        # Filtered noun chunks
        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip()
            phrase_lower = phrase.lower()
            if (
                1 <= len(phrase.split()) <= 4
                and phrase_lower not in excluded_words_set
                and phrase_lower not in nlp.Defaults.stop_words
            ):
                spacy_phrases.add(phrase)

        # Filtered individual noun/proper noun tokens
        for token in doc:
            token_text = token.text.strip().lower()
            if (
                token.pos_ in {"NOUN", "PROPN"}
                and token_text not in nlp.Defaults.stop_words
                and token.pos_ not in excluded_pos
                and token_text not in excluded_words_set
                and len(token_text) > 2
            ):
                spacy_phrases.add(token.text.strip())

        # Convert HuggingFace results
        ner_entities = [
            NEREntity(
                entity_group=ent.get("entity_group", "NER"),
                word=ent.get("word"),
                score=ent.get("score"),
                start=ent.get("start"),
                end=ent.get("end")
            )
            for ent in raw_results
        ]

        # Add spaCy phrases (high confidence) with start/end positions
        for phrase in spacy_phrases:
            start = request.text.find(phrase)
            end = start + len(phrase) if start != -1 else None
            ner_entities.append(
                NEREntity(
                    entity_group="PHRASE",
                    word=phrase,
                    score=1.0,
                    start=start,
                    end=end
                )
            )

        # Remove exact duplicates
        unique_words = {}
        for entity in ner_entities:
            key = entity.word.strip().lower()
            if key not in unique_words:
                unique_words[key] = entity

        all_entities = list(unique_words.values())

        # Track phrase frequency for optional use
        update_phrase_counts([e.word for e in all_entities])

        # Final deduplication (e.g., "cloud" and "cloud infrastructure")
        deduplicated_entities = deduplicate_phrases(all_entities)

        return {"entities": deduplicated_entities}

    except Exception as e:
        logger.exception("Error in NER endpoint")
        raise HTTPException(status_code=500, detail=str(e))
