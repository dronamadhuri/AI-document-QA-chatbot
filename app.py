import streamlit as st
from PyPDF2 import PdfReader

# ================= STREAMLIT UI =================
st.title("📘 DOCUMENT QA-SYSTEM")
st.write("Upload a PDF and ask questions.")

# ================= UPLOAD PDF =================
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.success("PDF loaded successfully!")

    # ================= ASK QUESTIONS =================
    query = st.text_input("Ask a question about the PDF:")

    if query:
        query_lower = query.lower()
        text_lower = text.lower()

        if query_lower in text_lower:
            st.subheader("📌 Answer (Found in PDF):")
            st.write(f"The PDF contains your query: **{query}**")
        else:
            # simple keyword search
            keywords = query_lower.split()
            sentences = text.split(".")
            matches = []

            for sentence in sentences:
                if any(word in sentence.lower() for word in keywords):
                    matches.append(sentence.strip())

            if matches:
                st.subheader("📌 Possible Answers:")
                for match in matches[:5]:
                    st.write(f"- {match}")
            else:
                st.subheader("📌 Answer:")
                st.write("Information not found in PDF.")
