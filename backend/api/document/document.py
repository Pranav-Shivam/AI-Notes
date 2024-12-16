from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from uuid import uuid4
import os
from app.document.document import Documents
from .request.document import (
    DocumentRetrieveRequest,
    DocumentDeleteRequest
)
from .response.document import (
    DocumentUploadResponse,
    DocumentDeleteResponse
)

document_router = APIRouter(prefix="/api/documents", tags=["Documents"])

# Configure your upload directory
UPLOAD_DIR = ("uploads")

# Check if the directory exists, if not, create it
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@document_router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(document: UploadFile = File(...), document_name: str = Form(...), tags: str =Form(...)):
    try:
        # Generate unique document ID
        document_id = str(uuid4())
        
        # Create file path
        file_extension = os.path.splitext(document_name)[1]
        file_path = os.path.join(UPLOAD_DIR, f"{document_id}{file_extension}")
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await document.read()
            buffer.write(content)
        
        # Calculate the file size in bytes
        file_size = os.path.getsize(file_path)
        
        response = Documents().upload_documents(pdf_path=file_path, tags=tags.split(","), doc_name= document_name, file_size=file_size)
        print(response)
        
        if (response == True) :
            return DocumentUploadResponse(
                response="Document uploaded successfully",
                document_id=document_id
            )
            
        else:
            return DocumentUploadResponse(
                response="Document uploaded not successfully",
                document_id=document_id
            ) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@document_router.get("/get/{document_id}")
async def get_document(document_id: str):  # Changed to directly accept document_id
    try:
        # Find the file in upload directory
        for filename in os.listdir(UPLOAD_DIR):
            if filename.startswith(document_id):
                file_path = os.path.join(UPLOAD_DIR, filename)
                return FileResponse(
                    path=file_path, 
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": "inline",
                        "Access-Control-Allow-Origin": "*"  # Add CORS header
                    }
                )
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@document_router.delete("/delete/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(document : DocumentDeleteRequest):
    try:
        # Find and delete the file
        for filename in os.listdir(UPLOAD_DIR):
            if filename.startswith(document.document_id):
                os.remove(os.path.join(UPLOAD_DIR, filename))
                return DocumentDeleteResponse(
                    response="Document deleted successfully"
                )
        raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

