# Resume Ranking System  

## 📌 Overview  
The **Resume Ranking System** is a web-based application built using **Python, Streamlit, and Jupyter Notebook**. It helps automate the process of evaluating and ranking resumes based on predefined criteria such as skills, experience, education, and other relevant factors.  

## 🚀 Features  
- Upload and parse resumes in **PDF/DOCX** format  
- Extract key information using **Natural Language Processing (NLP)**  
- Compare resumes against a **job description**  
- Rank resumes based on predefined **scoring criteria**  
- Display results in an interactive **Streamlit dashboard**  

## 🛠️ Technologies Used  
- **Python** – Core programming language  
- **Streamlit** – For building the interactive web UI  
- **Jupyter Notebook** – For development and testing  
- **NLTK / spaCy** – For Natural Language Processing  
- **Pandas** – For data manipulation  
- **PyPDF2 / pdfminer.six** – For extracting text from PDFs  

## 📂 Project Structure  
![image](https://github.com/user-attachments/assets/abd2f84d-7cd3-4cf8-9749-34cc64af402e)

## 🎯 How It Works  
1. **Upload Resumes** – Users upload multiple resumes in PDF or DOCX format.  
2. **Extract Information** – The system extracts text and key details like skills, experience, and education.  
3. **Job Description Matching** – Compares resumes against the job description.  
4. **Scoring & Ranking** – Assigns scores based on keyword matching, experience, and relevancy.  
5. **Display Results** – Shows ranked resumes with detailed analysis in Streamlit UI.  

## 🔧 Installation & Usage  
### 1️⃣ Install Dependencies  
Make sure you have Python installed, then install the required packages:  
```bash
pip install -r requirements.txt

streamlit run app.py
---
