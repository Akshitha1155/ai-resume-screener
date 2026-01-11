# Simple learning roadmap for skills

LEARNING_ROADMAP = {
    "sql": [
        "Basic SQL queries",
        "Joins and subqueries",
        "Aggregation functions",
        "SQL for data analysis"
    ],
     "machine learning": [
        "Supervised vs Unsupervised learning",
        "Regression and classification",
        "Model evaluation techniques"
    ],
    "data analysis": [
        "Data cleaning techniques",
        "Exploratory Data Analysis (EDA)",
        "Data visualization",
        "Basic statistics"
    ],
    "deep learning": [
        "Neural network basics",
        "CNNs and RNNs",
        "Frameworks like TensorFlow/PyTorch"
    ],
    "power bi": [
        "Power BI interface",
        "Creating dashboards",
        "DAX basics"
    ],
    "statistics": [
        "Descriptive statistics",
        "Probability basics",
        "Hypothesis testing"
    ],
    "rest apis": [
        "HTTP methods",
        "Building APIs with Flask",
        "API authentication"
    ]
}

def generate_roadmap(missing_skills):
    roadmap = {}

    for skill in missing_skills:
        skill_key = skill.lower().strip()

        if skill_key in LEARNING_ROADMAP:
            roadmap[skill_key] = LEARNING_ROADMAP[skill_key]
        else:
            roadmap[skill_key] = [
                "Learn basic concepts",
                "Practice with tutorials",
                "Build a small project using this skill"
            ]

    return roadmap
