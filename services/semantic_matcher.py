from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the AI model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_description):

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    semantic_score = round(similarity * 100)

    return semantic_score


def calculate_ai_match(
    resume_text,
    job_description,
    resume_skills,
    job_skills
):

    # -----------------------------
    # Semantic Score
    # -----------------------------

    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description
    )

    # -----------------------------
    # Skill Match Score
    # -----------------------------

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    job_set = set(
        skill.lower()
        for skill in job_skills
    )

    if job_set:

        matched_skills = sorted(
            resume_set.intersection(job_set)
        )

        missing_skills = sorted(
            job_set.difference(resume_set)
        )

        skill_score = round(
            (len(matched_skills) / len(job_set))
            * 100
        )

    else:

        matched_skills = []
        missing_skills = []
        skill_score = 0

    # -----------------------------
    # Overall AI Score
    # -----------------------------

    overall_score = round(
        (semantic_score * 0.5)
        + (skill_score * 0.5)
    )

    # -----------------------------
    # Recommendation
    # -----------------------------

    if overall_score >= 80:

        recommendation = (
            "Excellent match! Your resume is "
            "strongly aligned with this job."
        )

    elif overall_score >= 65:

        recommendation = (
            "Good match! A few skill improvements "
            "could make your resume stronger."
        )

    elif overall_score >= 50:

        recommendation = (
            "Moderate match. Consider improving "
            "your relevant skills and resume content."
        )

    else:

        recommendation = (
            "Your resume needs improvement for "
            "this job. Focus on the missing skills."
        )

    return {
        "overall_score": overall_score,
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation
    }