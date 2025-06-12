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

    print(f"Total texts loaded: {len(texts)}")
    return texts

