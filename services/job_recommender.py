# services/job_recommender.py

ROLE_SKILLS = {
    "Python Developer": [
        "python",
        "sql",
        "git",
        "github",
        "docker"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "pandas",
        "numpy",
        "power bi",
        "tableau",
        "data analysis"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "data science"
    ],

    "Machine Learning Engineer": [
        "python",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "machine learning",
        "deep learning",
        "docker"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "git",
        "github"
    ],

    "Cloud Engineer": [
        "linux",
        "docker",
        "aws",
        "azure",
        "gcp",
        "git"
    ],

    "Technical Support Engineer": [
        "linux",
        "communication",
        "problem solving",
        "troubleshooting",
        "customer service",
        "technical support"
    ]
}


def recommend_roles(resume_skills):

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    recommendations = []

    for role, required_skills in ROLE_SKILLS.items():

        required_set = set(required_skills)

        matched_skills = resume_set.intersection(
            required_set
        )

        missing_skills = required_set.difference(
            resume_set
        )

        if required_set:

            score = round(
                (len(matched_skills) / len(required_set))
                * 100
            )

        else:
            score = 0

        recommendations.append({
            "role": role,
            "score": score,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills)
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations