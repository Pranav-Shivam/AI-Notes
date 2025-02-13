from core.db.couch_db.couch_thread_db import CouchThreadDB

class ThreadService:
    def __init__(self, thread_id):
        self.thread_id = thread_id
        self.db = CouchThreadDB()
    
    def fetch_latest_context(self):
        self.db.fetch_latest_context(self.thread_id)
    
    def add_new_context(self, context):
        self.db.add_new_context(context, thread_id=self.thread_id)
    
    def delete(self):
        pass
    
    