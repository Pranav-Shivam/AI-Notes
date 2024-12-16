from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from core.db.couch_db.couch_schemas import QuestionSchema
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

    def create_question(self, question_data: QuestionSchema) -> Dict[str, Any]:
        """Create a new question document in the database"""
        question_data.id =   generate_unique_id() # Assign a unique ID
        question_data.date_time = datetime.utcnow()  # Set current time as date_time if not provided
        try:
            doc_id, doc_rev = self.question_db.save(question_data.dict())
            return {"id": doc_id, "rev": doc_rev, "message": "Question created successfully"}
        except couchdb.http.ResourceConflict:
            return {"message": "Conflict: Document already exists"}
        except Exception as e:
            return {"error": str(e)}

    def get_question_by_id(self, question_id: str) -> Dict[str, Any]:
        """Retrieve a question by its ID"""
        try:
            question = self.question_db.get(question_id)
            if question:
                return {"question": question}
            else:
                return {"message": "Question not found"}
        except ResourceNotFound:
            return {"message": "Question not found"}
        except Exception as e:
            return {"error": str(e)}

    def update_question(self, question_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing question by its ID"""
        try:
            question = self.question_db.get(question_id)
            if question:
                question.update(updated_data)
                self.question_db.save(question)
                return {"message": "Question updated successfully"}
            else:
                return {"message": "Question not found"}
        except ResourceNotFound:
            return {"message": "Question not found"}
        except Exception as e:
            return {"error": str(e)}

    def delete_question(self, question_id: str) -> Dict[str, Any]:
        """Delete a question by its ID"""
        try:
            question = self.question_db.get(question_id)
            if question:
                self.question_db.delete(question)
                return {"message": "Question deleted successfully"}
            else:
                return {"message": "Question not found"}
        except ResourceNotFound:
            return {"message": "Question not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_all_questions(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Retrieve all questions with pagination"""
        try:
            rows = self.question_db.view("_all_docs", include_docs=True, limit=limit, skip=skip)
            questions = [row.doc for row in rows]
            return {"questions": questions}
        except Exception as e:
            return {"error": str(e)}

    def search_questions_by_tag(self, tag: str, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Search questions by tag"""
        try:
            rows = self.question_db.view("tags/by_tag", key=tag, include_docs=True, limit=limit, skip=skip)
            questions = [row.doc for row in rows]
            return {"questions": questions}
        except Exception as e:
            return {"error": str(e)}

    def get_questions_by_owner(self, owner_id: str, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Retrieve questions by owner ID"""
        try:
            rows = self.question_db.view("owner/by_owner", key=owner_id, include_docs=True, limit=limit, skip=skip)
            questions = [row.doc for row in rows]
            return {"questions": questions}
        except Exception as e:
            return {"error": str(e)}
