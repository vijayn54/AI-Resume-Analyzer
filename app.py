
import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from groq import Groq
import re


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Campus Companion AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GROQ CLIENT
# =========================================================
try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception:
    client = None


# =========================================================
# INITIAL SESSION STATE
# =========================================================
if "ats_score" not in st.session_state:
    st.session_state["ats_score"] = 0.0

if "match_score" not in st.session_state:
    st.session_state["match_score"] = 0.0

if "found_skills" not in st.session_state:
    st.session_state["found_skills"] = []

if "interview_score" not in st.session_state:
    st.session_state["interview_score"] = 0.0

if "placement_score" not in st.session_state:
    st.session_state["placement_score"] = 0.0

if "skill_gap_result" not in st.session_state:
    st.session_state["skill_gap_result"] = ""


# =========================================================
# PREMIUM UNIVERSITY UI
# =========================================================
st.markdown(
    """
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

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1e3a8a 0%,
            #2563eb 100%
        );
    }

    section[data-testid="stSidebar"] > div {
        background: transparent;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
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
        margin-bottom: 8px;
    }

    .hero h3 {
        color: #2563eb;
        margin-bottom: 10px;
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
        border: 1px solid #dbeafe;
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
        border: 1px solid #dbeafe;
    }

    textarea {
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 12px !important;
    }

    .section-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        border: 1px solid #e0f2fe;
    }

    .app-footer {
        text-align: center;
        padding: 25px;
        color: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px;">
        <div style="font-size:42px;">🎓</div>
        <h2 style="margin-bottom:5px;">Campus Companion</h2>
        <p style="font-size:14px;">
            AI Powered Career Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### ✨ Features

    ✅ ATS Score  
    ✅ Skill Detection  
    ✅ Job Match Analysis  
    ✅ AI Resume Feedback  
    ✅ Interview Preparation  
    ✅ Placement Readiness  
    ✅ Skill Gap Analysis
    """
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose Module",
    [
        "🏠 Home",
        "📄 Resume Analyzer",
        "🎤 Interview Preparation",
        "🎯 Placement Readiness"
    ]
)


# =========================================================
# MODULE 0 - STUDENT DASHBOARD
# =========================================================
if page == "🏠 Home":

    st.markdown(
        """
        <div class="hero">
            <h1>🎓 Campus Companion AI</h1>
<h3>Your Personal Placement & Career Assistant</h3>
<p>
    Analyze your resume, practice interviews, identify skill gaps,
    and track your placement readiness in one place.
</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # CONNECTED SCORES
    # -------------------------------------------------
    ats_score = st.session_state.get(
        "ats_score",
        0.0
    )

    match_score = st.session_state.get(
        "match_score",
        0.0
    )

    interview_score = st.session_state.get(
        "interview_score",
        0.0
    )

    placement_score = st.session_state.get(
        "placement_score",
        0.0
    )

    found_skills = st.session_state.get(
        "found_skills",
        []
    )

    skill_gap_result = st.session_state.get(
        "skill_gap_result",
        ""
    )

    # -------------------------------------------------
    # PERFORMANCE CARDS
    # -------------------------------------------------
    st.subheader("🎯 Current Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Resume ATS",
            f"{ats_score:.1f}%"
        )

    with col2:
        st.metric(
            "Job Match",
            f"{match_score:.1f}%"
        )

    with col3:
        st.metric(
            "Interview",
            f"{interview_score:.1f}%"
        )

    with col4:
        st.metric(
            "Placement",
            f"{placement_score:.1f}/100"
        )

    # -------------------------------------------------
    # NEXT BEST ACTION
    # -------------------------------------------------
    st.markdown("---")

    st.subheader("🚀 Your Next Best Action")

    if placement_score <= 0:
        st.info(
            "📄 Start by analyzing your resume and completing "
            "a mock interview."
        )
    elif placement_score < 60:
        st.warning(
            "🎯 Focus on improving your technical skills and "
            "interview performance."
        )
    elif placement_score < 80:
        st.info(
            "🧩 Work on your skill gaps and complete more "
            "mock interviews."
        )
    else:
        st.success(
            "🎉 You're showing strong placement readiness. "
            "Keep practicing and close your remaining skill gaps."
        )

    # -------------------------------------------------
    # PROGRESS
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("📈 Progress Overview")

    progress_items = {
        "Resume ATS": ats_score,
        "Job Match": match_score,
        "Interview": interview_score,
        "Placement Readiness": placement_score
    }

    for name, score in progress_items.items():
        st.write(
            f"**{name}: {score:.1f}%**"
        )
        st.progress(
            min(max(int(score), 0), 100)
        )

    # -------------------------------------------------
    # SKILL GAP SUMMARY
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("🧠 Skill Gap Status")

    if skill_gap_result:

        # Try to show the most relevant part of the report
        missing_match = re.search(
            r"3\.\s*MISSING SKILLS\s*(.*?)(?=4\.\s*TOP 5 PRIORITY SKILLS TO LEARN|$)",
            skill_gap_result,
            re.IGNORECASE | re.DOTALL
        )

        if missing_match:
            st.warning(
                missing_match.group(1).strip()
            )
        else:
            st.write(
                "A Skill Gap Report has been generated in "
                "Placement Readiness."
            )

    else:

        st.info(
            "Run Skill Gap Analysis from Placement Readiness "
            "to see your current skill-gap status."
        )

    # -------------------------------------------------
    # READINESS MESSAGE
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("🚀 Recommended Next Step")

    if placement_score <= 0:
        st.info(
            "Start by analyzing your resume, completing a mock interview, "
            "and calculating your placement readiness."
        )

    elif placement_score < 60:
        st.warning(
            "Focus on building your technical skills, improving your resume, "
            "and practicing interviews."
        )

    elif placement_score < 80:
        st.info(
            "You're progressing well. Work on your skill gaps and interview "
            "performance to become placement ready."
        )

    else:
        st.success(
            "🎉 Strong placement readiness. Keep improving your skill gaps "
            "and maintain regular interview practice."
        )


# =========================================================
# MODULE 1 - RESUME ANALYZER
# =========================================================
if page == "📄 Resume Analyzer":

    st.markdown(
        """
        <div class="hero">
            <h1>🎓 Campus Companion AI</h1>
            <h3>Smart Resume Analyzer & Placement Assistant</h3>
            <p>
                ATS Analysis • Resume Intelligence • Skill Detection
                • Career Guidance
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>📊 Student Placement Dashboard</h3>
            <p>
                Upload your resume and compare it with a job description
                to improve your placement chances.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
        # EXTRACTED RESUME
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

        resume_lower = text.lower()

        found_skills = []

        for skill in skills:

            if skill.lower() in resume_lower:
                found_skills.append(skill)

        # -------------------------------------------------
        # ATS SCORE
        # -------------------------------------------------
        ats_score = (
            len(found_skills) / len(skills)
        ) * 100

        st.session_state["ats_score"] = ats_score
        st.session_state["found_skills"] = found_skills

        # -------------------------------------------------
        # JOB MATCH SCORE
        # -------------------------------------------------
        match_score = 0.0

        if job_description.strip():

            resume_words = set(
                resume_lower.split()
            )

            jd_words = set(
                job_description.lower().split()
            )

            if jd_words:

                matched_words = (
                    resume_words.intersection(
                        jd_words
                    )
                )

                match_score = (
                    len(matched_words)
                    / len(jd_words)
                ) * 100

        st.session_state["match_score"] = match_score

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

            st.subheader(
                "🎯 Job Match Analysis"
            )

            st.progress(
                min(int(match_score), 100)
            )

            st.write(
                f"Match Score: {match_score:.2f}%"
            )

        # -------------------------------------------------
        # DOWNLOAD REPORT
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
        st.subheader(
            "🤖 AI Resume Feedback"
        )

        if st.button(
            "✨ Generate AI Feedback",
            key="resume_ai_feedback"
        ):

            if client is None:

                st.error(
                    "Groq API key is not configured. "
                    "Please check Streamlit Secrets."
                )

            else:

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

                        st.write(
                            feedback
                        )

                    except Exception as e:

                        st.error(
                            f"AI analysis failed: {e}"
                        )


# =========================================================
# MODULE 2 - AI INTERVIEW PREPARATION
# =========================================================
elif page == "🎤 Interview Preparation":

    st.markdown(
        """
        <div class="hero">
            <h1>🎤 AI Interview Preparation</h1>
            <h3>Practice. Improve. Get Placement Ready.</h3>
            <p>
                Generate personalized interview questions using AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>🚀 Personalized Interview Practice</h3>
            <p>
                Choose an interview type, enter your target role,
                and let AI generate realistic placement questions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

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

        elif client is None:

            st.error(
                "Groq API key is not configured. "
                "Please check Streamlit Secrets."
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

    # =================================================
    # MOCK INTERVIEW
    # =================================================

    st.markdown("---")

    st.subheader(
        "🎤 Mock Interview"
    )

    st.write(
        "Practice answering an interview question and "
        "get an AI evaluation."
    )

    mock_question = st.text_area(
        "💬 Enter an interview question",
        placeholder=(
            "Example: Explain your AI Resume Analyzer project."
        )
    )

    student_answer = st.text_area(
        "✍️ Your Answer",
        height=200,
        placeholder="Type your answer here..."
    )

    if st.button(
        "🧠 Evaluate My Answer",
        key="evaluate_mock_answer"
    ):

        if not mock_question.strip():

            st.warning(
                "Please enter an interview question."
            )

        elif not student_answer.strip():

            st.warning(
                "Please enter your answer."
            )

        elif client is None:

            st.error(
                "Groq API key is not configured."
            )

        else:

            with st.spinner(
                "AI is evaluating your answer..."
            ):

                evaluation_prompt = f"""
You are an expert interviewer evaluating a college student
preparing for internships and placements.

Interview Question:
{mock_question}

Student Answer:
{student_answer}

Evaluate the answer.

Your response MUST start with exactly one line in this format:

SCORE: X

where X is a number from 0 to 10.

Then provide:

1. What the student did well
2. What could be improved
3. Important points that were missed
4. A better sample answer
5. One practical tip for the next interview

Be encouraging, honest, and student-friendly.
"""

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": evaluation_prompt
                            }
                        ]
                    )

                    evaluation = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    # -------------------------------------------------
                    # EXTRACT INTERVIEW SCORE
                    # -------------------------------------------------
                    score_match = re.search(
                        r"SCORE\s*:\s*(10(?:\.0)?|[0-9](?:\.[0-9])?)",
                        evaluation,
                        re.IGNORECASE
                    )

                    if score_match:

                        score_value = float(
                            score_match.group(1)
                        )

                        score_value = max(
                            0.0,
                            min(
                                score_value,
                                10.0
                            )
                        )

                        interview_score = (
                            score_value * 10
                        )

                        st.session_state[
                            "interview_score"
                        ] = interview_score

                        st.metric(
                            "Interview Score",
                            f"{interview_score:.0f}/100"
                        )

                    else:

                        st.warning(
                            "The AI response did not return "
                            "a valid score."
                        )

                    st.subheader(
                        "📊 AI Interview Evaluation"
                    )

                    st.write(
                        evaluation
                    )

                except Exception as e:

                    st.error(
                        f"AI evaluation failed: {e}"
                    )


# =========================================================
# MODULE 3 - PLACEMENT READINESS
# =========================================================
elif page == "🎯 Placement Readiness":

    st.markdown(
        """
        <div class="hero">
            <h1>🎯 Placement Readiness Engine</h1>
            <h3>Know Where You Stand. Know What To Improve.</h3>
            <p>
                Analyze your preparation and get a personalized
                placement readiness score.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =================================================
    # CONNECTED DATA
    # =================================================
    ats_score = st.session_state.get(
        "ats_score",
        0.0
    )

    match_score = st.session_state.get(
        "match_score",
        0.0
    )

    interview_score = st.session_state.get(
        "interview_score",
        0.0
    )

    found_skills = st.session_state.get(
        "found_skills",
        []
    )

    # =================================================
    # CONNECTED MODULE SCORES
    # =================================================
    st.subheader(
        "🔗 Connected Module Scores"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Resume ATS",
            f"{ats_score:.1f}%"
        )

    with c2:

        st.metric(
            "Job Match",
            f"{match_score:.1f}%"
        )

    with c3:

        st.metric(
            "Interview",
            f"{interview_score:.1f}%"
        )

    if ats_score == 0:

        st.info(
            "📄 Analyze a resume first to load your ATS score."
        )

    if match_score == 0:

        st.info(
            "🎯 Add a job description in Resume Analyzer "
            "to load the Job Match score."
        )

    if interview_score == 0:

        st.info(
            "🎤 Complete a Mock Interview to load "
            "your Interview score."
        )

    if found_skills:

        st.write(
            "Detected Skills: "
            + ", ".join(found_skills)
        )

    # =================================================
    # ADDITIONAL ASSESSMENT
    # =================================================
    st.markdown("---")

    st.subheader(
        "📝 Additional Assessment"
    )

    col1, col2 = st.columns(2)

    with col1:

        cgpa = st.number_input(
            "🎓 CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.5,
            step=0.1
        )

        project_score = st.slider(
            "🚀 Project Strength",
            min_value=0,
            max_value=100,
            value=70
        )

    with col2:

        certification_score = st.slider(
            "📜 Certifications",
            min_value=0,
            max_value=100,
            value=60
        )

        communication_score = st.slider(
            "🗣️ Communication",
            min_value=0,
            max_value=100,
            value=65
        )

    target_role = st.text_input(
        "💼 Target Job Role",
        placeholder=(
            "Example: Software Developer, "
            "Data Analyst, AI Engineer"
        )
    )

    # =================================================
    # SKILL GAP ANALYZER
    # =================================================
    st.markdown("---")

    st.subheader(
        "🧩 AI Skill Gap Analyzer"
    )

    st.write(
        "Compare your resume skills with the skills required "
        "for your target role."
    )

    if st.button(
        "🔍 Analyze Skill Gap",
        key="analyze_skill_gap"
    ):

        if not target_role.strip():

            st.warning(
                "Please enter your target job role first."
            )

        elif client is None:

            st.error(
                "Groq API key is not configured."
            )

        elif not found_skills:

            st.warning(
                "Please analyze your resume first so the system "
                "can detect your current skills."
            )

        else:

            with st.spinner(
                "Analyzing required skills for your target role..."
            ):

                skill_gap_prompt = f"""
You are an expert career and placement advisor.

Target Job Role:
{target_role}

Student's Current Skills:
{", ".join(found_skills)}

Analyze the target role and identify the most important
technical and professional skills normally expected for that role.

Compare the target-role requirements with the student's skills.

Return exactly these sections:

1. REQUIRED SKILLS
2. SKILLS YOU ALREADY HAVE
3. MISSING SKILLS
4. TOP 5 PRIORITY SKILLS TO LEARN
5. PERSONALIZED LEARNING ROADMAP

Make the recommendations realistic for a college student.
"""

                try:

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": skill_gap_prompt
                            }
                        ]
                    )

                    skill_gap_result = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.session_state["skill_gap_result"] = skill_gap_result

                    st.subheader(
                        "📊 Skill Gap Report"
                    )

                    st.write(
                        skill_gap_result
                    )

                except Exception as e:

                    st.error(
                        f"Skill gap analysis failed: {e}"
                    )

    # =================================================
    # PLACEMENT READINESS SCORE
    # =================================================
    st.markdown("---")

    if st.button(
        "🚀 Calculate Placement Readiness",
        key="calculate_placement_readiness"
    ):

        if not target_role.strip():

            st.warning(
                "Please enter your target job role."
            )

        else:

            cgpa_score = (
                cgpa / 10
            ) * 100

            technical_skill_score = ats_score

            placement_score = (
                cgpa_score * 0.15
                + technical_skill_score * 0.25
                + interview_score * 0.20
                + match_score * 0.10
                + project_score * 0.10
                + certification_score * 0.05
                + communication_score * 0.15
            )

            st.session_state[
                "placement_score"
            ] = placement_score

            st.markdown("---")

            st.subheader(
                "🏆 Placement Readiness Score"
            )

            score_col1, score_col2, score_col3 = (
                st.columns(3)
            )

            with score_col1:

                st.metric(
                    "Overall Score",
                    f"{placement_score:.1f}/100"
                )

            with score_col2:

                if placement_score >= 80:

                    status = (
                        "Placement Ready 🟢"
                    )

                elif placement_score >= 60:

                    status = (
                        "Almost Ready 🟡"
                    )

                else:

                    status = (
                        "Needs Improvement 🔴"
                    )

                st.metric(
                    "Status",
                    status
                )

            with score_col3:

                st.metric(
                    "Target Role",
                    target_role
                )

            st.progress(
                min(
                    int(placement_score),
                    100
                )
            )

            # =================================================
            # READINESS BREAKDOWN
            # =================================================
            st.subheader(
                "📈 Readiness Breakdown"
            )

            categories = {
                "Academic": cgpa_score,
                "Resume / Technical": technical_skill_score,
                "Interview": interview_score,
                "Job Match": match_score,
                "Projects": project_score,
                "Certifications": certification_score,
                "Communication": communication_score
            }

            for category, score in categories.items():

                st.write(
                    f"**{category}: {score:.1f}%**"
                )

                st.progress(
                    min(
                        int(score),
                        100
                    )
                )

            # =================================================
            # WEAK AREAS
            # =================================================
            weak_areas = sorted(
                categories.items(),
                key=lambda item: item[1]
            )

            st.subheader(
                "⚠️ Areas To Improve"
            )

            improvements_found = False

            for category, score in weak_areas[:3]:

                if score < 70:

                    improvements_found = True

                    st.warning(
                        f"{category}: {score:.1f}% — "
                        "Focus on improving this area."
                    )

            if not improvements_found:

                st.success(
                    "🎉 No major weak areas were detected."
                )

            # =================================================
            # AI IMPROVEMENT PLAN
            # =================================================
            st.subheader(
                "🤖 AI Improvement Plan"
            )

            if client is None:

                st.error(
                    "Groq API key is not configured. "
                    "Please check Streamlit Secrets."
                )

            else:

                improvement_prompt = f"""
You are a college placement mentor.

A student's placement readiness information is:

Target Role:
{target_role}

CGPA:
{cgpa}

Resume / Technical Score:
{technical_skill_score:.1f}/100

Interview Performance:
{interview_score:.1f}/100

Job Match Score:
{match_score:.1f}/100

Project Strength:
{project_score}/100

Certifications:
{certification_score}/100

Communication:
{communication_score}/100

Overall Placement Score:
{placement_score:.1f}/100

Detected Skills:
{", ".join(found_skills) if found_skills else "No skills detected yet"}

Create a personalized improvement plan.

Provide:

1. Current readiness assessment
2. Top 3 weaknesses
3. What to improve first
4. A 30-day improvement roadmap
5. Recommended practice activities
6. Final placement advice

Keep it practical, honest, and suitable for a college student.
"""

                try:

                    with st.spinner(
                        "Creating your personalized placement plan..."
                    ):

                        response = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {
                                    "role": "user",
                                    "content": improvement_prompt
                                }
                            ]
                        )

                        improvement_plan = (
                            response
                            .choices[0]
                            .message
                            .content
                        )

                    st.write(
                        improvement_plan
                    )

                except Exception as e:

                    st.error(
                        f"AI placement analysis failed: {e}"
                    )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="app-footer">
        <hr>
        <h3>🎓 Campus Companion AI</h3>
        <p>
            Built using Streamlit + Groq AI + Python
        </p>
        <p>
            Helping Students Become Placement Ready 🚀
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


