from embedder import get_index
import numpy as np

def retrieve_similar_docs(query, top_k=5):
    index, data, _, model = get_index()
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), top_k)
    return data.iloc[I[0]]