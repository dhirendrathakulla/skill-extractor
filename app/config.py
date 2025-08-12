# config.py
from pathlib import Path
from transformers import pipeline
from load_skill_dictionary import load_skill_dictionary

# === Paths ===
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SKILLS_FILE_XLSX = DATA_DIR / "skills.xlsx"
TECH_SKILLS_FILE_XLSX = DATA_DIR / "tech_skills.xlsx"

# === Models (loaded once at startup) ===
NER_MODEL = pipeline(
    "ner",
    model="Nucha/Nucha_SkillNER_BERT",
    aggregation_strategy="simple"
)

# === Skill dictionary (deduplicated from Excel) ===
SKILL_DICTIONARY = list(load_skill_dictionary())
