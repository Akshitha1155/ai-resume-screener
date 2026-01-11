import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


if __name__ == "__main__":
    resume_folder = "../data/resumes"

    for file_name in os.listdir(resume_folder):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(resume_folder, file_name)
            print("-----", file_name, "-----")
            resume_text = extract_text_from_pdf(file_path)
            print(resume_text[:500])
