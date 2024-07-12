from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils.data_loader import load_csv
from src.utils.chunker import chunk_mapping
from src.utils.indexer import load_index
from src.utils.embedding import get_embedding
from src.provider.api import get_answer
import os

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(request: QueryRequest):
    question = request.question
    if not question.strip():
        raise HTTPException(status_code=400, detail="No question provided in the request body.")
    
    response = handle_query(question)
    return {"response": response}

def handle_query(question):
    index = load_index()
    embedding_question = get_embedding(question)
    ids_potenciales_respuestas = index.get_nns_by_vector(embedding_question, 5)
    datos = load_csv()
    chunked_documents = chunk_mapping(datos)
    potenciales_respuestas = [chunked_documents[idx] for idx in ids_potenciales_respuestas]
    texto_potencial = [f"person_id: {chunk['person_id']}, email: {chunk['email']}, name: {chunk['name']}, resume: {chunk['text']}" for chunk in potenciales_respuestas]
    openai_response = get_answer(question, texto_potencial)
    return openai_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
