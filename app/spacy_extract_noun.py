import re
import spacy
from data.excluded_words import excluded_words  # your custom list

nlp = spacy.load("en_core_web_sm")
excluded_words_set = set(word.lower() for word in excluded_words)

# --- Patterns ---
YEARS_PATTERN = re.compile(r"\b(\d+)\s*\+?\s*(?:years?|yrs?|yr)\b", re.IGNORECASE)

EXPERIENCE_YEARS_BEFORE = re.compile(
    r"\b(\d+)\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)"
    r"(?:\s+of\b.*?)?\b(?:experience|exp|exper|experienced)\b",
    re.IGNORECASE | re.DOTALL,
)

EXPERIENCE_EXP_BEFORE = re.compile(
    r"\b(?:experience|exp|exper|experienced)\b.*?\b(\d+)\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)\b",
    re.IGNORECASE | re.DOTALL,
)

YEAR_ONLY_FULL = re.compile(
    r"^\s*\d+\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)\s*$",
    re.IGNORECASE,
)

def _norm_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def extract_filtered_noun_chunks_and_experience(text: str):
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    doc = nlp(text)
    results = set()
    exp_numbers = set()

    # --- 1) Match explicit experience patterns anywhere in text ---
    for m in EXPERIENCE_YEARS_BEFORE.finditer(text):
        try:
            num = int(m.group(1))
        except Exception:
            continue
        if num not in exp_numbers:
            results.add(f"experience {num}")
            exp_numbers.add(num)

    for m in EXPERIENCE_EXP_BEFORE.finditer(text):
        try:
            num = int(m.group(1))
        except Exception:
            continue
        if num not in exp_numbers:
            results.add(f"experience {num}")
            exp_numbers.add(num)

    # --- 2) Fallback: plain years (only if no matching experience phrase) ---
    for m in YEARS_PATTERN.finditer(text):
        try:
            num = int(m.group(1))
        except Exception:
            continue
        if num not in exp_numbers:
            results.add(f"experience {num}")
            exp_numbers.add(num)

    # --- 3) Noun-chunk extraction ---
    for chunk in doc.noun_chunks:
        phrase_lower = _norm_spaces(chunk.text)
        if phrase_lower in nlp.Defaults.stop_words or phrase_lower in excluded_words_set:
            continue
        if not (1 <= len(phrase_lower.split()) <= 2):
            continue
        if YEAR_ONLY_FULL.match(phrase_lower):
            continue
        results.add(phrase_lower)

    # --- 4) Final cleanup ---
    final_list = [s for s in results if not YEAR_ONLY_FULL.match(s)]
    return final_list
