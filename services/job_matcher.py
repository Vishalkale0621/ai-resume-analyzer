import re


# Common technical and professional skills
JOB_SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
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
    "gcp",
    "linux",
    "communication",
    "problem solving",
    "troubleshooting",
    "customer service",
    "technical support",
]


def extract_job_skills(job_description):
    """
    Extract skills mentioned in a job description.
    """

    text = job_description.lower()

    found_skills = []

    for skill in JOB_SKILLS:

        if skill in text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_job_match(resume_skills, job_skills):
    """
    Calculate percentage match between resume skills
    and job description skills.
    """

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    job_set = set(
        skill.lower()
        for skill in job_skills
    )

    if not job_set:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    matched_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set.difference(resume_set)
    )

    match_score = round(
        (len(matched_skills) / len(job_set)) * 100
    )

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }