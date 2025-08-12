from fastapi import FastAPI, Request
from dictionary_matcher import match_skills_dictionary
from utils import clean_text, deduplicate
from ner_extractor import extract_skills_ner
from spacy_extract_noun import extract_filtered_noun_chunks
from canonical_map import merge_and_deduplicate

app = FastAPI()

@app.post("/extract_skills")
async def extract_skills_endpoint(request: Request):
    data = await request.json()
    text = clean_text(data.get("text", ""))

    ner_skills = extract_skills_ner(text)
    dict_skills = match_skills_dictionary(text)
    spacy_skill = extract_filtered_noun_chunks(text)
    print("ner_skills === ",ner_skills)
    print("dict_skills === ",dict_skills)
    print("spacy_skills === ",spacy_skill)
    combined = merge_and_deduplicate(ner_skills + dict_skills + spacy_skill)
    return {
        "skills": combined,
        "count": len(combined)
    }
