# utils.py
import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def deduplicate(skills):
    seen = set()
    result = []
    for s in skills:
        norm = s.lower()
        if norm not in seen:
            seen.add(norm)
            result.append(s)
    return result
