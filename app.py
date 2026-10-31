
import re
from io import BytesIO

import streamlit as st
from docx import Document
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# 1. Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume-to-Job Description Matcher")
st.write(
    "Upload a resume and paste a job description to identify "
    "text similarity, matching skills, and potential skill gaps."
)


# -----------------------------
# 2. Skill dictionary
# -----------------------------
SKILLS = [
    "python", "sql", "excel", "power bi", "tableau",
    "pandas", "numpy", "machine learning", "deep learning",
    "data analysis", "data visualization", "statistics",
    "natural language processing", "nlp", "tensorflow",
    "pytorch", "scikit-learn", "aws", "azure", "gcp",
    "git", "docker", "java", "c++", "communication",
    "problem solving", "data engineering", "generative ai",
    "large language models", "llm", "streamlit"
]


# -----------------------------
# 3. Extract text from files
# -----------------------------
def extract_resume_text(uploaded_file):
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if file_name.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]
        text = "\n".join(pages)

    elif file_name.endswith(".docx"):
        document = Document(BytesIO(file_bytes))
        text = "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

        # Also extract text from tables, which are common in resumes.
        for table in document.tables:
            for row in table.rows:
                text += "\n" + " ".join(
                    cell.text for cell in row.cells
                )

    elif file_name.endswith(".txt"):
        text = file_bytes.decode("utf-8", errors="ignore")

    else:
        raise ValueError("Please upload a PDF, DOCX, or TXT file.")

    if not text.strip():
        raise ValueError(
            "No text could be extracted. If this is a scanned PDF, "
            "OCR may be required."
        )

    return text


# -----------------------------
# 4. Clean text
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# 5. Identify skills
# -----------------------------
def find_skills(text):
    cleaned = clean_text(text)
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, cleaned):
            found.append(skill)

    return sorted(set(found))


# -----------------------------
# 6. Calculate similarity
# -----------------------------
def calculate_similarity(resume_text, job_text):
    documents = [
        clean_text(resume_text),
        clean_text(job_text)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(documents)
    except ValueError:
        return 0.0

    score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(score) * 100, 2)


# -----------------------------
# 7. Upload resume and enter job
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx", "txt"]
)

job_description = st.text_area(
    "Paste the job description",
    height=250,
    placeholder=(
        "Example: We are looking for a Data Analyst "
        "with Python, SQL, Excel, Power BI, and statistics skills..."
    )
)


# -----------------------------
# 8. Run matching
# -----------------------------
if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.error("Please upload your resume.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            resume_text = extract_resume_text(uploaded_file)

            resume_skills = set(find_skills(resume_text))
            job_skills = set(find_skills(job_description))

            matched_skills = sorted(resume_skills & job_skills)
            missing_skills = sorted(job_skills - resume_skills)

            score = calculate_similarity(
                resume_text,
                job_description
            )

            # -----------------------------
            # 9. Display results
            # -----------------------------
            st.divider()
            st.header("Analysis Results")

            col1, col2, col3 = st.columns(3)

            col1.metric("Text Similarity", f"{score}%")
            col2.metric("Matching Skills", len(matched_skills))
            col3.metric("Potential Skill Gaps", len(missing_skills))

            st.caption(
                "Similarity is a text-based comparison, not a hiring "
                "probability or a guarantee of job suitability."
            )

            st.subheader("✅ Matching Skills")

            if matched_skills:
                st.write(", ".join(matched_skills))
            else:
                st.info("No matching skills were found in the current dictionary.")

            st.subheader("📚 Skills Mentioned in the Job but Not Found in Resume")

            if missing_skills:
                st.write(", ".join(missing_skills))
                st.caption(
                    "Check these manually. Add a skill to your resume "
                    "only if you genuinely have that skill."
                )
            else:
                st.success(
                    "All skills in the current skill dictionary were found "
                    "in both texts."
                )

            st.subheader("📋 Resume Text Preview")
            st.text_area(
                "Extracted text",
                resume_text[:5000],
                height=180
            )

        except Exception as error:
            st.error(f"Could not analyze the resume: {error}")


st.divider()
st.caption(
    "Prototype for educational use. Review results manually before "
    "making recruitment or career decisions."
)
