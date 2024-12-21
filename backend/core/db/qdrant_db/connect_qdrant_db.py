from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue, UpdateResult, ScoredPoint
from qdrant_client.http import models as qdrant_models
from core.configurations import Configurations


class QdrantDataBase:
    def __init__(self):
        self.config = Configurations()
        self.client = self.connect_qdrant_db()
    
    def connect_qdrant_db(self) -> QdrantClient:
        """
        Establishes a connection to the Qdrant database.
        """
        return QdrantClient(host=self.config.QDRANT_HOST, port=self.config.QDRANT_PORT)
    
    def recreate_collection(self, coll_name: str, vector_size: int = 1536, distance: str = "Cosine"):
        """
        Recreates a collection with the specified name and vector configuration.
        """
        if not self.client.collection_exists(coll_name):
            self.client.recreate_collection(
                collection_name=coll_name,
                vectors_config={
                    "text_vector": qdrant_models.VectorParams(size=vector_size, distance=distance)
                }
            )

    def upsert_points(self, coll_name: str, points: List[PointStruct]) -> qdrant_models.UpdateResult:
        """
        Upserts (inserts or updates) points into the specified collection.
        """
        result = self.client.upsert(collection_name=coll_name, points=points)
        return result

    