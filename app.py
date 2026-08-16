import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from groq import Groq

# ----------------------------
# GROQ CLIENT
# ----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------
# CUSTOM CSS
# ----------------------------
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

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

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
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    margin-bottom: 25px;
}

.hero h1 {
    color: #1e3a8a;
}

.hero h3 {
    color: #2563eb;
}

.hero p {
    color: #475569;
}

[data-testid="stMetric"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    width: 100%;
    height: 50px;
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



# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
<div class="hero">
    <h1>🎓 Campus Companion AI</h1>
    <h3>Smart Resume Analyzer & Placement Assistant</h3>
    <p>
        ATS Analysis • Resume Intelligence • Skill Detection • Career Guidance
    </p>
</div>
""", unsafe_allow_html=True)


# ----------------------------
# SIDEBAR
# ----------------------------
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

✅ Placement Preparation

✅ Resume Suggestions
""")

# ----------------------------
# DASHBOARD
# ----------------------------
st.markdown("""
### 📊 Student Placement Dashboard

Upload your resume and compare it with job descriptions to improve your placement chances.
""")

# ----------------------------
# JOB DESCRIPTION
# ----------------------------
job_description = st.text_area(
    "Paste the Job Description Here",
    height=200
)

# ----------------------------
# FILE UPLOAD
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# ----------------------------
# MAIN LOGIC
# ----------------------------
if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Resume Text
    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        value=text,
        height=300,
        key="resume_content"
    )

    # Skills List
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

    # Skill Detection
    found_skills = []

    for skill in skills:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Detected Skills
    st.subheader("🚀 Detected Skills")

    if found_skills:

        for skill in found_skills:
            st.write(f"✅ {skill}")

    else:

        st.warning("No skills detected.")

    # ATS Score
    ats_score = (
        len(found_skills) / len(skills)
    ) * 100

    # Job Match Score
    match_score = 0

    if job_description.strip():

        resume_words = set(
            text.lower().split()
        )

        jd_words = set(
            job_description.lower().split()
        )

        if len(jd_words) > 0:

            matched_words = resume_words.intersection(
                jd_words
            )

            match_score = (
                len(matched_words)
                / len(jd_words)
            ) * 100

    # Metrics
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

    # Skills Chart
    st.subheader("📊 Skills Chart")

    fig, ax = plt.subplots()

    ax.pie(
        [
            len(found_skills),
            len(skills) - len(found_skills)
        ],
        labels=[
            "Found Skills",
            "Missing Skills"
        ],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # Missing Skills
    st.subheader("📌 Resume Suggestions")

    missing_skills = []

    for skill in skills:

        if skill not in found_skills:
            missing_skills.append(skill)

    if missing_skills:

        st.write(
            "Consider learning or adding these skills:"
        )

        for skill in missing_skills:
            st.write(f"❌ {skill}")

    else:

        st.success(
            "🎉 Great! Your resume contains all tracked skills."
        )

    # Report
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

    # Job Match Display
    if job_description.strip():

        st.subheader("📈 Job Match Score")

        st.progress(
            min(int(match_score), 100)
        )

        st.write(
            f"Match Score: {match_score:.2f}%"
        )

    # AI Feedback
    st.subheader("🤖 AI Resume Feedback")

    if st.button("Generate AI Feedback"):

        with st.spinner(
            "Analyzing Resume..."
        ):

            prompt = f"""
Analyze this resume and provide:

1. Strengths
2. Weaknesses
3. Missing Skills
4. Suggestions for Improvement
5. ATS Optimization Tips
6. Job Role Recommendations

Resume:

{text}
"""

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
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

                st.write(feedback)

            except Exception as e:

                st.error(
                    f"AI analysis failed: {e}"
                )

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
---
### 🎓 Campus Companion AI

Built using Streamlit + Groq AI + Python

Helping Students Become Placement Ready 🚀
""")

