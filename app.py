import streamlit as st
import tempfile
import os

# Import your project logic
from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import load_skills, extract_skills
from src.roadmap import generate_roadmap
from src.ats_checker import ats_score

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("🧠 AI Resume Screening System")
st.write("Upload your resume and paste the job description to get an AI-based analysis.")

st.markdown("---")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

# Job description input
jd_text = st.text_area(
    "Paste Job Description Here",
    height=200,
    placeholder="Paste the job description..."
)

analyze_btn = st.button("Analyze Resume")

if analyze_btn:
    if resume_file is None or jd_text.strip() == "":
        st.error("Please upload a resume and paste the job description.")
    else:
        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(resume_file.read())
            resume_path = tmp.name

        # Load skills list
        skills = load_skills("data/skills.csv")

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path)

        # Extract skills
        resume_skills = set(extract_skills(resume_text, skills))
        jd_skills = set(extract_skills(jd_text, skills))

        # Compare
        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills

        # Match score
        if len(jd_skills) > 0:
            match_score = (len(matched_skills) / len(jd_skills)) * 100
        else:
            match_score = 0

        # ATS score
        ats = ats_score(resume_text, jd_skills)

        # Learning roadmap
        roadmap = generate_roadmap(missing_skills)
        st.write("DEBUG ROADMAP:", roadmap)

        # --- DISPLAY RESULTS ---
        st.success("Analysis Completed Successfully!")

        st.subheader("Scores")
        st.write(f"**Match Score:** {match_score:.2f}%")
        st.write(f"**ATS Compatibility Score:** {ats:.2f}%")

        st.subheader(" Matched Skills")
        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matched skills found.")

        st.subheader(" Missing Skills")

    if missing_skills:
        st.write(", ".join(sorted(missing_skills)))
    else:
        st.success("No missing skills . Resume fully matches the job!")


