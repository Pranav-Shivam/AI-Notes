from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from core.db.couch_db.couch_schemas import CouchThreadSchema, ThreadMessages
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
    
    def get_thread_by_id(self, thread_id: str):
        doc = self.thread_db[thread_id]
    
    def get_query_response_by_thread_id(self, thread_id: str):
        
        doc = self.get_thread_by_id(thread_id)
        if not doc:
            return []
        
        try:
            couch_thread = CouchThreadSchema(**doc)
            queries_responses = [
                {'query': msg.query, 'response': msg.response}
                for msg in couch_thread.messages.message
            ]
            return queries_responses
        except Exception as e:
            return []
    

    def append_message_to_thread(self, thread_id: str, query: str, response: str):
        
        doc = self.get_thread_by_id(thread_id)
        if not doc:
            return {"error": "Thread not found"}
        
        try:
            # Update the updated_at field
            updated_at = datetime.utcnow().isoformat()
            doc['updated_at'] = updated_at
            
            # Create a new message
            new_message = ThreadMessages(
                message_id=str(len(doc.get('messages', {}).get('message', [])) + 1),
                timestamp=updated_at,
                sender="bot",  # or "user" depending on who sends the message
                query=query,
                response=response
            )
            
            # Append the new message
            if 'messages' not in doc:
                doc['messages'] = {'message': []}
            doc['messages']['message'].append(new_message.dict())
            
            # Save the updated document
            doc_id, doc_rev = self.thread_db.save(doc)
            return {"id": doc_id, "rev": doc_rev, "message": "Message appended successfully"}
        except Exception as e:
            return {"error": str(e)}  
        
    
    def check_for_thread(self, thread_id:str):
        if thread_id in self.thread_db:
            return True
        return False
        
        