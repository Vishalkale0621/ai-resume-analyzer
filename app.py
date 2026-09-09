import streamlit as st
import pymupdf
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.skill_extractor import extract_skills
from services.resume_scorer import calculate_resume_score
from services.job_matcher import (
    extract_job_skills,
    calculate_job_match
)

# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 Vishal\'s AI Resume Analyzer</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'Smart Resume Analysis & Career Intelligence'
    '</div>',
    unsafe_allow_html=True
)

# CUSTOM CSS
# =======================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #1e3a8a33, transparent 30%),
        radial-gradient(circle at 90% 20%, #7c3aed33, transparent 30%),
        linear-gradient(135deg,#0f172a,#111827,#1e293b);
    background-size:200% 200%;
    animation:bgMove 12s ease infinite;
}

@keyframes bgMove {
    0%,100% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
}

.main .block-container {
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:4rem;
    animation:fadeUp .8s ease;
}

@keyframes fadeUp {
    from {opacity:0;transform:translateY(20px);}
    to {opacity:1;transform:translateY(0);}
}

/* TITLE */

.main-title {
    text-align:center;
    font-size:3rem;
    font-weight:800;
    margin-bottom:.3rem;
    background:linear-gradient(
        90deg,#38bdf8,#818cf8,#c084fc,#22d3ee,#38bdf8
    );
    background-size:300%;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:shine 5s linear infinite,float 3s ease-in-out infinite;
}

@keyframes shine {
    to {background-position:300% center;}
}

@keyframes float {
    50% {transform:translateY(-5px);}
}

.subtitle {
    text-align:center;
    font-size:1.2rem;
    color:#94a3b8;
    margin-bottom:2rem;
    animation:fadeUp 1.2s ease;
}

h2,h3 {
    font-weight:700 !important;
    animation:fadeUp .7s ease;
}

/* METRICS */

[data-testid="stMetric"] {
    background:#ffffff0f;
    border:1px solid #ffffff1a;
    border-radius:16px;
    padding:1rem;
    transition:.3s;
    animation:cardIn .7s ease;
}

[data-testid="stMetric"]:hover {
    transform:translateY(-6px) scale(1.02);
    box-shadow:0 12px 30px #3b82f633;
}

@keyframes cardIn {
    from {opacity:0;transform:scale(.95);}
    to {opacity:1;transform:scale(1);}
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background:#ffffff0d;
    border:1px solid #ffffff1f;
    border-radius:16px;
    padding:1rem;
    transition:.3s;
}

[data-testid="stFileUploader"]:hover {
    transform:translateY(-3px);
    box-shadow:0 10px 30px #3b82f633;
}

/* TEXT AREA */

textarea {
    border-radius:12px !important;
    transition:.3s;
}

textarea:focus {
    box-shadow:0 0 0 2px #60a5fa55 !important;
}

/* ALERTS */

[data-testid="stAlert"] {
    border-radius:14px;
    animation:fadeUp .6s ease;
}

/* PROGRESS */

[data-testid="stProgress"] {
    animation:progressIn 1s ease;
}

@keyframes progressIn {
    from {transform:scaleX(0);transform-origin:left;}
    to {transform:scaleX(1);}
}

/* MOBILE */

@media(max-width:768px) {
    .main-title {font-size:2.1rem;}
    .subtitle {font-size:1rem;}
    .main .block-container {
        padding-left:1rem;
        padding-right:1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📌 About")

    st.write(
        """
        This application analyzes your resume and helps you
        understand your career readiness.
        """
    )

    st.markdown("---")

    st.write("### 🔍 What it analyzes")

    st.write("📄 Resume text")
    st.write("🧠 Skills")
    st.write("📊 Resume health")
    st.write("🎯 Job matching")
    st.write("🤖 AI-style semantic matching")
    st.write("💼 Recommended roles")
    st.write("📝 Improvement suggestions")

    st.markdown("---")

    st.caption(
        "Tip: Upload a text-based PDF resume for the best results."
    )

# RESUME UPLOAD
# =========================================================

st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
    help="Upload your resume in PDF format."
)


# STOP IF NO RESUME
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Upload your resume PDF above to start the analysis."
    )

    st.markdown("---")

    st.subheader("🚀 How it works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.write("### 1️⃣ Upload")
        st.write(
            "Upload your resume as a PDF."
        )

    with step2:
        st.write("### 2️⃣ Analyze")
        st.write(
            "The system extracts your skills and resume information."
        )

    with step3:
        st.write("### 3️⃣ Improve")
        st.write(
            "Compare your resume with jobs and discover missing skills."
        )

    st.stop()


# PROCESS RESUME
# =========================================================

st.success(
    "✅ Resume uploaded successfully — analysis is ready!"
)


# PDF TEXT EXTRACTION
# =========================================================

try:

    pdf_data = uploaded_file.getvalue()

    document = pymupdf.open(
        stream=pdf_data,
        filetype="pdf"
    )

    resume_text = ""

    for page in document:
        resume_text += page.get_text() + "\n"

    document.close()

except Exception as error:

    st.error(
        "❌ Unable to read this PDF."
    )

    st.caption(
        f"Technical details: {error}"
    )

    st.stop()


# Clean extracted text

resume_text = re.sub(
    r"\n{3,}",
    "\n\n",
    resume_text
).strip()


# CHECK PDF TEXT
# =========================================================

if not resume_text:

    st.warning(
        """
        ⚠️ No readable text was found in this PDF.

        This usually happens when the resume is a scanned image.
        Please upload a text-based PDF.
        """
    )

    st.stop()


# RESUME TEXT
# =========================================================

with st.expander("📄 View Extracted Resume Text"):

    st.text_area(
        "Extracted Resume Content",
        resume_text,
        height=350,
        label_visibility="collapsed"
    )


# SKILL DETECTION
# =========================================================

st.header("🧠 Detected Skills")

skills = extract_skills(resume_text)


if skills:

    st.write(
        f"Found **{len(skills)} skills** in your resume."
    )

    columns = st.columns(3)

    for index, skill in enumerate(skills):

        with columns[index % 3]:

            st.success(
                f"✓ {skill.title()}"
            )

else:

    st.warning(
        "No recognized skills were detected."
    )


# RESUME HEALTH SCORE
# =========================================================

st.header("📊 Resume Health Score")

score_data = calculate_resume_score(
    resume_text,
    skills
)

resume_score = score_data["total"]


# Main score

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Resume Score",
        f"{resume_score}/100"
    )

with col2:

    st.metric(
        "Skills Detected",
        len(skills)
    )

with col3:

    if resume_score >= 80:
        status = "Excellent"
    elif resume_score >= 60:
        status = "Good"
    elif resume_score >= 40:
        status = "Needs Work"
    else:
        status = "Needs Improvement"

    st.metric(
        "Resume Status",
        status
    )


# Progress bar

st.progress(
    min(max(resume_score / 100, 0.0), 1.0)
)


# Score message

if resume_score >= 80:

    st.success(
        "⭐ Excellent resume! Your resume has a strong overall structure."
    )

elif resume_score >= 60:

    st.info(
        "👍 Good resume! A few improvements can make it stronger."
    )

else:

    st.warning(
        "⚠️ Your resume needs improvement. Focus on skills, projects, "
        "experience and structure."
    )


# SCORE BREAKDOWN
# =========================================================

st.subheader("📈 Score Breakdown")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "🧠 Skills",
        f"{score_data['skills']}/30"
    )

with col2:

    st.metric(
        "💼 Experience",
        f"{score_data['experience']}/25"
    )

with col3:

    st.metric(
        "🎓 Education",
        f"{score_data['education']}/15"
    )

with col4:

    st.metric(
        "🚀 Projects",
        f"{score_data['projects']}/15"
    )

with col5:

    st.metric(
        "📑 Sections",
        f"{score_data['sections']}/15"
    )


# RESUME IMPROVEMENT SUGGESTIONS
# =========================================================

st.header("💡 Resume Improvement Suggestions")

if score_data["suggestions"]:

    for index, suggestion in enumerate(
        score_data["suggestions"],
        start=1
    ):

        st.info(
            f"💡 {index}. {suggestion}"
        )


# JOB DESCRIPTION MATCHING
# =========================================================

st.header("🎯 Job Description Matching")

st.write(
    """
    Paste a job description below. The application will compare
    the required skills with the skills detected in your resume.
    """
)

job_description = st.text_area(
    "📋 Paste Job Description",
    placeholder=(
        "Example:\n\n"
        "We are looking for a Python Developer with experience "
        "in Python, SQL, Pandas, NumPy, Machine Learning, Git, "
        "Docker and AWS. The candidate should have good "
        "communication and problem solving skills."
    ),
    height=250
)


# JOB ANALYSIS
# =========================================================

if job_description.strip():

    # -----------------------------------------------------
    # Extract Job Skills
    # -----------------------------------------------------

    job_skills = extract_job_skills(
        job_description
    )


    # -----------------------------------------------------
    # Basic Skill Match
    # -----------------------------------------------------

    match_data = calculate_job_match(
        skills,
        job_skills
    )

    basic_match_score = match_data["match_score"]


    # -----------------------------------------------------
    # Job Match Score
    # -----------------------------------------------------

    st.subheader("🎯 Job Match Score")

    st.metric(
        "Skill Match",
        f"{basic_match_score}%"
    )

    st.progress(
        min(max(basic_match_score / 100, 0.0), 1.0)
    )


    if basic_match_score >= 80:

        st.success(
            "🔥 Excellent match! Your skills closely match this job."
        )

    elif basic_match_score >= 60:

        st.info(
            "👍 Good match! You have many of the required skills."
        )

    elif basic_match_score >= 40:

        st.warning(
            "⚠️ Moderate match. Consider developing the missing skills."
        )

    else:

        st.error(
            "❌ Low match. Several job requirements are missing."
        )


    # -----------------------------------------------------
    # Matching Skills
    # -----------------------------------------------------

    st.subheader("✅ Matching Skills")

    matched_skills = match_data["matched_skills"]

    if matched_skills:

        columns = st.columns(3)

        for index, skill in enumerate(matched_skills):

            with columns[index % 3]:

                st.success(
                    f"✓ {skill.title()}"
                )

    else:

        st.info(
            "No matching skills were found."
        )


    # -----------------------------------------------------
    # Missing Skills
    # -----------------------------------------------------

    st.subheader("❌ Skills You Should Learn")

    missing_skills = match_data["missing_skills"]

    if missing_skills:

        columns = st.columns(3)

        for index, skill in enumerate(missing_skills):

            with columns[index % 3]:

                st.error(
                    f"✗ {skill.title()}"
                )

    else:

        st.success(
            "🎉 No major missing skills detected!"
        )


    # -----------------------------------------------------
    # Required Skills
    # -----------------------------------------------------

    st.subheader("📋 Required Job Skills")

    if job_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in job_skills
            )
        )

    else:

        st.warning(
            "No recognized skills were found in this job description."
        )


    # AI-STYLE SEMANTIC MATCH
    # =====================================================

    st.header("🤖 AI Semantic Match")

    st.write(
        """
        This compares the language of your resume with the
        language of the job description using TF-IDF and
        cosine similarity.
        """
    )

    try:

        documents = [
            resume_text,
            job_description
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        semantic_score = round(
            similarity * 100
        )

    except Exception:

        semantic_score = 0


    # -----------------------------------------------------
    # Overall AI Score
    # -----------------------------------------------------

    overall_score = round(
        (semantic_score * 0.5)
        + (basic_match_score * 0.5)
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🧠 Semantic Score",
            f"{semantic_score}%"
        )

    with col2:

        st.metric(
            "🔑 Skill Score",
            f"{basic_match_score}%"
        )

    with col3:

        st.metric(
            "🤖 Overall AI Match",
            f"{overall_score}%"
        )


    st.progress(
        min(max(overall_score / 100, 0.0), 1.0)
    )


    if overall_score >= 80:

        st.success(
            "🚀 Excellent overall match for this job!"
        )

    elif overall_score >= 60:

        st.info(
            "👍 Good overall match. A few improvements could make you stronger."
        )

    elif overall_score >= 40:

        st.warning(
            "⚠️ Moderate match. Focus on the missing job skills."
        )

    else:

        st.error(
            "❌ Your resume currently has a low match with this job."
        )


    # AI RECOMMENDATION
    # =====================================================

    st.header("💡 AI Recommendation")


    if overall_score >= 80:

        recommendation = (
            "Your resume is a strong match for this job. "
            "Focus on measurable achievements and prepare "
            "for technical interviews."
        )

    elif overall_score >= 60:

        recommendation = (
            "Your resume is reasonably aligned with this job. "
            "Improve the missing skills and add projects that "
            "demonstrate the required technologies."
        )

    elif overall_score >= 40:

        recommendation = (
            "Your resume has some relevant skills, but there "
            "is a noticeable gap. Focus on the missing skills "
            "and strengthen your projects and experience."
        )

    else:

        recommendation = (
            "Your resume needs significant improvement for this "
            "job. Start by learning the missing skills and "
            "building practical projects around them."
        )


    if overall_score >= 80:

        st.success(
            recommendation
        )

    elif overall_score >= 50:

        st.info(
            recommendation
        )

    else:

        st.warning(
            recommendation
        )


    # PERSONALIZED IMPROVEMENT PLAN
    # =====================================================

    st.header("📝 Personalized Improvement Plan")


    improvements = []


    # Missing skills

    if missing_skills:

        top_missing = missing_skills[:6]

        improvements.append(
            "Consider learning these job-relevant skills: "
            + ", ".join(
                skill.title()
                for skill in top_missing
            )
            + "."
        )


    # Resume score

    if resume_score < 60:

        improvements.append(
            "Your resume score is below 60. Improve your "
            "skills, projects, education, experience and "
            "overall resume structure."
        )

    elif resume_score < 80:

        improvements.append(
            "Your resume has a good foundation. Add measurable "
            "achievements and stronger project descriptions."
        )

    else:

        improvements.append(
            "Your resume structure is strong. Continue improving "
            "measurable achievements and job-specific keywords."
        )


    # Projects

    if score_data["projects"] < 15:

        improvements.append(
            "Add 2-3 strong projects and explain the technologies "
            "used, your contribution and the result."
        )


    # Experience

    if score_data["experience"] < 25:

        improvements.append(
            "Strengthen your experience section with specific "
            "responsibilities, achievements and measurable results."
        )


    # Education

    if score_data["education"] < 15:

        improvements.append(
            "Add your complete education details, degree, "
            "institution and relevant qualifications."
        )


    # Display improvements

    for index, improvement in enumerate(
        improvements,
        start=1
    ):

        st.info(
            f"💡 {index}. {improvement}"
        )


# =========================================================
# JOB ROLE RECOMMENDATIONS
# =========================================================

st.header("💼 Recommended Job Roles")

st.write(
    "These recommendations are based on the skills detected "
    "in your resume."
)


# Role database

ROLE_DATABASE = {

    "Python Developer": [
        "python",
        "sql",
        "git",
        "pandas",
        "numpy"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "data analysis"
    ],

    "Machine Learning Engineer": [
        "python",
        "pandas",
        "numpy",
        "scikit-learn",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch"
    ],

    "Data Scientist": [
        "python",
        "pandas",
        "numpy",
        "sql",
        "machine learning",
        "data science",
        "statistics"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js"
    ],

    "Database Developer": [
        "sql",
        "mysql",
        "oracle",
        "mongodb"
    ],

    "Cloud / DevOps Engineer": [
        "docker",
        "aws",
        "azure",
        "git",
        "linux"
    ],

    "Technical Support Engineer": [
        "technical support",
        "troubleshooting",
        "communication",
        "customer service",
        "problem solving"
    ]
}


# Normalize resume skills

resume_skill_set = {
    skill.lower()
    for skill in skills
}


role_results = []


for role, required_skills in ROLE_DATABASE.items():

    required_set = {
        skill.lower()
        for skill in required_skills
    }

    matched = sorted(
        resume_skill_set.intersection(
            required_set
        )
    )

    missing = sorted(
        required_set.difference(
            resume_skill_set
        )
    )

    if required_set:

        role_score = round(
            len(matched)
            / len(required_set)
            * 100
        )

    else:

        role_score = 0


    role_results.append(
        {
            "role": role,
            "score": role_score,
            "matched": matched,
            "missing": missing
        }
    )


# Sort roles

role_results.sort(
    key=lambda item: item["score"],
    reverse=True
)


# Display top 5

for index, result in enumerate(
    role_results[:5],
    start=1
):

    role = result["role"]
    role_score = result["score"]
    matched = result["matched"]
    missing = result["missing"]


    st.subheader(
        f"{index}. {role}"
    )


    st.metric(
        "Role Match",
        f"{role_score}%"
    )


    st.progress(
        min(max(role_score / 100, 0.0), 1.0)
    )


    if matched:

        st.write(
            "✅ **Matched Skills:** "
            + ", ".join(
                skill.title()
                for skill in matched
            )
        )


    if missing:

        st.write(
            "📚 **Skills to Learn:** "
            + ", ".join(
                skill.title()
                for skill in missing[:6]
            )
        )


    st.divider()


# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🤖 AI Resume Analyzer | Resume Analysis • Skill Detection • "
    "Job Matching • Career Recommendations"
)