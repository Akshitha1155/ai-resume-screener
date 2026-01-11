def extract_job_description(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


if __name__ == "__main__":
    jd_path = "../data/job_descriptions/data_analyst.txt"
    jd_text = extract_job_description(jd_path)

    print("----- JOB DESCRIPTION -----")
    print(jd_text)
