from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from core.db.couch_db.couch_schemas import DocumentSchema
from couchdb import ResourceNotFound
from datetime import datetime
from typing import Dict, Any
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import couchdb

class CouchDocumentsDB:
    def __init__(self):
        self.couch_db = CouchDataBase()
        self.config = Configurations()
        self.documents_db = self.couch_db.get_or_create_db(self.config.COUCH_DB_DOCUMENTS)

    def create_documents(self, document_data):
        try:
            payload = document_data.dict(by_alias=True)
            print(f"Saving document: {payload}")
            doc_id, doc_rev = self.documents_db.save(payload)
            print(f"Document saved with ID: {doc_id}, Rev: {doc_rev}")
            return {"status": "success", "data": doc_id}
        except Exception as e:
            print(f"Error saving document: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
