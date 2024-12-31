from typing import List, Dict, Any, Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    PointStruct, 
    Filter, 
    FieldCondition, 
    MatchValue, 
    UpdateResult, 
    ScoredPoint,
    Distance,
    VectorParams,
    OptimizersConfigDiff,
    SearchParams
)
from qdrant_client.http import models as qdrant_models
from core.configurations import Configurations
from fastapi import HTTPException

class QdrantDataBase:
    
    def __init__(self):
        """Initialize the QdrantDatabase with configuration and client connection."""
        self.config = Configurations()
        self.client = self.connect_qdrant_db()
        
    def connect_qdrant_db(self) -> QdrantClient:
        try:
            client = QdrantClient(host=self.config.QDRANT_HOST, port=self.config.QDRANT_PORT)
            # Test connection
            client.get_collections()
            return client
        except Exception as e:
            raise HTTPException(status_code=500, detail="Database connection failed")

    def recreate_collection(self, 
                          coll_name: str, 
                          vector_size: int = 1536, 
                          distance: Distance = Distance.COSINE) -> None:
        try:
            # Delete if exists
            if self.client.collection_exists(coll_name):
                self.client.delete_collection(coll_name)
            
            # Create new collection
            self.client.create_collection(
                collection_name=coll_name,
                vectors_config={
                    "text_vector": VectorParams(size=vector_size, distance=distance)
                },
                optimizers_config=OptimizersConfigDiff(
                    indexing_threshold=20000,
                    memmap_threshold=50000
                )
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to recreate collection: {str(e)}")

    def upsert_points(self, 
                     coll_name: str, 
                     points: List[PointStruct]) -> UpdateResult:
        try:
            result = self.client.upsert(collection_name=coll_name, points=points)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upsert points: {str(e)}")

    def search_query(self,
                    coll_name: str, 
                    query_vector: List[float], 
                    query_vector_name: str = "text_vector",
                    filter: Optional[Filter] = None,
                    top_k: int = 5,
                    score_threshold: Optional[float] = None) -> List[ScoredPoint]:
        try:
            search_results = self.client.search(
                collection_name=coll_name,
                query_vector=(query_vector_name, query_vector),  # Pass the actual vector
                with_payload=True,
                limit=top_k
            )
            return search_results
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete_points(self, 
                     coll_name: str, 
                     points_ids: List[str]) -> UpdateResult:
        try:
            result = self.client.delete(
                collection_name=coll_name,
                points_selector=points_ids
            )
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete points: {str(e)}")

    def get_collection_info(self, coll_name: str) -> Dict[str, Any]:
        try:
            info = self.client.get_collection(collection_name=coll_name)
            return info.dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get collection info: {str(e)}")