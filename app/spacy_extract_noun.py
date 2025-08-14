import re
import spacy
from data.excluded_words import excluded_words  # your custom list

# --- Load SpaCy model and excluded words ---
nlp = spacy.load("en_core_web_sm")
excluded_words_set = set(word.lower() for word in excluded_words)

# --- Regex patterns for extraction (on lowercased lines) ---
YEARS_PATTERN = re.compile(r"\b\d+\s*\+?\s*(?:years?|yrs?|yr)\b", re.IGNORECASE)
EXPERIENCE_PATTERN = re.compile(
    r"\b\d+\s*\+?\s*(?:years?|yrs?|yr)\s*(?:of\s+|in\s+)?(?:experience|exp|exper|experienced)\b",
    re.IGNORECASE
)

# --- Regex patterns for post-processing (on individual phrases) ---
YEAR_ONLY_STRICT = re.compile(r"^\s*(\d+)\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)\s*$", re.IGNORECASE)
EXPERIENCE_STRICT = re.compile(
    r"^\s*(\d+)\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)\s*(?:of\s+|in\s+)?(?:experience|exp|exper|experienced)\s*$",
    re.IGNORECASE
)

def _canonicalize_experience_word(phrase: str) -> str:
    """Normalize 'experienced'/'exp'/'exper' to 'experience'."""
    return re.sub(r"\b(?:experienced|exp|exper)\b", "experience", phrase, flags=re.IGNORECASE)

def _replace_plus_in_year_phrases(phrase: str) -> str:
    """Replace + with ' plus ' ONLY in year/experience phrases."""
    return re.sub(r"(\d+)\+(\s*(?:years?|yrs?|yr))", r"\1 plus\2", phrase, flags=re.IGNORECASE)

def _norm_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def _year_key(phrase: str):
    """
    Extract a key (number of years) from either a year-only phrase or
    an experience phrase. Ignores '+/plus' and unit variants.
    Returns an int or None.
    """
    s = _norm_spaces(phrase)
    m = YEAR_ONLY_STRICT.match(s) or EXPERIENCE_STRICT.match(s)
    if not m:
        return None
    try:
        return int(m.group(1))
    except Exception:
        return None

def remove_redundant_years_experience(skills):
    """
    Remove 'X years' if an 'X years experience' (any variant) also exists.
    Comparison is done by normalized numeric key (ignores +/plus, yr/yrs/years).
    """
    # Build sets of numeric keys present in experience phrases
    exp_keys = set()
    for s in skills:
        if EXPERIENCE_STRICT.match(_norm_spaces(s)):
            k = _year_key(s)
            if k is not None:
                exp_keys.add(k)

    # Keep everything except year-only phrases whose numeric key is in exp_keys
    cleaned = []
    for s in skills:
        s_norm = _norm_spaces(s)
        if YEAR_ONLY_STRICT.match(s_norm):
            k = _year_key(s)
            if k in exp_keys:
                continue  # drop 'X years' if corresponding 'X years experience' exists
        cleaned.append(s)
    return cleaned

def extract_filtered_noun_chunks_and_experience(text: str):
    doc = nlp(text)
    results = set()

    # --- 1) Line-by-line extraction of year/experience phrases ---
    for raw_line in text.splitlines():
        line = raw_line.lower()

        exp_matches = list(EXPERIENCE_PATTERN.finditer(line))
        year_matches = list(YEARS_PATTERN.finditer(line))

        if exp_matches:
            # Prefer the longer experience phrases when present
            for m in exp_matches:
                phrase = m.group(0)
                phrase = _canonicalize_experience_word(phrase)
                phrase = _replace_plus_in_year_phrases(phrase)
                results.add(_norm_spaces(phrase))
        else:
            # Otherwise keep the plain years
            for m in year_matches:
                phrase = m.group(0)
                phrase = _replace_plus_in_year_phrases(phrase)
                results.add(_norm_spaces(phrase))

    # --- 2) Noun-chunk extraction (1–2 words), lowercased ---
    for chunk in doc.noun_chunks:
        phrase = chunk.text
        phrase_lower = _norm_spaces(phrase)
        if (
            1 <= len(phrase_lower.split()) <= 2
            and phrase_lower not in excluded_words_set
            and phrase_lower not in nlp.Defaults.stop_words
        ):
            results.add(phrase_lower)

    # --- 3) Remove redundant 'X years' when 'X years experience' exists ---
    final_list = remove_redundant_years_experience(list(results))
    return final_list
