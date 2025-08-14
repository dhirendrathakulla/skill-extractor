# config.py
from pathlib import Path
from transformers import pipeline
from data.canonical_words import canonical_map
# === Paths ===
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SKILLS_FILE_XLSX = DATA_DIR / "skills.xlsx"
TECH_SKILLS_FILE_XLSX = DATA_DIR / "tech_skills.xlsx"


CANONICAL_DATA_MAP = {k.strip(): v for k, v in canonical_map.items()}


# === Models (loaded once at startup) ===
NER_MODEL = pipeline(
    "ner",
    model="Nucha/Nucha_SkillNER_BERT",
    aggregation_strategy="simple"
)
