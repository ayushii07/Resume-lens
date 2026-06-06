import streamlit as st
import google.generativeai as genai
from pdf2image import convert_from_bytes
from dotenv import load_dotenv
import os



st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide"
)



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background-color:#F8F4F1;
}

.main .block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* HERO */

.hero{
    background: linear-gradient(135deg,#0A4D57,#0F6A78);
    border-radius:30px;
    padding:50px;
    color:white;
    margin-bottom:30px;
}

.hero h1{
    font-size:55px;
    font-weight:700;
    margin-bottom:10px;
}

.hero p{
    font-size:18px;
    color:#f1f1f1;
}

/* CARDS */

.card{
    background:white;
    padding:25px;
    border-radius:25px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

.feature-card{
    background:#F6E4DE;
    padding:20px;
    border-radius:20px;
    text-align:center;
    min-height:140px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.05);
}

.feature-card h3{
    color:#0A4D57;
}

/* BUTTON */

.stButton > button{
    background:#0A4D57;
    color:white;
    border:none;
    border-radius:50px;
    padding:14px 35px;
    font-weight:600;
    width:100%;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"]{
    background:white;
    padding:20px;
    border-radius:20px;
    border:2px dashed #E8CFC5;
}

/* RESULT BOX */

.result-box{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
    margin-top:10px;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0px 8px 20px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)



load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")



st.markdown("""
<div class="hero">
<h1>RESUME LENS </h1>
<p>
AI-powered ATS resume analyzer , Get instant ATS insights with Resume Lens. Upload your resume and compare it against any job description to receive an ATS compatibility score, keyword analysis, skill gap detection, interview preparation tips, and actionable improvement suggestions.
</p>
</div>
""", unsafe_allow_html=True)



c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown("""
    <div class="feature-card">
    <h3>ATS Score</h3>
    <p>Resume Match Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
    <h3>Keywords</h3>
    <p>Missing Skills Detection</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
    <h3>Resume Fixes</h3>
    <p>Improve Resume Quality</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="feature-card">
    <h3>Interview Prep</h3>
    <p>Question Generator</p>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="feature-card">
    <h3>Skill Gap</h3>
    <p>Learning Roadmap</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



left,right = st.columns(2)

with left:

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with right:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=250
    )



def input_pdf_setup(uploaded_file):

    if uploaded_file is None:
        return None

    poppler_path = r"C:\Users\AYUSHI\OneDrive\Documents\SITES LOG\Release-26.02.0-0\poppler-26.02.0\Library\bin"

    images = convert_from_bytes(
        uploaded_file.read(),
        poppler_path=poppler_path
    )

    return images[0]


def get_gemini_response(prompt, pdf_content, job_description):

    response = model.generate_content(
        [
            prompt,
            pdf_content,
            job_description
        ]
    )

    return response.text



master_prompt = """
You are an expert ATS system, HR recruiter,
career coach and interview mentor.

Analyze the resume against the job description.

Return the response using the following sections:

# ATS SCORE
Provide:
- ATS Match Score (%)
- Candidate Summary
- Strengths
- Weaknesses

# MISSING KEYWORDS
Provide:
- Missing Keywords
- Missing Technical Skills
- Missing Tools
- Missing Certifications

# RESUME IMPROVEMENTS
Provide:
- Resume Improvement Suggestions
- Better Project Descriptions
- Better Achievement Statements

# INTERVIEW PREPARATION
Provide:
- Top Technical Questions
- Top HR Questions
- Top Project Questions

# SKILL GAP ANALYSIS
Provide:
- Missing Skills
- Learning Roadmap
- Recommended Certifications
- Readiness Percentage

Format professionally.
"""


st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button("🚀 Analyze Resume")



if analyze:

    if uploaded_file is None:
        st.warning("Please upload a resume.")
        st.stop()

    if not job_description:
        st.warning("Please enter a job description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        pdf_content = input_pdf_setup(uploaded_file)

        result = get_gemini_response(
            master_prompt,
            pdf_content,
            job_description
        )

    st.markdown("---")

    st.subheader("📊 Analysis Dashboard")

    st.markdown(
        f"""
        <div class="result-box">
        {result}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("Analysis Completed Successfully ✅")


st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <center>
    <p style='color:gray'>
    Powered by Google Gemini • AI Resume Intelligence Platform
    </p>
    </center>
    """,
    unsafe_allow_html=True
)