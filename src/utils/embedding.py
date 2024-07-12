from sentence_transformers import SentenceTransformer
from src.config import MODEL_NAME

model = SentenceTransformer(MODEL_NAME)

def get_embedding(text):
    return model.encode(text)