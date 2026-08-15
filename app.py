import streamlit as st
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")

# Sidebar
st.sidebar.title("Resume Analyzer")

st.sidebar.info(
    """
    Features:
    ✅ ATS Score
    ✅ Skill Detection
    ✅ Job Match Score
    ✅ AI Feedback
    """
)


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

    # Read PDF
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


    # Detect Skills
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

            matched_words = (
                resume_words.intersection(jd_words)
            )

            match_score = (
                len(matched_words) / len(jd_words)
            ) * 100


    # Metrics
    col1, col2 = st.columns(2)


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


    # Skills Chart
    st.subheader("Skills Chart")

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
    st.subheader("Resume Suggestions")

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
            "Great! Your resume contains all tracked skills."
        )


    # Download Report
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
        label="Download Resume Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )


    # Job Match Display
    if job_description.strip():

        st.subheader("Job Match Score")

        st.progress(
            min(int(match_score), 100)
        )

        st.write(
            f"Match Score: {match_score:.2f}%"
        )


    # AI Resume Feedback
    st.subheader("AI Resume Feedback")


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