from pydantic import BaseModel, Field
from typing import List

class QuestionAnswerResponse(BaseModel):
    query: str = Field(..., description="Query to a bot.")
    response: str = Field(..., description="Response from a bot.")
    tags: List[str] = Field(..., description="List of Tags relevant to the query.")
    
class SaveQuestionResponse(BaseModel):
    question_id: str = Field(..., description="Unique identifier of the saved question")
    status_code: int = Field(..., description="HTTP status code of the operation")
    message: str = Field(..., description="Response message indicating success or failure details")
    query: str = Field(..., description="The original query")
    response: str = Field(..., description="The response to the query")
    tags: List[str] = Field(default_factory=list, description="Associated tags")