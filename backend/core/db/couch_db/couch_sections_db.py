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
            print(f"Saving section: {payload}")
            doc_id, doc_rev = self.sections_db.save(payload)
            print(f"Section saved with ID: {doc_id}, Rev: {doc_rev}")
            return {"status": "success", "data": doc_id}
        except Exception as e:
            print(f"Error saving section: {e}")
            raise HTTPException(status_code=500, detail=str(e))