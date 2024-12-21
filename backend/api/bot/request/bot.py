from pydantic import BaseModel, Field
from typing import List


class BotQueryRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")

class BotDocumentsQueryRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    document_ids: List[str] = Field(..., description="List of document IDs relevant to the query.")
