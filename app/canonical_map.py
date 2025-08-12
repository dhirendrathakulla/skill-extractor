import re
from data.conanical_words import canonical_map

def normalize_skill(skill):
    skill = skill.lower()
    skill = re.sub(r'[^\w\s]', '', skill)  # remove punctuation
    skill = re.sub(r'\s+', '', skill)      # remove spaces
    return canonical_map.get(skill, skill)

def merge_and_deduplicate(*skill_lists):
    seen = set()
    merged = []

    for skills in skill_lists:
        for skill in skills:
            norm = normalize_skill(skill)
            if norm not in seen:
                seen.add(norm)
                merged.append(skill)
    return merged
