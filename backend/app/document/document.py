from app.document.indexer import PDFIndexer
from dotenv import load_dotenv
from core.configurations import Configurations
from fastapi.responses import StreamingResponse
from core.db.couch_db.couch_documents_db import CouchDocumentsDB
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB
from core.db.couch_db.couch_tags_db import CouchTagDB
from core.db.couch_db.couch_sections_db import CouchSectionDB
from fastapi.responses import FileResponse
from api.document.response.document import DocumentDeleteResponse, DocumentErrorResponse, DocumentUploadResponse
from typing import List, Dict, Generator
import fitz
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor
import math
from fastapi import HTTPException
from datetime import datetime

import os

# Load environment variables
load_dotenv()

class Documents:
    def __init__(self):
        self.config = Configurations()
        self.pdf_indexer = PDFIndexer()
        self.couch_document_db = CouchDocumentsDB()
        self.couch_tag_db = CouchTagDB()
        self.couch_section_db = CouchSectionDB()
        self.qdrant_sections_db =QdrantSectionDB()
    
    def upload_documents(self, pdf_contents, tags, document_name):
        # Parse tags into a list
        try:
            tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid format for tags")
        response = self.pdf_indexer.process_pdf(pdf_content= pdf_contents, tags= tags_list, document_name= document_name)
        if isinstance(response, DocumentErrorResponse):
            raise HTTPException(status_code=500, detail=response.message)

        return response
        
    
    def get_document_by_id(self, document_id: str):
        try:
            # Construct the file path directly
            if document_id.endswith(self.config.PDF_FILE_TYPE):
                document_path = os.path.join(self.config.UPLOAD_DIR, document_path)
            else:
                document_path = f"{document_id}.{self.config.PDF_FILE_TYPE}"
                document_path = os.path.join(self.config.UPLOAD_DIR, document_path)
            
            # Check if the file exists
            if os.path.exists(document_path):
                return FileResponse(
                    path=document_path, 
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": "inline",
                        "Access-Control-Allow-Origin": "*"  # Add CORS header
                    }
                )
            
            # If the file does not exist, return a 404 error
            return DocumentErrorResponse(
                status="404",
                message="File Not Found. Sorry, try again with another file.",
                document_id=document_id
            )

        except Exception as e:
            # Handle unexpected errors
            return DocumentErrorResponse(
                status="500",
                message=f"An unexpected error occurred: {str(e)}",
                document_id=document_id
            )
            
    def delete_document_by_id(self, document_id: str):
        try:
            if document_id.endswith(self.config.PDF_FILE_TYPE):
                document_path = os.path.join(self.config.UPLOAD_DIR, document_id)
            else: 
                document_path = f"{document_id}.{self.config.PDF_FILE_TYPE}"
                document_path = os.path.join(self.config.UPLOAD_DIR, document_path)
            # Check if the file exists
            if os.path.exists(document_path):
                os.remove(document_path)
                # delete the document
                self.couch_document_db.delete_documents(document_id= document_id)
                self.couch_section_db.delete_all_document_ids_sections(document_id=document_id)
                return DocumentDeleteResponse(
                    document_id=document_id,
                    status="200",
                    message=f"File '{document_id}' deleted successfully."
                )
            else:
                # File not found, return a 404 error
                return DocumentErrorResponse(
                    document_id=document_id,
                    status="404",
                    message="File Not Found. Sorry, try again with another file."
                )
            
            
        except Exception as e:
            # Return a generic error response
            return DocumentErrorResponse(
                document_id=document_id,
                status="500",
                message=f"An error occurred while deleting the file: {str(e)}"
            ) 
            
    
    
    
    
