import os
from annoy import AnnoyIndex
from src.utils.embedding import get_embedding
from src.config import INDEX_NAME, EMBEDDING_SIZE
from src.utils.chunker import chunk_mapping
from src.utils.data_loader import load_csv

# Configuración
embedding_size = 768  # Ajusta según el tamaño de tus embeddings
index_name = INDEX_NAME  # Nombre del archivo de índice Annoy

def build_annoy_index():
    # Inicializar AnnoyIndex
    index = AnnoyIndex(embedding_size, 'angular')  # 'angular' es un buen método para embeddings de texto
    datos = load_csv()
    chunk_id_mapping = chunk_mapping(datos)

    for idx, chunk in chunk_id_mapping.items():
        v = get_embedding("person_id: " + chunk["person_id"]+", email: " + chunk["email"]+", name: " + chunk["name"]+", resume: "+chunk["text"])
        index.add_item(idx, v)

    # Construir el índice y guardar en disco
    index.build(10)  # Ajusta el número de árboles (10 es un valor típico)
    index.save(index_name)

    print(f"Índice Annoy creado y guardado en {index_name}")

if __name__ == "__main__":
    build_annoy_index()

def load_index():
    index = AnnoyIndex(EMBEDDING_SIZE, 'angular')
    index.load(INDEX_NAME)
    return index