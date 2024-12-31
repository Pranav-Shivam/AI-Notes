from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class SectionMetadata(BaseModel):
    additional_info: Optional[str] = None

class QdrantSection(BaseModel):
    id: str = Field(..., description="Unique identifier for the section")
    vector: Dict[str, Any] = Field(..., description="Vector representation")
    payload: Dict[str, Any] = Field(..., description="Section payload details")

class SectionPayload(BaseModel):
    document_id: str
    content: str
    token_count: int
    tags: List[str] = []
    embeddings_version: str
    owner_id: str
    metadata: Optional[SectionMetadata] = None

class QdrantSectionResponse(BaseModel):
    section: str
    score: float

class QdrantSectionResponseList(BaseModel):
    sections: List[QdrantSectionResponse]

class QuestionMetadata(BaseModel):
    source: Optional[str] = None
    context: Optional[str] = None

class QdrantQuestion(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    vector: List[float] = Field(..., description="Vector representation")
    payload: Dict[str, Any] = Field(..., description="Question payload details")

class QuestionPayload(BaseModel):
    document_id: str
    question: str
    answer: str
    tags: List[str] = []
    related_section_ids: List[str] = []
    embeddings_version: str
    owner_id: str
    metadata: Optional[QuestionMetadata] = None