import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from src.utils.data_loader import load_csv
from src.utils.chunker import chunk_mapping
from src.utils.indexer import load_index
from src.utils.embedding import get_embedding
from src.provider.api import get_answer

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/query':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Empty request body'}).encode())
                return
            
            try:
                request_body = json.loads(post_data)
            except json.JSONDecodeError as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid JSON in request body'}).encode())
                return
            
            question = request_body.get('question', None)
            response = handle_query(question)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not Found'}).encode())

def handle_query(question=None):
    if question is None or question.strip() == "":
        return {"response": "No question provided in the request body."}

    index = load_index()
    embedding_question = get_embedding(question)
    ids_potenciales_respuestas = index.get_nns_by_vector(embedding_question, 5)
    datos = load_csv()
    chunked_documents = chunk_mapping(datos)
    potenciales_respuestas = [chunked_documents[idx] for idx in ids_potenciales_respuestas]
    texto_potencial = [f"person_id: {chunk['person_id']}, email: {chunk['email']}, name: {chunk['name']}, resume: {chunk['text']}" for chunk in potenciales_respuestas]
    openai_response = get_answer(question, texto_potencial)
    return {"response": openai_response}

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()