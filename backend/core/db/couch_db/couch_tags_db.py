from core.db.couch_db.connect_couch_db import CouchDataBase
from core.configurations import Configurations
from core.db.couch_db.couch_schemas import TagSchema
from couchdb import ResourceNotFound
from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import uuid4
import couchdb
from core.generate_unique_id import generate_unique_id

class CouchTagDB:
    def __init__(self):
        self.couch_db = CouchDataBase()
        self.config = Configurations()
        self.tags_db = self.couch_db.get_or_create_db(self.config.COUCH_DB_TAGS)

    def create_tag(self, tag_data: TagSchema) -> Dict[str, Any]:
        """Create a new tag document in the database"""
        tag_data.id = generate_unique_id() # Assign a unique ID
        tag_data.date_time = datetime.utcnow()  # Set current time as date_time if not provided
        try:
            doc_id, doc_rev = self.tags_db.save(tag_data.dict())
            return {"id": doc_id, "rev": doc_rev, "message": "Tag created successfully"}
        except couchdb.http.ResourceConflict:
            return {"message": "Conflict: Document already exists"}
        except Exception as e:
            return {"error": str(e)}

    def get_tag_by_id(self, tag_id: str) -> Dict[str, Any]:
        """Retrieve a tag by its ID"""
        try:
            tag = self.tags_db.get(tag_id)
            if tag:
                return {"tag": tag}
            else:
                return {"message": "Tag not found"}
        except ResourceNotFound:
            return {"message": "Tag not found"}
        except Exception as e:
            return {"error": str(e)}

    def update_tag(self, tag_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing tag by its ID"""
        try:
            tag = self.tags_db.get(tag_id)
            if tag:
                tag.update(updated_data)
                self.tags_db.save(tag)
                return {"message": "Tag updated successfully"}
            else:
                return {"message": "Tag not found"}
        except ResourceNotFound:
            return {"message": "Tag not found"}
        except Exception as e:
            return {"error": str(e)}

    def delete_tag(self, tag_id: str) -> Dict[str, Any]:
        """Delete a tag by its ID"""
        try:
            tag = self.tags_db.get(tag_id)
            if tag:
                self.tags_db.delete(tag)
                return {"message": "Tag deleted successfully"}
            else:
                return {"message": "Tag not found"}
        except ResourceNotFound:
            return {"message": "Tag not found"}
        except Exception as e:
            return {"error": str(e)}

    def get_all_tags(self, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Retrieve all tags with pagination"""
        try:
            rows = self.tags_db.view("_all_docs", include_docs=True, limit=limit, skip=skip)
            tags = [row.doc for row in rows]
            return {"tags": tags}
        except Exception as e:
            return {"error": str(e)}

    def get_tags_by_owner(self, owner_id: str, limit: int = 10, skip: int = 0) -> Dict[str, Any]:
        """Retrieve tags by owner ID"""
        try:
            rows = self.tags_db.view("owner/by_owner", key=owner_id, include_docs=True, limit=limit, skip=skip)
            tags = [row.doc for row in rows]
            return {"tags": tags}
        except Exception as e:
            return {"error": str(e)}
