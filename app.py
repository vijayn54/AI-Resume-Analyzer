import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from groq import Groq


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Campus Companion AI",
    page_icon="🎓",
    layout="wide"
)


# -------------------------------------------------
# GROQ CLIENT
# -------------------------------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -------------------------------------------------
# PREMIUM UNIVERSITY THEME
# -------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f8fafc,
        #e0f2fe,
        #dbeafe
    );
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #1e3a8a,
        #2563eb
    );
}

section[data-testid="stSidebar"] * {
    color: white;
}

.hero {
    text-align: center;
    padding: 35px;
    border-radius: 25px;
    background: white;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    margin-bottom: 25px;
}

.hero h1 {
    color: #1e3a8a;
    font-size: 42px;
}

.hero h3 {
    color: #2563eb;
}

.hero p {
    color: #475569;
    font-size: 18px;
}

[data-testid="stMetric"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.10);
}

.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    width: 100%;
    min-height: 48px;
}

.stButton > button:hover {
    background: #1d4ed8;
}

div[data-testid="stFileUploader"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
}

textarea {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("🎓 Campus Companion")

st.sidebar.success(
    "AI Powered Career Assistant"
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Features

✅ ATS Score

✅ Skill Detection

✅ Job Match Analysis

✅ AI Resume Feedback

✅ Interview Preparation

✅ Placement Preparation
""")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose Module",
    [
        "📄 Resume Analyzer",
        "🎤 Interview Preparation"
    ]
)


# =================================================
# MODULE 1 - RESUME ANALYZER
# =================================================
if page == "📄 Resume Analyzer":

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.markdown("""
    <div class="hero">
        <h1>🎓 Campus Companion AI</h1>
        <h3>Smart Resume Analyzer & Placement Assistant</h3>
        <p>
            ATS Analysis • Resume Intelligence • Skill Detection • Career Guidance
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------
    st.markdown("""
    ### 📊 Student Placement Dashboard

    Upload your resume and compare it with a job description
    to improve your placement chances.
    """)

    # -------------------------------------------------
    # JOB DESCRIPTION
    # -------------------------------------------------
    job_description = st.text_area(
        "📋 Paste the Job Description Here",
        height=200,
        placeholder="Paste the target job description here..."
    )

    # -------------------------------------------------
    # RESUME UPLOAD
    # -------------------------------------------------
    uploaded_file = st.file_uploader(
        "📄 Upload your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("✅ Resume uploaded successfully!")

        # -------------------------------------------------
        # PDF READING
        # -------------------------------------------------
        try:

            pdf_reader = PdfReader(uploaded_file)

            text = ""

            for page_content in pdf_reader.pages:

                page_text = page_content.extract_text()

                if page_text:
                    text += page_text + "\n"

        except Exception as e:

            st.error(
                f"Could not read the PDF: {e}"
            )
            st.stop()

        if not text.strip():

            st.warning(
                "No readable text was found in this PDF."
            )
            st.stop()

        # -------------------------------------------------
        # EXTRACTED TEXT
        # -------------------------------------------------
        st.subheader("📄 Extracted Resume Text")

        st.text_area(
            "Resume Content",
            value=text,
            height=300,
            key="resume_content"
        )

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------
        skills = [
            "Python",
            "Java",
            "SQL",
            "Machine Learning",
            "Data Science",
            "C++",
            "HTML",
            "CSS",
            "JavaScript"
        ]

        # -------------------------------------------------
        # SKILL DETECTION
        # -------------------------------------------------
        found_skills = []

        resume_lower = text.lower()

        for skill in skills:

            if skill.lower() in resume_lower:
                found_skills.append(skill)

        # -------------------------------------------------
        # ATS SCORE
        # -------------------------------------------------
        ats_score = (
            len(found_skills) / len(skills)
        ) * 100

        # -------------------------------------------------
        # JOB MATCH SCORE
        # -------------------------------------------------
        match_score = 0

        if job_description.strip():

            resume_words = set(
                resume_lower.split()
            )

            jd_words = set(
                job_description.lower().split()
            )

            if jd_words:

                matched_words = (
                    resume_words.intersection(jd_words)
                )

                match_score = (
                    len(matched_words)
                    / len(jd_words)
                ) * 100

        # -------------------------------------------------
        # MISSING SKILLS
        # -------------------------------------------------
        missing_skills = [
            skill
            for skill in skills
            if skill not in found_skills
        ]

        # -------------------------------------------------
        # METRICS
        # -------------------------------------------------
        st.subheader("📊 Resume Overview")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "ATS Score",
                f"{ats_score:.1f}%"
            )

        with col2:

            st.metric(
                "Job Match",
                f"{match_score:.1f}%"
            )

        with col3:

            st.metric(
                "Skills Found",
                len(found_skills)
            )

        # -------------------------------------------------
        # DETECTED SKILLS
        # -------------------------------------------------
        st.subheader("🚀 Detected Skills")

        if found_skills:

            skill_columns = st.columns(3)

            for index, skill in enumerate(found_skills):

                with skill_columns[index % 3]:

                    st.success(
                        f"✅ {skill}"
                    )

        else:

            st.warning(
                "No tracked skills were detected."
            )

        # -------------------------------------------------
        # SKILLS CHART
        # -------------------------------------------------
        st.subheader("📈 Skills Analysis")

        found_count = len(found_skills)
        missing_count = len(skills) - found_count

        fig, ax = plt.subplots()

        ax.pie(
            [found_count, missing_count],
            labels=[
                "Found Skills",
                "Missing Skills"
            ],
            autopct="%1.1f%%"
        )

        st.pyplot(
            fig,
            use_container_width=False
        )

        # -------------------------------------------------
        # SUGGESTIONS
        # -------------------------------------------------
        st.subheader("📌 Resume Suggestions")

        if missing_skills:

            st.write(
                "Consider learning or adding these skills:"
            )

            for skill in missing_skills:

                st.write(
                    f"❌ {skill}"
                )

        else:

            st.success(
                "🎉 Great! Your resume contains all tracked skills."
            )

        # -------------------------------------------------
        # JOB MATCH
        # -------------------------------------------------
        if job_description.strip():

            st.subheader("🎯 Job Match Analysis")

            st.progress(
                min(int(match_score), 100)
            )

            st.write(
                f"Match Score: {match_score:.2f}%"
            )

        # -------------------------------------------------
        # REPORT
        # -------------------------------------------------
        report = f"""
AI Resume Analyzer Report

ATS Score:
{ats_score:.2f}%

Job Match Score:
{match_score:.2f}%

Detected Skills:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}
"""

        st.download_button(
            label="📥 Download Resume Report",
            data=report,
            file_name="resume_report.txt",
            mime="text/plain"
        )

        # -------------------------------------------------
        # AI FEEDBACK
        # -------------------------------------------------
        st.subheader("🤖 AI Resume Feedback")

        if st.button(
            "✨ Generate AI Feedback",
            key="resume_ai_feedback"
        ):

            with st.spinner(
                "Analyzing your resume..."
            ):

                prompt = f"""
You are an expert resume reviewer helping a college student
prepare for internships and placements.

Analyze this resume and provide:

1. Strengths
2. Weaknesses
3. Missing Skills
4. Suggestions for Improvement
5. ATS Optimization Tips
6. Recommended Job Roles

Be practical, clear, and student-friendly.

Resume:

{text}
"""

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    feedback = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.markdown(
                        "### 🧠 AI Analysis"
                    )

                    st.write(feedback)

                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )


# =================================================
# MODULE 2 - INTERVIEW PREPARATION
# =================================================
elif page == "🎤 Interview Preparation":

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------
    st.markdown("""
    <div class="hero">
        <h1>🎤 AI Interview Preparation</h1>
        <h3>Practice. Improve. Get Placement Ready.</h3>
        <p>
            Generate personalized interview questions using AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # INTERVIEW TYPE
    # -------------------------------------------------
    st.subheader(
        "🎯 Choose Interview Type"
    )

    interview_type = st.selectbox(
        "Select Interview Mode",
        [
            "Technical Interview",
            "HR Interview",
            "Project-Based Interview",
            "Mixed Interview"
        ]
    )

    # -------------------------------------------------
    # TARGET ROLE
    # -------------------------------------------------
    target_role = st.text_input(
        "💼 Target Job Role",
        placeholder=(
            "Example: Python Developer, "
            "Data Scientist, AI Engineer"
        )
    )

    # -------------------------------------------------
    # NUMBER OF QUESTIONS
    # -------------------------------------------------
    number_of_questions = st.slider(
        "📝 Number of Questions",
        min_value=3,
        max_value=10,
        value=5
    )

    # -------------------------------------------------
    # GENERATE QUESTIONS
    # -------------------------------------------------
    if st.button(
        "🚀 Generate Interview Questions",
        key="generate_interview_questions"
    ):

        if not target_role.strip():

            st.warning(
                "Please enter your target job role first."
            )

        else:

            with st.spinner(
                "Generating personalized interview questions..."
            ):

                prompt = f"""
You are an expert interviewer helping a college student
prepare for internships and placements.

Create {number_of_questions} interview questions
for a student applying for:

Target Role:
{target_role}

Interview Type:
{interview_type}

Make the questions realistic and practical.

For every question, provide:

1. Interview Question
2. What the interviewer is looking for
3. Short answering tip

Keep the language clear and student-friendly.
"""

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    questions = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.subheader(
                        "📚 Your Interview Questions"
                    )

                    st.write(
                        questions
                    )

                except Exception as e:

                    st.error(
                        f"AI interview generation failed: {e}"
                    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
---
<center>

### 🎓 Campus Companion AI

Built using Streamlit + Groq AI + Python

Helping Students Become Placement Ready 🚀

</center>
""", unsafe_allow_html=True)