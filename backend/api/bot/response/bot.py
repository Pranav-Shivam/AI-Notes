from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BotQueryResponse(BaseModel):
    query: str = Field(..., description="The query sent to the bot.")
    response: str = Field(..., description="The bot's response to the query.")
    document_ids: List[str] = Field(..., description="List of document IDs associated with the query.")
    tags : List[str] =  Field(..., description="List of document IDs associated with the query.")
    date_time: str = Field(..., description="The timestamp when the response was generated.")
    
class BotResponse(BaseModel):
    query: str = Field(..., description="The query sent to the bot.")
    response: str = Field(..., description="The bot's response to the query.")
    thread_id: str = Field(..., description="The bot's response to the query.")
    document_ids: List[str] = Field(..., description="List of document IDs associated with the query.")
    tags : List[str] =  Field(..., description="List of document IDs associated with the query.")
    date_time: str = Field(..., description="The timestamp when the response was generated.")


class BotDocumentsQueryResponse(BaseModel):
    query: str = Field(..., description="The query sent to the bot.")
    response: str = Field(..., description="The bot's response to the query.")
    document_ids: List[str] = Field(..., description="List of document IDs associated with the query.")
    tags : List[str] =  Field(..., description="List of document IDs associated with the query.")
    datetime: str = Field(..., description="The timestamp when the response was generated.")
