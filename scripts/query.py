import faiss
import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Chargement
index = faiss.read_index("embeddings/lol.index")
with open("embeddings/texts.pkl", "rb") as f:
    texts = pickle.load(f)

# Requête
query = "épée pour infliger des dégâts magiques"
query_embedding = model.encode([query])
D, I = index.search(np.array(query_embedding), k=5)

print("Résultats :")
for i in I[0]:
    print(texts[i])
