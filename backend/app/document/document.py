from app.document.indexer import PDFIndexer



def upload_documents(file_path):
    # Initialize indexer
    indexer = PDFIndexer(
        qdrant_host="localhost",
        qdrant_port=6333,
        collection_name="pdf_chunks",
        couch_url="http://root:root@localhost:5984",
        couch_db_name="pdf_store"
    )
    
    # Index a PDF file
    indexer.index_pdf(
        pdf_path=file_path,
        tags=["document", "research"]
    )
    return True