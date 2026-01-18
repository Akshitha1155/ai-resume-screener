import sys
import os
import tempfile
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_PATH = os.path.join(BASE_DIR, "data", "skills.csv")

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st

from resume_parser import extract_text_from_pdf
from matcher import match_skills


st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("🧠 AI Resume Screening System (Advanced)")
st.write(
    "Upload your resume and paste the job description to get an AI-based analysis "
    "with semantic skill matching."
)

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

        # Extract resume text
        resume_text = extract_text_from_pdf(resume_path)

        # --- CALL ADVANCED MATCHER ---
        result = match_skills(resume_text, jd_text, SKILLS_PATH)

        matched_skills = result["matched_skills"]
        semantic_matches = result["semantic_matches"]
        missing_skills = result["missing_skills"]
        match_score = result["match_score"]
        ats_score = result["ats_score"]
        roadmap = result["roadmap"]

        # Cleanup temp file
        os.remove(resume_path)

        # --- DISPLAY RESULTS ---
        st.success("Analysis Completed Successfully!")

        st.subheader("📊 Scores")
        st.write(f"**Match Score:** {match_score:.2f}%")
        st.write(f"**ATS Compatibility Score:** {ats_score:.2f}%")

        st.subheader("✅ Exact & Final Matched Skills")
        if matched_skills:
            st.write(", ".join(sorted(set(matched_skills))))
        else:
            st.write("No exact matches found.")

        if semantic_matches:
            st.subheader("🧠 Semantic Matched Skills")
            for jd_skill, resume_skill in semantic_matches:
                st.write(f"{jd_skill} ↔ {resume_skill}")

        st.subheader("❌ Missing Skills")

        if missing_skills:
            st.write(", ".join(sorted(missing_skills)))

        elif match_score > 0:
            st.success("No missing skills 🎉 Resume fully matches the job!")

        else:
            st.warning("No skill match found between resume and job description.")


        st.subheader("🎯 Learning Roadmap")
        if roadmap:
            for skill, steps in roadmap.items():
                st.markdown(f"**{skill.upper()}**")
                for step in steps:
                    st.write("•", step)
        else:
            st.info("No roadmap needed.")
