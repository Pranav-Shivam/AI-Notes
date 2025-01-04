from pydantic import BaseModel, Field
from typing import List

class EmbeddingSchema(BaseModel):
    token_size: int = Field(..., description="Total token size of the chunk of text")
    section_chunk: str = Field(..., description="The chunk of text for which embeddings are generated")
    embeddings: List[float] = Field(..., description="OpenAI embeddings for the chunk of text")

class EmbeddingSchemaList(BaseModel):
    chunks: List[EmbeddingSchema]