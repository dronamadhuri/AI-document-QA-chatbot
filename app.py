import streamlit as st
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ---------------------
# 1. Load HF Model
# ---------------------
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)

# ---------------------
# 2. Streamlit UI
# ---------------------
st.title("📘 PDF Question Answering App")
st.write("Upload a PDF and ask questions from its content.")

# ---------------------
# 3. PDF Upload
# ---------------------
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    st.success("PDF loaded successfully!")

    # ---------------------
    # 4. Split text into chunks
    # ---------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)

    # ---------------------
    # 5. Build Embedding Model
    # ---------------------
    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ---------------------
    # 6. Create FAISS VectorDB
    # ---------------------
    vectordb = FAISS.from_texts(chunks, embed_model)

    # ---------------------
    # 7. Ask Query
    # ---------------------
    query = st.text_input("Ask a question based on the PDF")

    if query:
        results = vectordb.similarity_search(query, k=3)
        context = "\n\n".join([r.page_content for r in results])

        # ---------------------
        # 8. Build Prompt
        # ---------------------
        prompt = f"""
You are an assistant. Use ONLY the context below to answer.
If the answer is not in the context, say "Information not found in PDF."

Context:
{context}

Question: {query}

Answer:
"""

        # ---------------------
        # 9. Generate Answer
        # ---------------------
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.3
        )

        answer = tokenizer.decode(output[0], skip_special_tokens=True)

        st.subheader("📌 Answer")
        st.write(answer)
