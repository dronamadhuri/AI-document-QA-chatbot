import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def create_vectorstore(chunks):
    embeddings = embedder.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return {"index": index, "chunks": chunks}

def search_vectorstore(vectordb, query, k=3):
    q_emb = embedder.encode([query])
    distances, ids = vectordb["index"].search(q_emb, k)
    results = [vectordb["chunks"][i] for i in ids[0]]
    return results
