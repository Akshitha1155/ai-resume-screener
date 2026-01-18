from sentence_transformers import SentenceTransformer, util
# Skill aliases / normalization map
SKILL_ALIASES = {
    "dbms": ["sql", "mysql", "postgresql", "oracle"],
    "database management system": ["sql", "mysql", "postgresql"],
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "data visualization": ["power bi", "tableau"]
}


# Load SBERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")
def normalize_skill(skill):
    skill = skill.lower().strip()
    for parent, aliases in SKILL_ALIASES.items():
        if skill == parent or skill in aliases:
            return parent
    return skill



def semantic_skill_match(resume_skills, jd_skills, threshold=0.6):
    """
    Returns:
    - semantic_matches: list of tuples (jd_skill, matched_resume_skill)
    - missing_skills: list of jd skills not matched semantically
    """

    semantic_matches = []
    missing_skills = []

    normalized_resume_skills = [normalize_skill(s) for s in resume_skills]
    normalized_jd_skills = [normalize_skill(s) for s in jd_skills]

    resume_embeddings = model.encode(normalized_resume_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(normalized_jd_skills, convert_to_tensor=True)


    for idx, jd_skill in enumerate(jd_skills):
        scores = util.cos_sim(jd_embeddings[idx], resume_embeddings)[0]
        best_score = scores.max().item()
        best_match_index = scores.argmax().item()

        if best_score >= threshold:
            semantic_matches.append(
                (jd_skill, resume_skills[best_match_index])
            )
        else:
            missing_skills.append(jd_skill)

    return semantic_matches, missing_skills
