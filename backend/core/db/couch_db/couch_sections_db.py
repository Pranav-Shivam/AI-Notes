from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from core.db.couch_db.couch_schemas import SectionSchema
from couchdb import ResourceNotFound
from datetime import datetime
from typing import List, Dict, Any
from uuid import uuid4
import couchdb
from core.generate_unique_id import generate_unique_id
from fastapi import APIRouter, UploadFile, File, HTTPException, Form


class CouchSectionDB:
    def __init__(self):
        self.couch_db = CouchDataBase()
        self.config = Configurations()
        self.sections_db = self.couch_db.get_or_create_db(self.config.COUCH_DB_SECTIONS)

    def create_section(self, section_data):
        try:
            payload = section_data.dict(by_alias=True)
            doc_id, doc_rev = self.sections_db.save(payload)
            return {"status": "success", "data": doc_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def delete_section(self, section_id: str):
        try:
            doc= self.sections_db[section_id]
            self.sections_db.delete(doc)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_doc_by_id(self, section_id: str):
        doc = self.documents_db[section_id]
        return doc
    
    def get_section_field_by_id(self, section_id: str, field_name: str):
        doc = self.get_doc_by_id(section_id)
        return doc.get(field_name)
    
    def delete_all_document_ids_sections(self, document_id):
        try:
            db =  self.sections_db
            for doc_id in db:
                doc = db[doc_id]
                if doc.get('document_id') == document_id:
                    db.delete(doc)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_all_section_ids_by_document_id(self, document_id: str):
        try:
            query_result = self.sections_db.find({
                "selector": {"document_id": document_id},
                "fields": ["_id"]
            })
            section_ids = [doc["_id"] for doc in query_result]
            return section_ids
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))