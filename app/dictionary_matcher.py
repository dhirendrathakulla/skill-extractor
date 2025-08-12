from load_skill_dictionary import load_skill_dictionary
from rapidfuzz import fuzz
import pprint

SKILL_DICTIONARY = load_skill_dictionary()  # {normalized: original}

print("DEBUG: SKILL_DICTIONARY type ->", type(SKILL_DICTIONARY))
try:
    print("DEBUG: length ->", len(SKILL_DICTIONARY))
except Exception as e:
    print("DEBUG: len() error ->", e)

if isinstance(SKILL_DICTIONARY, dict):
    print("DEBUG: sample items (first 20):")
    pprint.pprint(list(SKILL_DICTIONARY.items())[:20])
else:
    print("DEBUG: not a dict, sample:")
    pprint.pprint(SKILL_DICTIONARY[:20])



def match_skills_dictionary(text: str, threshold=85):
    text_lower = text.lower()
    matches = set()
    # Exact substring match
    exact_matched_norms = set()
    for norm, original in SKILL_DICTIONARY.items():
        if len(norm) < 2:
            continue  # skip short normalized keys
        if norm in text_lower:
            matches.add(original)
            exact_matched_norms.add(norm)

    # Fuzzy match for those not matched exactly
    for norm, original in SKILL_DICTIONARY.items():
        if len(norm) < 2:
            continue  # skip short normalized keys
        if norm in exact_matched_norms:
            continue
        score = fuzz.partial_ratio(norm, text_lower)
        if score >= threshold:
            matches.add(original)

    return sorted(matches)
