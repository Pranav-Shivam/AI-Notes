import os
from typing import List, Dict, Any
import hashlib
from datetime import datetime

import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
import couchdb
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class PDFIndexer:
    def __init__(
        self,
        qdrant_host: str,
        qdrant_port: int,
        collection_name: str,
        couch_url: str,
        couch_db_name: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ):
        """
        Initialize the PDF indexer with database connections and parameters.
        
        Args:
            qdrant_host: Hostname for Qdrant server
            qdrant_port: Port for Qdrant server
            collection_name: Name of the Qdrant collection
            couch_url: URL for CouchDB server
            couch_db_name: Name of the CouchDB database
            chunk_size: Maximum size of text chunks in characters
            overlap: Number of characters to overlap between chunks
        """
        # Initialize embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Qdrant client
        self.qdrant = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = collection_name
        
        # Create Qdrant collection if it doesn't exist
        self.qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=self.model.get_sentence_embedding_dimension(),
                distance=models.Distance.COSINE
            )
        )
        
        # Initialize CouchDB client
        couch = couchdb.Server(couch_url)
        if couch_db_name not in couch:
            self.couch_db = couch.create(couch_db_name)
        else:
            self.couch_db = couch[couch_db_name]
            
        self.chunk_size = chunk_size
        self.overlap = overlap

    def generate_document_id(self, text: str, timestamp: str) -> str:
        """Generate a unique document ID based on text content and timestamp."""
        content_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{timestamp}_{content_hash}"

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def create_chunks(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap, trying to maintain sentence boundaries.
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap
                words = current_chunk.split()
                overlap_text = " ".join(words[-self.overlap:]) if len(words) > self.overlap else current_chunk
                current_chunk = overlap_text + " " + sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks

    def create_embeddings(self, chunks: List[str]) -> List[np.ndarray]:
        """Create embeddings for text chunks."""
        return self.model.encode(chunks)

    def store_in_databases(
        self,
        chunks: List[str],
        embeddings: List[np.ndarray],
        pdf_path: str,
        tags: List[str]
    ) -> None:
        """Store chunks and their embeddings in both databases."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate unique ID for the chunk
            doc_id = self.generate_document_id(chunk, f"{timestamp}_{i}")
            
            # Prepare payload
            payload = {
                "document_id": doc_id,
                "text": chunk,
                "tags": tags,
                "source_file": pdf_path,
                "chunk_index": i,
                "timestamp": timestamp
            }
            
            # Store in Qdrant
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=i,
                        vector=embedding.tolist(),
                        payload=payload
                    )
                ]
            )
            
            print("embdding : ", i ," ",embedding.tolist())
            # Store in CouchDB
            self.couch_db[doc_id] = payload

    def index_pdf(self, pdf_path: str, tags: List[str] = None) -> None:
        """
        Main method to index a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            tags: List of tags to associate with the document
        """
        if tags is None:
            tags = []
            
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = self.create_chunks(text)
        
        # Create embeddings
        embeddings = self.create_embeddings(chunks)
        
        # Store in databases
        self.store_in_databases(chunks, embeddings, pdf_path, tags)
    

# Example usage
if __name__ == "__main__":
    # Initialize indexer
    indexer = PDFIndexer(
        qdrant_host="localhost",
        qdrant_port=6333,
        collection_name="pdf_chunks",
        couch_url="http://admin:password@localhost:5984",
        couch_db_name="pdf_store"
    )
    
    # Index a PDF file
    indexer.index_pdf(
        pdf_path="path/to/your/document.pdf",
        tags=["document", "research"]
    )