import csv

def load_skills(skill_file):
    skills = []
    with open(skill_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                skills.append(row[0].lower())
    return skills


def extract_skills(text, skills):
    text = text.lower()
    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":
    # Sample text (we will replace this later)
    sample_resume_text = """
    I have experience in Python, Machine Learning, Excel and Flask.
    """

    skill_file = "../data/skills.csv"
    skills = load_skills(skill_file)

    extracted = extract_skills(sample_resume_text, skills)

    print("Extracted Skills:")
    print(extracted)
