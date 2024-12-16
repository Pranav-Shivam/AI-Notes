#imports
from core.db.couch_db.couch_documents_db import CouchDocumentsDB
from core.db.couch_db.couch_tags_db import CouchTagDB
from core.db.couch_db.couch_sections_db import CouchSectionDB
from core.configurations import Configurations
from core.embeddings.get_embedding import EmbeddingModels
from core.db.qdrant_db.connect_qdrant_db import QdrantDataBase
from datetime import datetime
import tiktoken
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from core.db.qdrant_db.qdrant_schemas import QdrantSection
from core.db.qdrant_db.qdrant_questions_db import QdrantQuestionDB
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB
import re
import fitz  # PyMuPDF
from typing import List, Dict, Any
from core.generate_unique_id import generate_unique_id, generate_unique_id_from_text
from core.db.couch_db.couch_schemas import DocumentSchema, QuestionSchema, TagSchema, SectionSchema, UserSchema


class PDFIndexer:
    
    def __init__(self):
        #Initialize configuarations and databases
        self.config = Configurations()
        self.qdrant = QdrantDataBase()
        self.qdrant_sections_db =QdrantSectionDB()
        self.couch_document_db = CouchDocumentsDB()
        self.couch_tag_db = CouchTagDB()
        self.couch_section_db = CouchSectionDB()
        self.embed = EmbeddingModels()
        self.doc_id = ""
        self.token_size = self.config.TOKEN_SIZE
        self.user = self.config.USERNAME
    
    def store_in_db(self, document_name, src_path, document_type, document_content, current_user, tags, file_size, sections):
    # Check if document already exists
        current_date_time = datetime.now()
        current_date_time = str(current_date_time)
        # Create and log document data
        doc_data = DocumentSchema(
            _id=self.doc_id,
            document_name=document_name,
            document_src=src_path,
            date_time=current_date_time,
            extension=".pdf",
            document_type=document_type,
            document_text=document_content,
            created_by=current_user,
            updated_by=current_user,
            tags=tags
        )

        # Save document
        try:
            response = self.couch_document_db.create_documents(doc_data)
        except HTTPException as e:
            raise e

        # Create sections
        for sec in sections:
            section = sec["section"]
            embeddings = sec["embeddings"]
            token_count = sec["token_size"]
            section_id = generate_unique_id()

            # Create and log section data
            section_couch_data = SectionSchema(
                _id=section_id,
                document_id=self.doc_id,
                date_time=current_date_time,
                section=section,
                token_count=token_count,
                tags=tags,
                embeddings_version="Current_version",
                owner_id=current_user
            )

            # Save section
            try:
                response = self.couch_section_db.create_section(section_couch_data)
            except HTTPException as e:
                raise e

            # Save section in Qdrant
            try:
                section_qdrant_data = QdrantSection(
                    id=section_id,
                    vector={"text_vector": embeddings},
                    payload={
                        "document_id": self.doc_id,
                        "content": section,
                        "token_count": token_count,
                        "tags": tags,
                        "embeddings_version": "Current_version",
                        "owner_id": current_user,
                        "metadata": {"additional_info": None}
                    }
                )
                self.qdrant_sections_db.insert_section(section=section_qdrant_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                
        
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
    def count_tokens(self, text):
        # Initialize tiktoken encoder (use the encoder for your chosen model, e.g., GPT-3.5)
        encoder = tiktoken.get_encoding("cl100k_base")
        """Return the number of tokens in the provided text using tiktoken."""
        return len(encoder.encode(text))
        
    def generate_chunks_with_embeddings(self, text: str) -> List[Dict]:
        """
        Chunk the text into smaller parts considering token limits, while avoiding sentence splits.
        Each chunk includes the token size, the section, and its embeddings.
        """
        # Generate a unique ID for the document
        self.doc_id = generate_unique_id_from_text(text)
        
        # Split the text into sentences based on punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)  
        
        # Initialize variables
        chunks = []
        current_chunk = ""
        chunks_with_embeddings = []

        # Loop through each sentence to build chunks
        for sentence in sentences:
            sentence = sentence.strip()
            # Check if adding the sentence to the current chunk exceeds the token limit
            if self.count_tokens(current_chunk + " " + sentence) > self.token_size:
                if current_chunk:
                    # Generate embeddings and store the current chunk's details
                    chunk_embeddings = self.embed.generate_embeddings(current_chunk)
                    chunks_with_embeddings.append({
                        "token_size": self.count_tokens(current_chunk),
                        "section": current_chunk,
                        "embeddings": chunk_embeddings
                    })
                    chunks.append(current_chunk)
                
                # Start a new chunk with the current sentence
                current_chunk = sentence
            else:
                # Add the sentence to the current chunk
                current_chunk += " " + sentence if current_chunk else sentence

        # Handle the final chunk
        if current_chunk:
            chunk_embeddings = self.embed.generate_embeddings(current_chunk)
            chunks_with_embeddings.append({
                "token_size": self.count_tokens(current_chunk),
                "section": current_chunk,
                "embeddings": chunk_embeddings
            })
            chunks.append(current_chunk)

        return chunks_with_embeddings
    
        
    def index_pdf(self, pdf_path, tags, doc_name, file_size):
        """
        Main method to index a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            tags: List of tags to associate with the document
        """
        if tags is None:
            tags = []
        
        text = self.extract_text_from_pdf(pdf_path)
        
        chunks = self.generate_chunks_with_embeddings(text)
        
        self.store_in_db(document_name= doc_name,
                         src_path= pdf_path,
                         document_type="pdf",
                         document_content = text,
                         current_user= self.user,
                         tags= tags,
                         file_size= file_size,
                         sections= chunks)
        
         
        
        
            
            
             
            
        
        
        
        
        
        