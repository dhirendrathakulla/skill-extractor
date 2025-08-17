from config import NER_MODEL, CANONICAL_DATA_MAP
from data.excluded_words import excluded_words
from typing import List, Dict

excluded_words_set = set(word.lower() for word in excluded_words)

def extract_skills_ner(text: str) -> List[str]:
    """
    Extract skills using NER model with:
    - Excluded words filtering
    - Canonical mapping
    - Case-insensitive deduplication
    """
    if not isinstance(text, str):
        return []

    entities = NER_MODEL(text)
    skills = []
    seen_skills = set()
    
    for ent in entities:
        entity_group = ent.get("entity_group", "").upper()
        if entity_group not in {"HSKILL", "SSKILL"}:
            continue
            
        raw_skill = ent["word"].strip()
        if not raw_skill:
            continue
            
        # Normalize and check exclusions
        skill_lower = raw_skill.lower()
        if skill_lower in excluded_words_set:
            continue
            
        # Apply canonical mapping if exists
        canonical_skill = CANONICAL_DATA_MAP.get(skill_lower, raw_skill)
        canonical_key = canonical_skill.lower()
        
        # Deduplicate
        if canonical_key not in seen_skills:
            seen_skills.add(canonical_key)
            skills.append(canonical_skill)
    
    return skills