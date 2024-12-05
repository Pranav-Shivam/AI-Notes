from pydantic import BaseModel, Field
from fastapi.responses import FileResponse

class DocumentUploadResponse(BaseModel):
    response: str = Field(..., description="Response from from API")
    document_id: str = Field(..., description="Document ID from API")
    
    
# class DocumentRetrieveResponse(BaseModel):
#     document: FileResponse = Field(..., description="Document from API")
    
class DocumentDeleteResponse(BaseModel):
    response: str = Field(..., description="Response from API")
    