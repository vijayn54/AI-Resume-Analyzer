import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")

# Job Description Input
job_description = st.text_area(
    "Paste the Job Description Here",
    height=200
)

# Resume Upload
uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Show Resume Text
    st.subheader("Extracted Resume Text")

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

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Detected Skills
    st.subheader("Detected Skills")

    if found_skills:
        for skill in found_skills:
            st.write(f"✅ {skill}")
    else:
        st.warning("No skills detected.")

    # ATS Score
    st.subheader("ATS Score")

    ats_score = (len(found_skills) / len(skills)) * 100

    st.progress(int(ats_score))
    st.write(f"ATS Score: {ats_score:.2f}/100")

    # Skills Chart
    st.subheader("Skills Chart")

    fig, ax = plt.subplots()

    ax.pie(
        [len(found_skills), len(skills) - len(found_skills)],
        labels=["Found Skills", "Missing Skills"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # Resume Suggestions
    st.subheader("Resume Suggestions")

    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    if missing_skills:
        st.write("Consider learning or adding these skills:")

        for skill in missing_skills:
            st.write(f"❌ {skill}")
    else:
        st.success("Great! Your resume contains all tracked skills.")

    # Download Report
    report = f"""
ATS Score: {ats_score:.2f}/100

Detected Skills:
{', '.join(found_skills)}

Missing Skills:
{', '.join(missing_skills)}
"""

    st.download_button(
        label="Download Resume Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )

    # Job Match Score
    if job_description.strip():

        resume_words = set(text.lower().split())
        jd_words = set(job_description.lower().split())

        matched_words = resume_words.intersection(jd_words)

        match_score = (
            len(matched_words) / len(jd_words)
        ) * 100

        st.subheader("Job Match Score")

        st.progress(int(match_score))
        st.write(f"Match Score: {match_score:.2f}%")