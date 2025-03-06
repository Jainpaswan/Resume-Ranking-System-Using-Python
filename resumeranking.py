import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import numpy as np
import time
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to clean and normalize text
def clean_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

# Function to extract text from PDF
def extract_text_from_pdf(file):
    try:
        pdf = PdfReader(file)
        text = " ".join([page.extract_text() if page.extract_text() else "" for page in pdf.pages])
        text = clean_text(text)
        return text if text.strip() else None  # Return None if the text is empty
    except Exception as e:
        st.error(f"Error reading {file.name}: {e}")
        return None

# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    #st.write("🔍 Debug: Job Description Length:", len(job_description))
    #st.write("🔍 Debug: Number of Valid Resumes:", len(resumes))

    if not resumes or all(resume is None for resume in resumes):
        st.error("❌ No valid resumes to rank.")
        return None  # No valid resumes

    # Remove None values
    resumes = [resume for resume in resumes if resume]

    documents = [job_description] + resumes
    #st.write("🔍 Debug: Number of Documents for TF-IDF:", len(documents))

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))

    try:
        vectors = vectorizer.fit_transform(documents).toarray()
        #st.write("✅ Debug: TF-IDF Vectorization Success!")

        job_desc_vector = vectors[0]
        resume_vectors = vectors[1:]

        if len(resume_vectors) == 0:
            st.error("❌ No valid resume vectors for similarity calculation.")
            return None  # No valid resume vectors

        cosine_similarities = cosine_similarity([job_desc_vector], resume_vectors).flatten()
        #st.write("✅ Debug: Cosine Similarities Computed:", cosine_similarities)

        if cosine_similarities.size == 0:
            st.error("❌ Cosine similarity calculation failed.")
            return None

        # Normalize scores between 0 and 100, handling the case where all similarities are the same
        if cosine_similarities.max() == cosine_similarities.min():
            normalized_scores = np.full_like(cosine_similarities, 50)  # Set all scores to 50 if only one resume
        else:
            normalized_scores = (cosine_similarities - cosine_similarities.min()) / (cosine_similarities.max() - cosine_similarities.min()) * 100
        
        st.write("✅ Debug: Normalized Scores Computed:", normalized_scores)

        return normalized_scores
    except Exception as e:
        st.error(f"❌ Error in ranking: {e}")
        return None

# Streamlit UI
st.title("📄 AI Resume Screening & Candidate Ranking System")
st.header("📝 Job Description")
job_description = st.text_area("Enter the job description here", height=150)

st.header("📂 Upload Resumes")
uploaded_files = st.file_uploader("Upload multiple PDF resumes", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description:
    st.header("📊 Ranking Resumes")

    resumes = []
    error_files = []
    progress_bar = st.progress(0)

    for idx, file in enumerate(uploaded_files):
        text = extract_text_from_pdf(file)
        if text is None:
            error_files.append(file.name)
        else:
            resumes.append(text)
        progress_bar.progress((idx + 1) / len(uploaded_files))
        time.sleep(0.2)

    progress_bar.empty()

    if error_files:
        st.error(f"⚠️ Unable to process: {', '.join(error_files)}")

    if resumes:
        scores = rank_resumes(job_description, resumes)

        if scores is not None:
            results = pd.DataFrame({
                "Resume": [file.name for file in uploaded_files if file.name not in error_files],
                "Score": scores
            })

            results = results.sort_values(by="Score", ascending=False)
            st.success("✅ Ranking complete!")
            st.dataframe(results)

            csv = results.to_csv(index=False)
            st.download_button(label="📥 Download Results as CSV", data=csv, file_name="resume_ranking_results.csv", mime="text/csv")
        else:
            st.error("❌ No valid resume scores generated.")
    else:
        st.error("❌ No valid resumes processed.")
