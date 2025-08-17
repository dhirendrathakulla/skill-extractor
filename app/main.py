# main.py
from fastapi import FastAPI, Request
from logger import logger
from dictionary_matcher import match_skills_dictionary
from utils import clean_text
from ner_extractor import extract_skills_ner
from spacy_extract_noun import extract_filtered_noun_chunks_and_experience
from canonical_map import merge_and_deduplicate

app = FastAPI()

@app.post("/extract_skills")
async def extract_skills_endpoint(request: Request):
    try:
        data = await request.json()
        text = clean_text(data.get("text", ""))

        logger.info(f"Received text: {text[:100]}...")  # Log first 100 chars

        ner_skills = extract_skills_ner(text)
        dict_skills = match_skills_dictionary(text, ner_skills)
        spacy_skills = extract_filtered_noun_chunks_and_experience(text,ner_skills + dict_skills)

        logger.info(f"Ner skills: {ner_skills}")
        logger.info(f"Dict skills: {dict_skills}")
        logger.info(f"Spacy skills: {spacy_skills}")

        combined = merge_and_deduplicate(
            ner_skills + dict_skills + spacy_skills
        )

        return {"skills": combined, "count": len(combined)}

    except Exception as e:
        logger.exception("Error in skill extraction endpoint")
        return {"error": str(e)}
