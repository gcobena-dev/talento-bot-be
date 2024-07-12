def chunk_by_words(text, chunk_size=300, overlap=10):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
        i += chunk_size - overlap
    return chunks

def chunk_mapping(datos):
    chunked_documents = []
    chunk_unique_id = 0
    for doc_id, document in enumerate(datos):
        chunks = chunk_by_words(document[1])
        for chunk_id, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": chunk_unique_id,
                "document_id": chunk_id,
                "person_id": document[0],
                "email": document[5],
                "name": document[4],
                "text": chunk
            })
            chunk_unique_id += 1

    chunk_id_mapping = {}
    for chunk in chunked_documents:
        chunk_id_mapping[chunk["id"]] = chunk

    return chunk_id_mapping