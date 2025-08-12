from fastapi import FastAPI, Request
from dictionary_matcher import match_skills_dictionary
from utils import clean_text, deduplicate
from ner_extractor import extract_skills_ner

app = FastAPI()

@app.post("/extract_skills")
async def extract_skills_endpoint(request: Request):
    data = await request.json()
    text = clean_text(data.get("text", ""))

    ner_skills = extract_skills_ner(text)
    dict_skills = match_skills_dictionary(text)

    combined = deduplicate(ner_skills + dict_skills)
    return {
        "skills": combined,
        "count": len(combined)
    }
