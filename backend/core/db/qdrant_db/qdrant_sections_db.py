from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from core.configurations import Configurations
from core.db.qdrant_db.connect_qdrant_db import QdrantDataBase
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue, ScoredPoint
from core.db.qdrant_db.qdrant_schemas import QdrantSection, QdrantSectionResponse, QdrantSectionResponseList
from core.embeddings.get_embedding import EmbeddingModels
from app.bot.schemas import DocumentIdResponse, BotTagResponse


class QdrantSectionDB:
    def __init__(self):
        self.client = QdrantDataBase()
        self.config = Configurations()
        self.embedding_models = EmbeddingModels()
        self.query_vector_name = self.config.QUERY_VECTOR_NAME
        
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
    
    def search_sections_based_query(self, query: str) -> Tuple[BotTagResponse, QdrantSectionResponseList, DocumentIdResponse]:

        query_vector = self.embedding_models.generate_embeddings(query)
        searched_sections = self.client.search_query(
            coll_name=self.collection_name, query_vector=query_vector, query_vector_name=self.query_vector_name
        )

        return self._process_search_results(searched_sections)

    def _process_search_results(self, sections: List[ScoredPoint]) -> Tuple[BotTagResponse, QdrantSectionResponseList, DocumentIdResponse]:

        tag_response = BotTagResponse(tags=[])
        section_response = QdrantSectionResponseList(sections=[])
        document_id_response = DocumentIdResponse(document_ids=[])

        for sec in sections:
            response_result = QdrantSectionResponse(
                section=sec.payload.get("content", ""),
                score=sec.score,
            )
            document_id_response.document_ids.append(sec.id)
            section_response.sections.append(response_result)

            # Collect unique tags efficiently using set operations
            tag_response.tags.extend(set(sec.payload.get("tags", [])) - set(tag_response.tags))

        return tag_response, section_response, document_id_response
    