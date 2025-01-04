from pydantic import BaseModel, Field
from typing import List


class QuestionRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    tags: List[str] = Field(..., description="List of Tags relevant to the query.")
    
class QuestionAnswerRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    response: str
    document_id: str = Field(..., description="Document ID relevant to the query.")
    thread_id: str = Field(..., description="Thread ID relevant to the query.")
    tags: List[str] = Field(..., description="List of Tags relevant to the query.")

class BotDocumentsQueryRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    document_id: str = Field(..., description="Document ID relevant to the query.")
    thread_id: str = Field(..., description="Thread ID relevant to the query.")
    tags: List[str] = Field(..., description="List of Tags relevant to the query.")
    
class BotRequest(BaseModel):
    query: str = Field(..., description="Query from a bot.")
    document_id: str = Field(..., description="Document ID relevant to the query.")
    thread_id: str = Field(..., description="Thread ID relevant to the query.")
    tags: List[str] = Field(..., description="List of Tags relevant to the query.")