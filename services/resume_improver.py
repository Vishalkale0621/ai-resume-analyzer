# services/resume_improver.py


def generate_resume_improvements(
    resume_text,
    resume_skills,
    job_skills,
    missing_skills,
    resume_score
):

    suggestions = []

    # --------------------------------
    # Missing Skills
    # --------------------------------

    if missing_skills:

        important_missing = missing_skills[:6]

        suggestions.append(
            "Consider adding these job-relevant skills "
            "if you genuinely have experience with them: "
            + ", ".join(
                skill.title()
                for skill in important_missing
            )
            + "."
        )

    # --------------------------------
    # Resume Score
    # --------------------------------

    if resume_score < 60:

        suggestions.append(
            "Your resume score is below 60. "
            "Improve the structure, skills, projects, "
            "education and experience sections."
        )

    elif resume_score < 80:

        suggestions.append(
            "Your resume has a good foundation. "
            "Add measurable achievements and more "
            "job-specific keywords to strengthen it."
        )

    else:

        suggestions.append(
            "Your resume has a strong overall structure. "
            "Focus on tailoring it to each job description."
        )

    # --------------------------------
    # Project Recommendation
    # --------------------------------

    project_keywords = [
        "python",
        "machine learning",
        "data analysis",
        "sql",
        "pandas"
    ]

    relevant_project_skills = [
        skill for skill in project_keywords
        if skill in job_skills
    ]

    if relevant_project_skills:

        suggestions.append(
            "Add a project demonstrating: "
            + ", ".join(
                skill.title()
                for skill in relevant_project_skills
            )
            + "."
        )

    # --------------------------------
    # Experience Recommendation
    # --------------------------------

    text_lower = resume_text.lower()

    if "experience" not in text_lower:

        suggestions.append(
            "Add a clear Work Experience section. "
            "Include your responsibilities and measurable results."
        )

    # --------------------------------
    # Achievement Recommendation
    # --------------------------------

    achievement_words = [
        "%",
        "increased",
        "reduced",
        "improved",
        "achieved",
        "saved",
        "optimized"
    ]

    has_achievements = any(
        word in text_lower
        for word in achievement_words
    )

    if not has_achievements:

        suggestions.append(
            "Add measurable achievements. "
            "For example: improved performance by 20% "
            "or reduced processing time by 30%."
        )

    return suggestions