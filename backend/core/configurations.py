import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Configurations:
    # Qdrant Configurations
    QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
    QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))
    QDRANT_DOCUMENTS_COLLECTION = os.getenv('QDRANT_DOCUMENTS_COLLECTION', 'documents')
    QDRANT_SECTIONS_COLLECTION = os.getenv('QDRANT_SECTIONS_COLLECTION', 'sections')
    QDRANT_QUESTIONS_COLLECTION = os.getenv('QDRANT_QUESTIONS_COLLECTION', 'questions')
    
    # CouchDB Configurations
    COUCH_URL = os.getenv('COUCH_URL', 'http://localhost:5984')
    COUCH_DB_DOCUMENTS = os.getenv('COUCHDB_DOCUMENTS', 'documents')
    COUCH_DB_QUESTIONS = os.getenv('COUCHDB_QUESTIONS', 'questions')
    COUCH_DB_TAGS = os.getenv('COUCHDB_TAGS', 'tags')
    COUCH_DB_SECTIONS = os.getenv('COUCHDB_SECTIONS', 'sections')
    COUCH_DB_THREADS = os.getenv('COUCHDB_THREADS', 'threads')
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
    OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
    
    # Token Settings
    TOKEN_SIZE = int(os.getenv('TOKEN_SIZE', 500))
    OVERLAP = int(os.getenv('OVERLAP', 10))
    
    # User
    USERNAME = "Pranav Shivam"
    
    #File Path
    UPLOAD_DIR = "uploads"
    MEMORY_THRESOLD: int = 100 * 1024 * 1024
    CHUNK_SIZE: int = 1024 * 1024
    MAX_WORKER: int = 4
    PDF_FILE_TYPE: str = "pdf" 


# if __name__ == "__main__":
#     config = Configurations()
#     print(f"QDRANT_HOST: {config.QDRANT_HOST}")
#     print(f"QDRANT_PORT: {config.QDRANT_PORT}")
#     print(f"QDRANT_DOCUMENTS_COLLECTION: {config.QDRANT_DOCUMENTS_COLLECTION}")
#     print(f"QDRANT_SECTIONS_COLLECTION: {config.QDRANT_SECTIONS_COLLECTION}")
#     print(f"QDRANT_QUESTIONS_COLLECTION: {config.QDRANT_QUESTIONS_COLLECTION}")
#     print(f"COUCH_URL: {config.COUCH_URL}")
#     print(f"COUCH_DB_DOCUMENTS: {config.COUCH_DB_DOCUMENTS}")
#     print(f"COUCH_DB_QUESTIONS: {config.COUCH_DB_QUESTIONS}")
#     print(f"COUCH_DB_TAGS: {config.COUCH_DB_TAGS}")
#     print(f"COUCH_DB_SECTIONS: {config.COUCH_DB_SECTIONS}")
#     print(f"COUCH_DB_THREADS: {config.COUCH_DB_THREADS}")
#     print(f"OPENAI_API_KEY: {config.OPENAI_API_KEY}")
#     print(f"TOKEN_SIZE: {config.TOKEN_SIZE}")
#     print(f"OVERLAP: {config.OVERLAP}")
