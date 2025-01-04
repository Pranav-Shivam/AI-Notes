from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
# from core.db.couch_db.couch_schemas import CouchTagSchema
from couchdb import ResourceNotFound
from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import uuid4
import couchdb
from core.generate_unique_id import generate_unique_id, generate_unique_id_from_text

class CouchThreadDB:
    def __init__(self):
        self.couch_db = CouchDataBase()
        self.config = Configurations()
        self.thread_db = self.couch_db.get_or_create_db(self.config.COUCH_DB_THREADS)

    def create_threads(self, thread_data):
        """Create a new tag document in the database"""
        try:
            
            payload = thread_data.dict(by_alias=True)
            doc_id, doc_rev = self.thread_db.save(payload)
            return {"id": doc_id, "rev": doc_rev, "message": "Tag created successfully"}
        except couchdb.http.ResourceConflict:
            return {"message": "Conflict: Document already exists"}
        except Exception as e:
            return {"error": str(e)}