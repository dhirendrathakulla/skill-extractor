import re
import spacy
from data.excluded_words import excluded_words  # your custom list

# --- Load SpaCy model ---
nlp = spacy.load("en_core_web_sm")
excluded_words_set = set(word.lower() for word in excluded_words)

# --- Regex patterns ---
# Case 1: "X years ... experience" (loose gap allowed)
YEARS_BEFORE_EXP = re.compile(
    r"\b\d+\s*\+?\s*(?:years?|yrs?|yr)\b(?:\s+\w+){0,6}?\s*\b(?:experience|exp|exper|experienced)\b",
    re.IGNORECASE
)

# Case 2: "experience/experienced ... X years" or "experienced X years"
EXP_BEFORE_YEARS = re.compile(
    r"\b(?:experience|exp|exper|experienced)\b(?:\s+\w+){0,6}?\s*\b\d+\s*\+?\s*(?:years?|yrs?|yr)\b",
    re.IGNORECASE
)

# Case 3: Plain "X years" (only for experience)
YEARS_ONLY = re.compile(
    r"\b\d+\s*\+?\s*(?:years?|yrs?|yr)\b",
    re.IGNORECASE
)

# --- Strict patterns for numeric extraction ---
STRICT_ANY = re.compile(r"(\d+)", re.IGNORECASE)

def _norm_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def _extract_year_number(phrase: str):
    """Extract the first integer found in phrase."""
    m = STRICT_ANY.search(phrase)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None

def extract_filtered_noun_chunks_and_experience(text: str):
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    doc = nlp(text)
    results = set()
    exp_numbers = set()

    # --- 1) Find all experience patterns ---
    for raw_line in text.splitlines():
        line = raw_line.lower()

        matches = []
        matches.extend(YEARS_BEFORE_EXP.findall(line))
        matches.extend(EXP_BEFORE_YEARS.findall(line))

        if matches:
            for phrase in matches:
                num = _extract_year_number(phrase)
                if num is not None and num not in exp_numbers:
                    results.add(f"experience:{num}")
                    exp_numbers.add(num)
        else:
            # If no explicit experience match, fallback to plain years
            for phrase in YEARS_ONLY.findall(line):
                num = _extract_year_number(phrase)
                if num is not None and num not in exp_numbers:
                    results.add(f"experience:{num}")
                    exp_numbers.add(num)

    # --- 2) Noun-chunk extraction ---
    for chunk in doc.noun_chunks:
        phrase = chunk.text
        phrase_lower = _norm_spaces(phrase)
        if (
            1 <= len(phrase_lower.split()) <= 2
            and phrase_lower not in excluded_words_set
            and phrase_lower not in nlp.Defaults.stop_words
        ):
            results.add(phrase_lower)

    return list(results)
