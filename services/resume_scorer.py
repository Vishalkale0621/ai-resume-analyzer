import re


def calculate_resume_score(text, skills):
    """
    Calculate a resume score out of 100.

    Categories:
    Skills       = 30
    Experience   = 25
    Education    = 15
    Projects     = 15
    Sections     = 15
    """

    text_lower = text.lower()

    # -----------------------------
    # 1. Skills Score - 30 points
    # -----------------------------

    skill_count = len(skills)

    if skill_count >= 10:
        skill_score = 30
    elif skill_count >= 7:
        skill_score = 25
    elif skill_count >= 5:
        skill_score = 20
    elif skill_count >= 3:
        skill_score = 15
    elif skill_count >= 1:
        skill_score = 10
    else:
        skill_score = 0

    # -----------------------------
    # 2. Experience Score - 25 points
    # -----------------------------

    experience_keywords = [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "intern",
        "worked",
        "responsibilities"
    ]

    experience_found = any(
        keyword in text_lower
        for keyword in experience_keywords
    )

    experience_score = 25 if experience_found else 5

    # -----------------------------
    # 3. Education Score - 15 points
    # -----------------------------

    education_keywords = [
        "education",
        "bachelor",
        "master",
        "degree",
        "college",
        "university",
        "b.tech",
        "b.e",
        "m.tech",
        "mba",
        "diploma"
    ]

    education_found = any(
        keyword in text_lower
        for keyword in education_keywords
    )

    education_score = 15 if education_found else 0

    # -----------------------------
    # 4. Projects Score - 15 points
    # -----------------------------

    project_keywords = [
        "projects",
        "project",
        "developed",
        "built",
        "implemented",
        "created"
    ]

    project_found = any(
        keyword in text_lower
        for keyword in project_keywords
    )

    project_score = 15 if project_found else 0

    # -----------------------------
    # 5. Resume Sections - 15 points
    # -----------------------------

    sections = [
        "summary",
        "skills",
        "experience",
        "education",
        "projects",
        "certifications",
        "contact"
    ]

    sections_found = sum(
        1 for section in sections
        if section in text_lower
    )

    section_score = min(
        sections_found * 3,
        15
    )

    # -----------------------------
    # Total Score
    # -----------------------------

    total_score = (
        skill_score
        + experience_score
        + education_score
        + project_score
        + section_score
    )

    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    if skill_score < 25:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if not experience_found:
        suggestions.append(
            "Add your work experience or internship experience."
        )

    if not education_found:
        suggestions.append(
            "Add your education details."
        )

    if not project_found:
        suggestions.append(
            "Add 2-3 technical projects with measurable results."
        )

    if sections_found < 5:
        suggestions.append(
            "Improve your resume structure with clear sections."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has a good overall structure. Keep improving measurable achievements."
        )

    return {
        "total": total_score,
        "skills": skill_score,
        "experience": experience_score,
        "education": education_score,
        "projects": project_score,
        "sections": section_score,
        "suggestions": suggestions
    }