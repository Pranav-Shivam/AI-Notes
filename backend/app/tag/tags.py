from pydantic import Field, BaseModel
from core.configurations import Configurations
from core.db.couch_db.couch_tags_db import CouchTagDB

class Tag(BaseModel):
    tag: str
    

class TagService:
    def __init__(self) -> None:
        self.config = Configurations()
    
    def get_all_tags(self):
        pass
    
    def update_a_tag(self, old, new):
        pass
    
    def add_a_tag_to_db(self, tag):
        pass