# PDFgpt – Local PDF Question Answering System

## 🚀 Run Project

1. Create & activate virtual environment:
python -m venv venv
venv\Scripts\activate # Windows
2. Install dependencies:
pip install -r requirements.txt

markdown
Copy code

3. Run Streamlit app:
streamlit run app.py

bash
Copy code

## 📌 Features
- Upload PDF
- Extract text
- Split into chunks
- Embed using SentenceTransformer
- Build FAISS vector DB
- Query & generate answers using FLAN-T5

