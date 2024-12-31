from pydantic import BaseModel, Field
from typing import List


class BotQueryRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")

class BotDocumentsQueryRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    document_ids: List[str] = Field(..., description="List of document IDs relevant to the query.")
    
class BotRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    document_id: str = Field(..., description="Document ID relevant to the query.")
    thread_id: str = Field(..., description="Thread ID relevant to the query.")
    tags: str = Field(..., description="List of Tags relevant to the query.")
