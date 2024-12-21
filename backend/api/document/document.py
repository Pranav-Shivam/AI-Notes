from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from uuid import uuid4
from fastapi.responses import StreamingResponse
import os
from app.document.document import Documents
from core.configurations import Configurations
from .request.document import (
    DocumentRetrieveRequest,
    DocumentDeleteRequest
)
from .response.document import (
    DocumentUploadResponse,
    DocumentDeleteResponse
)

document_router = APIRouter(prefix="/api/documents", tags=["Documents"])

config = Configurations()
documents_services = Documents()


@document_router.post("/upload")
async def upload_document(document: UploadFile = File(...),tags: str =Form(...)):
    
    if not document.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    try:
        contents = await document.read()
        return documents_services.upload_documents(contents, tags, document.filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@document_router.get("/get/{document_id}")
async def get_document(document_id: str):  # Changed to directly accept document_id
    try:
        response = documents_services.get_document_by_id(document_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@document_router.delete("/delete/{document_id}")
async def delete_document(document_id : str):
    try:
        response = documents_services.delete_document_by_id(document_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

