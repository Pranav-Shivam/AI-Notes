from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from fastapi import HTTPException
# from core.db.couch_db.couch_schemas import QuestionSchema
from couchdb import ResourceNotFound
from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import uuid4
import couchdb
from core.generate_unique_id import generate_unique_id

class CouchQuestionDB:
    def __init__(self):
        self.couch_db = CouchDataBase()
        self.config = Configurations()
        self.question_db = self.couch_db.get_or_create_db(self.config.QDRANT_QUESTIONS_COLLECTION)

    def insert_question(self, question_data):
        try:
            payload= question_data.dict(by_alias=True)
            doc_id, doc_rev = self.question_db.save(payload)
            return {"status": "success", "data": doc_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))