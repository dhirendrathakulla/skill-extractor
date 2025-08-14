import re
from data.conanical_words import canonical_map

def normalize_skill(skill):
    """Normalizes a skill string without handling typos"""
    if not isinstance(skill, str):
        return None
    
    skill = skill.lower().strip()
    
    # Remove ##-prefixed skills
    if skill.startswith('##'):
        return None
    
    # Remove punctuation and spaces
    skill = re.sub(r'[^\w\s]', '', skill)  # remove punctuation
    skill = re.sub(r'\s+', '', skill)      # remove spaces
    
    return canonical_map.get(skill, skill)

def merge_and_deduplicate(*skill_lists):
    """Merges multiple skill lists with deduplication"""
    seen = set()
    merged = []

    for skills in skill_lists:
        for skill in skills:
            norm = normalize_skill(skill)
            if norm and norm not in seen:  # Explicit None check
                seen.add(norm)
                merged.append(skill)  # Keep original casing
    return merged