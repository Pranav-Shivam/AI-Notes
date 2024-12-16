from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

# Documents Collection Schema
class DocumentSchema(BaseModel):
    # id: str = Field(..., alias="_id")
    document_name: str
    document_src: str
    date_time: str
    extension: str
    document_type: str
    document_text: str
    created_by: str
    updated_by: str
    tags: List[str]
    # permissions: Dict[str, List[str]]
    # metadata: Dict[str, Optional[int]]
# Sections Collection Schema
class SectionSchema(BaseModel):
    document_id: str
    date_time: str
    section: str
    token_count: Optional[int]
    tags: List[str]
    embeddings_version: str
    owner_id: str
    
# Tags Collection Schema
class TagSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    date_time: datetime
    tag: str
    owner_id: str



# Questions Collection Schema
class QuestionSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    date_time: datetime
    question: str
    answer: str
    tags: List[str]
    related_section_ids: List[str]
    created_by: str
    updated_by: str
    metadata: Dict[str, Optional[str]]
    
    
class UserSchema(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    updated_at: datetime
    roles: List[str]
    status: str
    metadata: Dict[str, Optional[str]]