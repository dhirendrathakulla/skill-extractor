import pandas as pd
import re
from pathlib import Path

def normalize_skill(skill):
    """Lowercase, strip, remove extra spaces & non-alphanumeric edges."""
    if not isinstance(skill, str):
        return None
    skill = skill.lower()
    skill = re.sub(r'\s+', ' ', skill).strip()
    skill = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', skill)
    return skill

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
            norm = normalize_skill(val)
            if norm and norm not in all_skills:
                all_skills[norm] = val  # normalized → original

    return all_skills  # keep as dict for .items() use
