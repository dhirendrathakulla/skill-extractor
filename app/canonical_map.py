import re
from data.role_suffixes import role_suffixes
from load_skill_dictionary import load_skill_dictionary
from config import CANONICAL_DATA_MAP

SKILL_DICTIONARY = load_skill_dictionary()

def normalize_skill(skill):
    """Returns tuple: (match_key, display_value) with canonical mapping applied."""
    if not isinstance(skill, str):
        return None, None
    
    display_value = skill.strip().lower()
    if display_value.startswith('##'):
        return None, None

    # Remove punctuation but keep spaces for display_value
    clean_value = re.sub(r'[^\w\s]', '', display_value)
    clean_value = re.sub(r'\s+', ' ', clean_value).strip()

    # Check for role suffix stripping
    words = clean_value.split()
    if len(words) > 1 and words[-1] in role_suffixes:
        base = " ".join(words[:-1])
        base_no_space = base.replace(" ", "")
        if base_no_space in CANONICAL_DATA_MAP or base in SKILL_DICTIONARY:
            clean_value = base

    # Canonical mapping check with spaces
    if clean_value in CANONICAL_DATA_MAP:
        clean_value = CANONICAL_DATA_MAP[clean_value]

    # Create match key (no spaces)
    match_key = clean_value.replace(" ", "")
    # Canonical mapping check without spaces
    if match_key in CANONICAL_DATA_MAP:
        match_key = CANONICAL_DATA_MAP[match_key].replace(" ", "")

    return match_key, clean_value

def merge_and_deduplicate(*skill_lists):
    """Merge skills, deduplicate by match_key, keep readable form."""
    seen = set()
    merged = []
    
    for skills in skill_lists:
        for skill in skills:
            match_key, display_value = normalize_skill(skill)
            if match_key and match_key not in seen:
                seen.add(match_key)
                merged.append(display_value)
    return merged
