from pydantic import BaseModel, Field
from fastapi.responses import FileResponse


class DocumentUploadResponse(BaseModel):
    document_id: str = Field(..., description="The unique ID of the uploaded document.")
    status: str = Field(..., description="The upload status.")
    message: str = Field(..., description="A message describing the upload result.")
    created_at: str = Field(..., description="The date and time when the document was created.")


# class DocumentRetrieveResponse(BaseModel):
#     document: FileResponse = Field(..., description="The retrieved document file.")


class DocumentDeleteResponse(BaseModel):
    document_id: str = Field(..., description="The unique ID of the document to delete.")
    status: str = Field(..., description="The deletion status.")
    message: str = Field(..., description="A message describing the deletion result.")


class DocumentErrorResponse(BaseModel):
    document_id: str = Field(..., description="The document ID that caused the error.")
    status: str = Field(..., description="The error status.")
    message: str = Field(..., description="A message describing the error.")
