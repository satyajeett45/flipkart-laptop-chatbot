from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from data_loader import load_laptop_data

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
data = load_laptop_data()

embeddings = model.encode(data["Description"].tolist())
index.add(np.array(embeddings))

def get_index():
    return index, data, embeddings, model