import pandas as pd
import re
from pathlib import Path
from utils import normalize_skill  # <-- import from your common utils

from data.conanical_words import canonical_map


def expand_skill_variants(skill):
    """Generate normalized variants for better matching."""
    variants = set()
    norm = normalize_skill(skill)
    if not norm:
        return variants

    variants.add(norm)

    # If skill has a canonical form, add it
    if norm in canonical_map:
        variants.add(canonical_map[norm])

    # Add acronym from parentheses (e.g., EC2)
    match = re.search(r"\(([^)]+)\)", skill)
    if match:
        variants.add(normalize_skill(match.group(1)))

    # Remove vendor prefix like 'Amazon', 'Microsoft'
    if ' ' in norm:
        words = norm.split()
        if words[0] in ['amazon', 'microsoft', 'google', 'ibm']:
            variants.add(' '.join(words[1:]))

    return {v for v in variants if v}

def load_skill_dictionary():
    """Load skills from O*NET skills.xlsx and tech_skills.xlsx in /data."""
    base_dir = Path(__file__).parent / "data"
    files = {
        "Skills.xlsx": "Element Name",
        "Technology Skills.xlsx": "Example"
    }

    all_skills = {}
    for file, col_name in files.items():
        file_path = base_dir / file
        if not file_path.exists():
            continue

        df = pd.read_excel(file_path)

        if col_name not in df.columns:
            raise ValueError(f"Expected column '{col_name}' not found in {file}")

        for val in df[col_name].dropna():
            for variant in expand_skill_variants(val):
                if variant not in all_skills:
                    all_skills[variant] = val  # variant → original

    return all_skills  # keep as dict for .items() use
