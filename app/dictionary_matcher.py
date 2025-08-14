import re
from load_skill_dictionary import load_skill_dictionary
from rapidfuzz import fuzz
import pprint

SKILL_DICTIONARY = load_skill_dictionary()

def match_skills_dictionary(text: str, threshold=85):
    """
    Match skills from SKILL_DICTIONARY in the given text.
    Returns a sorted list of matched skills (normalized lowercase).
    """
    text_lower = text.lower()
    matches_normalized = set()

    # Exact match using word boundaries
    exact_matched_norms = set()
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2:
            continue
        if re.search(rf"\b{re.escape(norm_clean)}\b", text_lower):
            matches_normalized.add(norm_clean)
            exact_matched_norms.add(norm_clean)

    # Fuzzy match for skills not matched exactly
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2:
            continue
        if norm_clean in exact_matched_norms:
            continue
        score = fuzz.partial_ratio(norm_clean, text_lower)
        if score >= threshold:
            matches_normalized.add(norm_clean)

    return sorted(matches_normalized)
