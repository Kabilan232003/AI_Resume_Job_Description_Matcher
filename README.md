
# AI Resume-to-Job Description Matcher

## 1. Project Overview

This project compares a candidate's resume with a job description
using Natural Language Processing (NLP).

It calculates a text similarity score and identifies matching
skills and potential skill gaps.

## 2. Problem Statement

Candidates often find it difficult to determine whether their
resume reflects the skills and requirements in a job description.

This application helps candidates review the alignment between
their resume and a target role.

## 3. Project Objectives

- Extract text from PDF, DOCX, and TXT resumes.
- Clean and preprocess text.
- Convert text into numerical features using TF-IDF.
- Calculate similarity using cosine similarity.
- Identify matching and potentially missing skills.
- Display results in a web application.

## 4. Technologies Used

- Python
- Natural Language Processing (NLP)
- TF-IDF
- Cosine Similarity
- Scikit-learn
- Streamlit
- PyPDF
- Python-docx

## 5. Project Structure

    AI_Resume_Job_Matcher/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    └── .venv/

## 6. Installation

Create a virtual environment:

    python -m venv .venv

Activate it in Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

Install the required libraries:

    python -m pip install -r requirements.txt

## 7. Run the Application

Run this command in the project folder:

    python -m streamlit run app.py

Open the local address displayed in the terminal.

## 8. How to Use

1. Upload a PDF, DOCX, or TXT resume.
2. Paste a job description.
3. Click Analyze Resume.
4. Review the text similarity score.
5. Review matching skills and potential skill gaps.

## 9. Machine Learning Workflow

Resume and job description
→ Text extraction
→ Text cleaning
→ TF-IDF vectorization
→ Cosine similarity
→ Skill comparison
→ Results dashboard

## 10. Limitations

- The skill dictionary contains a limited selection of skills.
- TF-IDF does not fully understand context or meaning.
- The similarity score is not a hiring probability.
- Scanned PDFs may require Optical Character Recognition (OCR).
- Results should be reviewed manually.

## 11. Future Improvements

- Semantic matching with Sentence Transformers
- Skill synonym detection
- Model evaluation with labeled resume-job pairs
- Downloadable reports
- Multilingual resume support
- Deployment to a cloud platform

## 12. Disclaimer

This application is an educational prototype. It should support,
not replace, human review in recruitment decisions.
