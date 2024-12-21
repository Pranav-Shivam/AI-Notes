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
            doc_id, doc_rev = self.documents_db.save(payload)
            return {"status": "success", "data": doc_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def delete_documents(self, document_id: str):
        try:
            doc= self.documents_db[document_id]
            self.documents_db.delete(doc)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_doc_by_id(self, document_id):
        doc = self.documents_db[document_id]
        return doc
    
    def get_document_field_by_id(self, document_id: str, field_name: str):
        doc = self.get_doc_by_id(document_id)
        return doc.get(field_name)
    
