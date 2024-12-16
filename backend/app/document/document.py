from app.document.indexer import PDFIndexer
from dotenv import load_dotenv
from core.configurations import Configurations
import os

# Load environment variables
load_dotenv()

class Documents:
    def __init__(self):
        self.config = Configurations()
        self.pdf_indexer = PDFIndexer() 
    
    def upload_documents(self, pdf_path, tags, doc_name, file_size):
        self.pdf_indexer.index_pdf(pdf_path, tags, doc_name, file_size)
        return True
        
    