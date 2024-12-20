from fastapi import FastAPI
from api.route.route import router as testroute
from api.document.document import document_router
import uvicorn
import nltk

nltk.download('punkt_tab')
app = FastAPI()
app.include_router(testroute)
app.include_router(document_router)



