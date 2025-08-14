import re
from load_skill_dictionary import load_skill_dictionary
from rapidfuzz import fuzz
from utils import normalize_skill  # your shared normalizer
from config import CANONICAL_DATA_MAP

SKILL_DICTIONARY = load_skill_dictionary()

# Single words that are too ambiguous to match alone
AMBIGUOUS_SINGLETONS = {
    "edge", "works", "forms"  # extend as needed
}

def match_skills_dictionary(text: str, threshold=85):
    """
    - Phrase matching uses a text view where in-word hyphens are turned into spaces
      (e.g., 'full-stack' -> 'full stack'), so dictionary phrases match reliably.
    - Single-word exact matching uses the original text but forbids hyphen-adjacent hits,
      so 'leading-edge' won't trigger 'edge'.
    - Fuzzy matching is applied to multi-word skills only.
    - Canonical mapping is applied at the end.
    """
    # Two text views:
    text_lower = text.lower()
    # For phrases: convert hyphens that are between word chars into spaces
    #  'full-stack' -> 'full stack', 'state-of-the-art' -> 'state of the art'
    #  'AWS - EC2' stays 'aws - ec2' (spaces around hyphen are preserved)
    text_for_phrase = re.sub(r'(?<=\w)-(?=\w)', ' ', text_lower)

    matches_normalized = set()
    exact_matched_norms = set()

    # Precompute which entries are multi-word (include hyphenated entries from dict if any)
    multi_word_entries = set()
    for k in SKILL_DICTIONARY.keys():
        k_clean = k.strip().lower()
        if " " in k_clean or "-" in k_clean:
            multi_word_entries.add(k_clean)

    # --- Exact match phase ---
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2:
            continue

        # Multi-word (or hyphenated) skills → match on phrase view
        if " " in norm_clean or "-" in norm_clean:
            if re.search(rf"\b{re.escape(norm_clean)}\b", text_for_phrase):
                matches_normalized.add(norm_clean)
                exact_matched_norms.add(norm_clean)
            continue

        # Single-word skills → block ambiguous singletons unless explicitly wanted
        if norm_clean in AMBIGUOUS_SINGLETONS:
            continue

        # Single-word exact match on original text,
        # but forbid hyphen-adjacent matches (e.g., leading-edge)
        pattern = rf"(?<!-)\b{re.escape(norm_clean)}\b(?!-)"
        if re.search(pattern, text_lower):
            matches_normalized.add(norm_clean)
            exact_matched_norms.add(norm_clean)

    # --- Fuzzy match phase (multi-word only) ---
    for norm, _ in SKILL_DICTIONARY.items():
        norm_clean = norm.strip().lower()
        if len(norm_clean) < 2 or norm_clean in exact_matched_norms:
            continue
        if " " not in norm_clean and "-" not in norm_clean:
            continue  # skip single-word fuzzy

        score = fuzz.partial_ratio(norm_clean, text_for_phrase)
        if score >= threshold:
            matches_normalized.add(norm_clean)

    # --- Canonical mapping ---
    final_skills = set(CANONICAL_DATA_MAP.get(s, s) for s in matches_normalized)
    return sorted(final_skills)
