from transformers import pipeline

qa_model = pipeline("text2text-generation", model="google/flan-t5-base")

def answer_question(query, docs):
    context = " ".join(docs)
    prompt = f"Answer the question based only on this text: {context}\n\nQuestion: {query}"
    ans = qa_model(prompt, max_length=200)[0]["generated_text"]
    return ans
