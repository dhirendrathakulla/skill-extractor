from config import NER_MODEL

def extract_skills_ner(text: str):
    entities = NER_MODEL(text)
    skills = []
    print("Entities output:", entities)

    for ent in entities:
        entity_group = ent.get("entity_group", "").upper()
        if entity_group in {"HSKILL", "SSKILL"}:  # accept both
            skill_text = ent["word"].strip()
            if skill_text:
                skills.append(skill_text)

    # remove duplicates while preserving order
    seen = set()
    unique_skills = [s for s in skills if not (s.lower() in seen or seen.add(s.lower()))]
    return unique_skills
