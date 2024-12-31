from pydantic import BaseModel
from typing import List, Dict, Optional

class BotTagResponse(BaseModel):
    tags: List[str]

class DocumentIdResponse(BaseModel):
    document_ids: List[str]

class SectionList(BaseModel):
    sections: List[str]