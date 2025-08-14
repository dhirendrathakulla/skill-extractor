import re
from load_skill_dictionary import load_skill_dictionary
from rapidfuzz import fuzz
from utils import normalize_skill  # ensure same normalization everywhere

from data.conanical_words import canonical_map

SKILL_DICTIONARY = load_skill_dictionary()

def match_skills_dictionary(text: str, threshold=85):
    """
    Match skills from SKILL_DICTIONARY in the given text.
    - Single-word skills: exact match only
    - Multi-word skills: exact + fuzzy match
    - Applies canonical_map to unify synonyms
    """
    text_lower = text.lower()
    matches_normalized = set()

    # --- Exact match phase ---
    exact_matched_norms = set()
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2:
            continue

        if re.search(rf"\b{re.escape(norm_clean)}\b", text_lower):
            matches_normalized.add(norm_clean)
            exact_matched_norms.add(norm_clean)

    # --- Fuzzy match phase (multi-word only) ---
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2 or norm_clean in exact_matched_norms:
            continue

        if " " not in norm_clean:  # skip single-word fuzzy
            continue

        score = fuzz.partial_ratio(norm_clean, text_lower)
        if score >= threshold:
            matches_normalized.add(norm_clean)

    # --- Apply canonical mapping ---
    final_skills = set()
    for skill in matches_normalized:
        if skill in canonical_map:
            final_skills.add(canonical_map[skill])
        else:
            final_skills.add(skill)

    return sorted(final_skills)
