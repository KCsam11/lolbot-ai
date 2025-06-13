import os
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === CONFIGURATION ===
DATA_DIR = "data"
EMBEDDINGS_DIR = "embeddings"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# === CHARGER LES TEXTES ===
def load_texts():
    texts = []

    # Charger champions
    with open("data/champions_formatted.txt", "r", encoding="utf-8") as f:
        texts += [chunk.strip() for chunk in f.read().split("\n\n") if chunk.strip()]

    #charger champions details
    with open("data/detail_champions_formatted.txt", "r", encoding="utf-8") as f:
        texts += [chunk.strip() for chunk in f.read().split("\n\n") if chunk.strip()]

    # Charger items
    with open("data/items_formatted.txt", "r", encoding="utf-8") as f:
        texts += [chunk.strip() for chunk in f.read().split("\n\n") if chunk.strip()]

    return texts

# === CHARGER LE MODÈLE D'EMBEDDING ===
textes = load_texts()
model = SentenceTransformer(EMBEDDING_MODEL)
embeddings = model.encode(textes, show_progress_bar=True)

dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, "lol.index"))

with open(os.path.join(EMBEDDINGS_DIR, "texts.pkl"), "wb") as f:
    pickle.dump(textes, f)

index = faiss.read_index("embeddings/lol.index")
with open("embeddings/texts.pkl", "rb") as f:
    texts = pickle.load(f)

query = ""
query_embedding = model.encode([query])
D, I = index.search(np.array(query_embedding), k=5)

print("Résultats :")
for i in I[0]:
    print(texts[i])
