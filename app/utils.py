# utils.py
import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_skill(skill):
    """Lowercase, strip, remove extra spaces & non-alphanumeric edges."""
    if not isinstance(skill, str):
        return None
    skill = skill.lower()
    skill = re.sub(r'\s+', ' ', skill).strip()
    skill = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', skill)
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

