from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from core.configurations import Configurations
from core.db.qdrant_db.connect_qdrant_db import QdrantDataBase
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
from core.db.qdrant_db.qdrant_schemas import QdrantQuestion


class QdrantQuestionDB:
    def __init__(self):
        self.client = QdrantDataBase()
        self.config =Configurations()
        self.collection_name = self.config.QDRANT_QUESTIONS_COLLECTION

    def insert_question(self, question: QdrantQuestion):
        """
        Inserts a new question into the Qdrant collection.
        """
        point = PointStruct(
            id=question.id,
            vector=question.vector,
            payload=question.payload
        )
        self.client.client.upsert(collection_name=self.collection_name, points=[point])

    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a question by its unique identifier.
        """
        response = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[question_id]
        )
        return response[0] if response else None

    def search_questions_by_vector(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for the closest questions based on a vector.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return search_result

    def delete_question(self, question_id: str):
        """
        Deletes a question by its unique identifier.
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={"ids": [question_id]}
        )

    def update_question(self, question: QdrantQuestion):
        """
        Updates an existing question.
        """
        self.insert_question(question)  # Upsert method replaces the existing point

    def filter_questions_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """
        Filters questions by the owner_id field.
        """
        response = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="payload.owner_id",
                        match=MatchValue(value=owner_id)
                    )
                ]
            )
        )
        return response[0] if response else []