from pydantic import BaseModel, Field
from fastapi import  UploadFile, File


class DocumentUploadRequest(BaseModel):
    document_name: str = Field(..., description="File name from UI")
    document_file: UploadFile = File(..., description="File from UI")
    
class DocumentUpdateRequest(BaseModel):
    document_name: str = Field(..., description="File name from UI")
    document_file: UploadFile = File(..., description="File from UI")
    
class DocumentRetrieveRequest(BaseModel):
    document_id: str = Field(..., description="Document ID from UI")
    
class DocumentDeleteRequest(BaseModel):
    document_id: str = Field(..., description="Document ID from UI")
    