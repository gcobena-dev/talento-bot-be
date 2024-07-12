import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'resume.csv')
EMBEDDING_SIZE = 768
INDEX_NAME = os.path.join(os.path.dirname(__file__), '..', 'data', 'full-index.ann')
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'

if 'OPENAI_API_KEY' in os.environ:
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
else:
    OPENAI_API_KEY = None