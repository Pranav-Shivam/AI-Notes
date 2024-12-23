from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
from datetime import datetime

# Documents Collection Schema
class DocumentSchema(BaseModel):
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
class SectionSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    date_time: str
    section: str
    token_count: Optional[int]
    tags: List[str]
    embeddings_version: str
    owner_id: str

    class Config:
        populate_by_name = True  # Updated key

# Tags Collection Schema
class TagSchema(BaseModel):
    id: str = Field(..., alias="_id")
    document_id: str
    date_time: datetime
    tag: str
    owner_id: str

    class Config:
        populate_by_name = True  # Updated key

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

    class Config:
        populate_by_name = True  # Updated key

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

    class Config:
        populate_by_name = True  # Updated key
