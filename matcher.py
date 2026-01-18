from src.skill_extractor import load_skills, extract_skills
from src.roadmap import generate_roadmap
from src.ats_checker import ats_score
from src.semantic_matcher import semantic_skill_match
import os


def match_skills(resume_text, jd_text):
    # Resolve skills file path safely
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_file = os.path.join(BASE_DIR, "data", "skills.csv")

    # Load skills list
    skills = load_skills(skill_file)

    # Extract skills
    resume_skills = list(set(extract_skills(resume_text, skills)))
    jd_skills = list(set(extract_skills(jd_text, skills)))

    # Exact keyword matches
    exact_matches = list(set(resume_skills).intersection(set(jd_skills)))

    # Remaining JD skills after exact match
    remaining_jd_skills = list(set(jd_skills) - set(exact_matches))

    # Semantic matching
    semantic_matches, _ = semantic_skill_match(
        resume_skills,
        remaining_jd_skills
    )

    # Skills matched semantically (JD side)
    semantic_matched_jd_skills = [jd for jd, _ in semantic_matches]

    # Final matched skills
    final_matched_skills = exact_matches + semantic_matched_jd_skills

    # Final missing skills (CORRECT LOGIC)
    final_missing_skills = list(set(jd_skills) - set(final_matched_skills))

    # Match score
    match_score = (
        (len(final_matched_skills) / len(jd_skills)) * 100
        if len(jd_skills) > 0 else 0
    )

    # ATS score
    ats = ats_score(resume_text, jd_skills)

    # Learning roadmap
    roadmap = generate_roadmap(final_missing_skills)

    return {
        "matched_skills": final_matched_skills,
        "semantic_matches": semantic_matches,
        "missing_skills": final_missing_skills,
        "match_score": match_score,
        "ats_score": ats,
        "roadmap": roadmap
    }
