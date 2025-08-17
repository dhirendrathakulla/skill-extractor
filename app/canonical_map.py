import re
import json
from pathlib import Path
from data.role_suffixes import role_suffixes
from load_skill_dictionary import load_skill_dictionary
from config import CANONICAL_DATA_MAP
from data.excluded_words import excluded_words  # Your custom exclusion list

excluded_words_set = set(word.lower() for word in excluded_words)
SKILL_DICTIONARY = load_skill_dictionary()

# ---------------------------
# Load context rules (JSON-based)
# ---------------------------
RULES_PATH = Path(__file__).parent / "data" / "contextual_rules.json"
if RULES_PATH.exists():
    with open(RULES_PATH) as f:
        CONTEXTUAL_RULES = json.load(f)
else:
    CONTEXTUAL_RULES = {}

# ---------------------------
# Normalization
# ---------------------------
def normalize_skill(skill):
    """Returns tuple: (match_key, display_value) with canonical mapping applied."""
    if not isinstance(skill, str):
        return None, None
    
    display_value = skill.strip().lower()
    if display_value.startswith('##'):
        return None, None

    # remove punctuation but keep hyphen/space
    clean_value = re.sub(r"[^\w\s-]", "", display_value)
    clean_value = re.sub(r"\s+", " ", clean_value).strip()

    # Skip excluded words
    if clean_value in excluded_words_set:
        return None, None

    # Handle role suffix stripping (e.g., "developer", "engineer")
    words = clean_value.split()
    if len(words) > 1 and words[-1] in role_suffixes:
        base = " ".join(words[:-1])
        base_no_space = base.replace(" ", "").replace("-", "")
        if len(base_no_space) >= 3 and (
            base_no_space in CANONICAL_DATA_MAP or base in SKILL_DICTIONARY
        ):
            clean_value = base

    # Canonical mapping with spaces
    if clean_value in CANONICAL_DATA_MAP:
        clean_value = CANONICAL_DATA_MAP[clean_value]

    # Create match key (no space/hyphen)
    match_key = clean_value.replace(" ", "").replace("-", "")

    # Canonical mapping without spaces
    if match_key in CANONICAL_DATA_MAP:
        match_key = CANONICAL_DATA_MAP[match_key].replace(" ", "").replace("-", "")

    # Avoid false positives for very short single words
    if " " not in clean_value and len(clean_value) < 2:
        return None, None

    return match_key, clean_value

# ---------------------------
# Merge & Deduplicate + Apply Context Rules
# ---------------------------
def merge_and_deduplicate(*skill_lists):
    """Merge skills, deduplicate by match_key, then apply contextual rules."""
    seen = set()
    merged = []
    
    for skills in skill_lists:
        for skill in skills:
            if not isinstance(skill, str):
                continue
                
            skill_lower = skill.strip().lower()
            if skill_lower in excluded_words_set:
                continue
                
            match_key, display_value = normalize_skill(skill)
            if match_key and match_key not in seen:
                seen.add(match_key)
                merged.append(display_value)

    # ---------------------------
    # Context-based merging rules (from JSON config)
    # ---------------------------
    merged_lower = set(s.lower() for s in merged)

    for combo, replacement in CONTEXTUAL_RULES.items():
        parts = [p.strip().lower() for p in combo.split("+")]
        if all(p in merged_lower for p in parts):
            # Remove the parts
            merged = [s for s in merged if s.lower() not in parts]
            # Add the canonical replacement (normalized too)
            _, replacement_norm = normalize_skill(replacement)
            if replacement_norm and replacement_norm not in merged:
                merged.append(replacement_norm)

    return merged
