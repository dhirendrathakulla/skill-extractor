import re
from typing import Set, List, Optional
import spacy
from data.excluded_words import excluded_words  # Your custom exclusion list

nlp = spacy.load("en_core_web_sm")
excluded_words_set = set(word.lower() for word in excluded_words)

# --- Regex Patterns ---
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
YEAR_ONLY_FULL = re.compile(r"^\s*\d+\s*(?:\+|plus)?\s*(?:years?|yrs?|yr)\s*$", re.IGNORECASE)
PERCENTAGE_ONLY = re.compile(r'^\s*\d+%\s*$')

def _norm_spaces(s: str) -> str:
    """Normalize whitespace and lowercase text."""
    return re.sub(r"\s+", " ", s.strip().lower())

def extract_filtered_noun_chunks_and_experience(
    text: str,
    existing_skills: Optional[List[str]] = None
) -> List[str]:
    """
    Enhanced skill extractor that:
    1. Maintains all original filtering logic
    2. Excludes skills from existing_skills list
    3. Preserves experience year extraction
    
    Args:
        text: Input text to process
        existing_skills: List of skills to exclude (NER + previous spaCy results)
    
    Returns:
        List of unique, filtered skills and experience years
    """
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    # Normalize existing skills for exclusion
    excluded_from_processing = set()
    if existing_skills:
        for skill in existing_skills:
            if isinstance(skill, str):
                normalized = _norm_spaces(skill)
                excluded_from_processing.add(normalized)

    doc = nlp(text)
    results: Set[str] = set()
    exp_numbers: Set[int] = set()

    # --- 1) Experience Extraction (unchanged) ---
    for pattern in [EXPERIENCE_YEARS_BEFORE, EXPERIENCE_EXP_BEFORE, YEARS_PATTERN]:
        for match in pattern.finditer(text):
            try:
                num = int(match.group(1))
                if num not in exp_numbers:
                    exp_phrase = f"experience {num}"
                    results.add(exp_phrase)
                    exp_numbers.add(num)
            except (ValueError, IndexError):
                continue

    # --- 2) Noun Chunk Processing with Enhanced Filtering ---
    for chunk in doc.noun_chunks:
        phrase_lower = _norm_spaces(chunk.text)
        
        # Skip conditions (existing + new)
        if (phrase_lower in nlp.Defaults.stop_words or
            phrase_lower in excluded_words_set or
            phrase_lower in excluded_from_processing or  # NEW: Skip existing skills
            PERCENTAGE_ONLY.match(phrase_lower) or
            not (1 <= len(phrase_lower.split()) <= 2) or
            YEAR_ONLY_FULL.match(phrase_lower)):
            continue
            
        results.add(phrase_lower)

    # --- 3) Final Cleanup ---
    return [
        phrase for phrase in results
        if not (YEAR_ONLY_FULL.match(phrase) or PERCENTAGE_ONLY.match(phrase))
    ]