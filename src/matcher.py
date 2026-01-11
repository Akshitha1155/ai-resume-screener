from resume_parser import extract_text_from_pdf
from jd_parser import extract_job_description
from roadmap import generate_roadmap
from ats_checker import ats_score
from skill_extractor import load_skills, extract_skills
import os

if __name__ == "__main__":
    # Paths
    resume_path = "../data/resumes/Resume1.pdf"
    jd_path = "../data/job_descriptions/data_analyst.txt"
    skill_file = "../data/skills.csv"

    # Load skills list
    skills = load_skills(skill_file)

    # Extract texts
    resume_text = extract_text_from_pdf(resume_path)
    jd_text = extract_job_description(jd_path)

    # Extract skills
    resume_skills = set(extract_skills(resume_text, skills))
    jd_skills = set(extract_skills(jd_text, skills))

    # Compare
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills

    print("Resume Skills:", resume_skills)
    print("Job Required Skills:", jd_skills)
    print("\nMatched Skills:", matched_skills)
    print("Missing Skills:", missing_skills)
    # Match score
    if len(jd_skills) > 0:
        match_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        match_score = 0

    print(f"\nMatch Score: {match_score:.2f}%")
    
    # ATS Compatibility Score
    ats = ats_score(resume_text, jd_skills)
    print(f"\nATS Compatibility Score: {ats:.2f}%")

    
# Generate learning roadmap
roadmap = generate_roadmap(missing_skills)

print("\n--- Learning Roadmap ---")
for skill, steps in roadmap.items():
    print(f"\n{skill.upper()}:")
    for step in steps:
        print(" -", step)



