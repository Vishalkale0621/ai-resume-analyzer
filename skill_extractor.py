import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


# Skills database
SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "sql",
    "mysql",
    "oracle",
    "mongodb",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "data science",
    "nlp",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "communication",
    "problem solving",
    "troubleshooting",
    "customer service"
]


def extract_skills(text):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))