from core.configurations import Configurations
from datetime import datetime
import couchdb
from typing import Dict, List, Optional, Any

class CouchDataBase:
    def __init__(self):
        """Initialize CouchDB connections for all collections"""
        self.config = Configurations()
        self.couch = couchdb.Server(self.config.COUCH_URL)
    
    def get_or_create_db(self, db_name):
        if db_name not in self.couch:
            return self.couch.create(db_name)
        return self.couch[db_name]

        
    # # Initialize all CouchDB databases
        # self.documents_db = self.db_couch.get_or_create_db(self.config.COUCH_DB_DOCUMENTS)
        # self.questions_db = self.db_couch.get_or_create_db(self.config.COUCH_DB_QUESTIONS)
        # self.tags_db = self.db_couch.get_or_create_db(self.config.COUCH_DB_TAGS)
        # self.sections_db = self.db_couch.get_or_create_db(self.config.COUCH_DB_SECTIONS)