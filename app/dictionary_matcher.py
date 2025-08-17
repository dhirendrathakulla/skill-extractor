from typing import List, Optional, Set, Dict
import re
from rapidfuzz import fuzz
from load_skill_dictionary import load_skill_dictionary
from config import CANONICAL_DATA_MAP
from data.excluded_words import excluded_words

# Initialize global dictionaries
SKILL_DICTIONARY = load_skill_dictionary()
excluded_words_set = set(word.lower() for word in excluded_words)

def normalize_skill(skill: str) -> tuple:
    """Normalize skill name for consistent comparison"""
    if not isinstance(skill, str):
        return None, None
    
    # Basic normalization
    normalized = skill.strip().lower()
    normalized = re.sub(r'[^\w\s-]', '', normalized)  # Remove punctuation
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized.replace(" ", "").replace("-", ""), normalized

def match_skills_dictionary(text: str, ner_skills: Optional[List[str]] = None, threshold: int = 85) -> List[str]:
    """
    Production-grade skill matcher that:
    1. Ignores NER-extracted skills
    2. Respects excluded_words
    3. Uses exact + fuzzy matching
    4. Applies canonical mapping
    
    Args:
        text: Input text to analyze
        ner_skills: List of skills already found by NER
        threshold: Fuzzy matching threshold (0-100)
    
    Returns:
        List of matched skills (canonical form)
    """
    # Normalize NER skills for exclusion
    ner_normalized = set()
    for skill in ner_skills:
        _, norm = normalize_skill(skill)
        if norm and norm not in excluded_words_set:
            ner_normalized.add(norm)
    
    # Prepare text views
    text_lower = text.lower()
    text_for_phrase = re.sub(r'(?<=\w)-(?=\w)', ' ', text_lower)
    
    matches = set()
    exact_matches = set()

    # --- Phase 1: Exact Matching ---
    for dict_skill, _ in SKILL_DICTIONARY.items():
        skill_lower = dict_skill.lower()
        
        # Skip conditions
        if (len(skill_lower) < 2 or
            skill_lower in ner_normalized or
            skill_lower in excluded_words_set):
            continue

        # Multi-word matching
        if " " in skill_lower or "-" in skill_lower:
            if re.search(rf'\b{re.escape(skill_lower)}\b', text_for_phrase):
                matches.add(skill_lower)
                exact_matches.add(skill_lower)
            continue

        # Single-word exact matching (hyphen-protected)
        if re.search(rf'(?<!-)\b{re.escape(skill_lower)}\b(?!-)', text_lower):
            matches.add(skill_lower)
            exact_matches.add(skill_lower)

    # --- Phase 2: Fuzzy Matching ---
    for dict_skill, _ in SKILL_DICTIONARY.items():
        skill_lower = dict_skill.lower()
        if (len(skill_lower) < 2 or
            skill_lower in exact_matches or
            skill_lower in ner_normalized or
            skill_lower in excluded_words_set or
            (" " not in skill_lower and "-" not in skill_lower)):
            continue

        score = fuzz.partial_ratio(skill_lower, text_for_phrase)
        if score >= threshold:
            matches.add(skill_lower)

    # Apply canonical mapping
    return sorted({CANONICAL_DATA_MAP.get(s, s) for s in matches})