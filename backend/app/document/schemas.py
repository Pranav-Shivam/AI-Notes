from pydantic import BaseModel
from typing import List, Dict, Optional

class PageContent(BaseModel):
    page: int
    content: str
    error: Optional[str] = None

class ChunkResponse(BaseModel):
    total_pages: int
    current_chunk: Dict[str, int]
    content: List[PageContent]
    
class BotTagResponse(BaseModel):
    tags: List[str]
