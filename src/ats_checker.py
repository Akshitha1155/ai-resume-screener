def ats_score(resume_text, required_skills):
    score = 0

    # Rule 1: Length check
    if len(resume_text) > 300:
        score += 30

    # Rule 2: Skill keyword coverage
    skill_matches = 0
    for skill in required_skills:
        if skill in resume_text.lower():
            skill_matches += 1

    if len(required_skills) > 0:
        score += (skill_matches / len(required_skills)) * 50

    # Rule 3: Sections check
    sections = ["experience", "education", "skills", "projects"]
    section_count = sum(1 for sec in sections if sec in resume_text.lower())

    score += section_count * 5

    return min(score, 100)


if __name__ == "__main__":
    sample_text = "Skills: Python SQL Machine Learning Education Experience Projects"
    sample_skills = ["python", "sql", "machine learning"]

    print("ATS Score:", ats_score(sample_text, sample_skills))
