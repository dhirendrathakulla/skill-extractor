# utils.py
import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_skill(skill):
    skill = skill.lower()
    skill = re.sub(r'[\.\-\s]+', '', skill)  # remove dots, dashes, spaces
    return skill

def deduplicate(skills):
    seen = set()
    result = []
    for s in skills:
        norm = normalize_skill(s)
        if norm not in seen:
            seen.add(norm)
            result.append(s)
    return result

