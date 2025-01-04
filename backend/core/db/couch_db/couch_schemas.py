from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Literal
from datetime import datetime

# Documents Collection Schema
class CouchDocumentSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_name: str
    document_src: str
    date_time: str
    extension: str
    document_type: str
    document_text: str
    created_by: str
    updated_by: str
    tags: List[str]
    file_size: str

    class Config:
        populate_by_name = True  # Updated key

# Sections Collection Schema
class CouchSectionSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    question_id: str
    date_time: str
    section: str
    token_count: Optional[int]
    tags: List[str]
    embeddings_version: str
    owner_id: str

    class Config:
        populate_by_name = True  # Updated key

# Tags Collection Schema
class CouchTagSchema(BaseModel):
    id: str = Field(..., alias="_id")
    # document_id: str
    # date_time: str
    tag: str
    # owner_id: str
    # question_id: str

    class Config:
        populate_by_name = True  # Updated key

# Questions Collection Schema
class CouchQuestionSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    thread_id: str
    date_time: str
    question: str
    answer: str
    created_by: str
    updated_by: str
    tags: List[str]
    #metadata: Dict[str, Optional[str]]

    class Config:
        populate_by_name = True  # Updated key

class CouchUserSchema(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    updated_at: datetime
    roles: List[str]
    status: str
    metadata: Dict[str, Optional[str]]

    class Config:
        populate_by_name = True  # Updated key

#Thread database
class ThreadMessageMetadata(BaseModel):
    query_type: Optional[str]
    related_document_id: Optional[str]
    related_section_ids: Optional[List[str]]
    embeddings_version: Optional[str]

class ThreadMessages(BaseModel):
    message_id: str
    timestamp: str
    sender: Literal["user", "bot"]
    query: str
    response: str
    # metadata: Optional[ThreadMessageMetadata]

class Permissions(BaseModel):
    read: List[str]
    write: List[str]

class ThreadMetadata(BaseModel):
    total_messages: Optional[int]
    average_response_time_ms: Optional[int]
    context: Optional[str]
    priority: Optional[str]

class ThreadMessageList(BaseModel):
    message: List[ThreadMessages] = Field(default_factory=list)

class CouchThreadSchema(BaseModel):
    id: str = Field(alias="_id")  # CouchDB document ID
    user_id: str
    created_at: str
    updated_at: str
    title: str
    status: Literal["active", "archived", "closed"]  # Strictly limited values
    tags: List[str]
    messages: ThreadMessageList
    # permissions: Permissions
    # metadata: Optional[ThreadMetadata]
    
    class Config:
        populate_by_name = True  # Updated key
