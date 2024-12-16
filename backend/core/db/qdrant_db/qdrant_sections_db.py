from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from core.configurations import Configurations
from core.db.qdrant_db.connect_qdrant_db import QdrantDataBase
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
from core.db.qdrant_db.qdrant_schemas import QdrantSection


class QdrantSectionDB:
    def __init__(self):
        self.client = QdrantDataBase()
        self.config = Configurations()
        
        self.collection_name = self.config.QDRANT_SECTIONS_COLLECTION

    def insert_section(self, section: QdrantSection):
        """
        Inserts a new section into the Qdrant collection.
        """
        # Recreate collection
        self.client.recreate_collection(coll_name=self.collection_name)
        point = PointStruct(
            id=section.id,
            vector=section.vector,
            payload=section.payload
        )
        self.client.upsert_points(coll_name=self.collection_name, points=[point])

    