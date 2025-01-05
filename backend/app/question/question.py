# Database Field Enums
from core.utils.enums import (
    CouchDBUserFields,
    CouchDBDocumentFields,
    CouchDBTagFields,
    CouchDBSectionFields,
    CouchDBQuestionFields,
    CouchDBThreadFields,
    CouchDBMessageFields,
    QdrantSectionFields,
    QdrantQuestionFields
)
from fastapi import HTTPException
from api.question.response.question import SaveQuestionResponse
from core.configurations import Configurations
from core.embeddings.get_embedding import EmbeddingModels, EmbeddingSchema, EmbeddingSchemaList
from api.question.request.question import QuestionRequest, QuestionAnswerRequest
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB
from core.db.couch_db.couch_question_db import CouchQuestionDB
from core.db.couch_db.couch_tags_db import CouchTagDB
from core.db.couch_db.couch_sections_db import CouchSectionDB
from core.db.couch_db.couch_thread_db import CouchThreadDB
from core.db.qdrant_db.qdrant_questions_db import QdrantQuestionDB
from core.db.couch_db.couch_schemas import CouchQuestionSchema, ThreadMessages, ThreadMessageMetadata, ThreadMetadata, CouchThreadSchema, CouchTagSchema, ThreadMessageList, CouchSectionSchema
from core.db.qdrant_db.qdrant_schemas import QdrantQuestionSchema, QdrantSection, QuestionPayload, SectionMetadata, SectionPayload
from core.utils.current_date_time import CurrentDateTime
from core.generate_unique_id import generate_unique_id, generate_unique_id_from_text
from couchdb.http import ResourceNotFound, ResourceConflict, ServerError
from pydantic import ValidationError 
from typing import List, Optional
from dataclasses import dataclass
from uuid import uuid4

class QuestionService:
    def __init__(self) -> None:
        """Initializes the QuestionService with required databases, models, and configurations."""
        self.couch_question_db = CouchQuestionDB()
        self.qdrant_question_db = QdrantQuestionDB()
        self.qdrant_section_db = QdrantSectionDB()
        self.couch_tag_db = CouchTagDB()
        self.couch_thread_db = CouchThreadDB()
        self.couch_section_db = CouchSectionDB()
        self.qdrant_section_fields = QdrantSectionFields
        self.qdrant_question_fields = QdrantQuestionFields
        self.config = Configurations()
        self.embed_models = EmbeddingModels()
        self.current_date_time = CurrentDateTime().get_current_time()

    def save_query_and_response_db(self, query: QuestionAnswerRequest) -> str:

        try:
            # Extract data from the request
            document_id = query.document_id or ""
            thread_id = query.thread_id or self._generate_unique_id()
            question = query.query
            answer = query.response
            current_user = self.config.USERNAME
            question_id = self._generate_unique_id_from_text(question)
            tags = query.tags

            # Save question and answer in CouchDB
            self._save_question_in_couchdb(question_id, document_id, thread_id, question, answer, current_user, tags)

            # Save question embeddings in Qdrant
            self._save_question_in_qdrant(question_id, document_id, question, answer, tags, current_user)

            # Create and save thread in CouchDB
            self._save_thread_in_couchdb(thread_id, current_user, question, answer, tags)

            # Save tags in CouchDB
            self._save_tags_in_couchdb(tags)

            # Save answer sections in CouchDB and Qdrant
            self.save_answer_in_sections_db(answer, question_id, document_id, tags)

            return SaveQuestionResponse(
                question_id=question_id,
                status_code=200,
                message="Question and response saved successfully",
                query=question,
                response=answer,
                tags=tags
            )

        except (ResourceNotFound, ResourceConflict, ServerError) as e:
            return SaveQuestionResponse(
                question_id=question_id,
                status_code=500,
                message=str(e),
                query=query.query,
                response=query.response,
                tags=query.tags
            )
        except ValidationError as e:
            return SaveQuestionResponse(
                question_id=question_id,
                status_code=400,
                message=str(e),
                query=query.query,
                response=query.response,
                tags=query.tags
            )
        except Exception as e:
            return SaveQuestionResponse(
                question_id=question_id,
                status_code=500,
                message=str(e),
                query=query.query,
                response=query.response,
                tags=query.tags
            )

    def save_answer_in_sections_db(self, answer: str, question_id: str, document_id: str, tags: List[str]) -> None:

        try:
            sections: EmbeddingSchemaList = self.embed_models.generate_chunks_with_embeddings(text=answer)

            for section_data in sections.chunks:
                section_id = self._generate_unique_id()
                self._save_section_in_couchdb(section_id, question_id, document_id, section_data, tags, self.current_date_time, self.config.USERNAME)
                self._save_section_in_qdrant(section_id, question_id, document_id, section_data, tags, self.config.USERNAME)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save answer sections: {str(e)}")

    def _parse_tags(self, tags_str: str) -> List[str]:

        try:
            return [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid tags format: {str(e)}")

    def _save_question_in_couchdb(self, question_id: str, document_id: str, thread_id: str, question: str, answer: str, user: str, tags: List[str]) -> None:
        """Saves the question and answer in CouchDB."""
        question_data = CouchQuestionSchema(
            id=question_id,
            document_id=document_id,
            thread_id=thread_id,
            date_time=self.current_date_time,
            question=question,
            answer=answer,
            created_by=user,
            updated_by=user,
            tags=tags
        )
        self.couch_question_db.insert_question(question_data)

    def _save_question_in_qdrant(self, question_id: str, document_id: str, question: str, answer: str, tags: List[str], user: str) -> None:
        """Saves the question embeddings in Qdrant."""
        try:
            embeddings = self.embed_models.generate_chunks_with_embeddings(answer)
            
            for em in embeddings.chunks:
                quest_embed = em.embeddings
                
            payload = QuestionPayload(
                document_id=document_id,
                question=question,
                answer=answer,
                tags=tags,
                embeddings_version=self.config.OPENAI_EMBEDDING_MODEL,
                owner_id=user
            )
            
            question_data = QdrantQuestionSchema(
                id=question_id,
                vector={self.config.QUERY_VECTOR_NAME: quest_embed},
                payload=payload.dict()
            )
            self.qdrant_question_db.insert_question(question_data)
        except Exception as e:
            print("ERROR: ", str(e))
            raise Exception(f"Failed to save question in Qdrant: {str(e)}")

    def _save_thread_in_couchdb(self, thread_id: str, user: str, question: str, answer: str, tags: List[str]) -> None:
        """Saves the thread in CouchDB."""
        thread_data = CouchThreadSchema(
            id=thread_id,
            user_id=user,
            created_at=self.current_date_time,
            updated_at=self.current_date_time,
            title=question,
            status="active",
            tags=tags,
            messages=ThreadMessageList(
            message=[ThreadMessages(  # Changed from positional to keyword argument
                message_id=self._generate_unique_id(),
                timestamp=self.current_date_time,
                sender="user",
                query=question,
                response=answer
            )]
        )
        )
        self.couch_thread_db.create_threads(thread_data)

    def _save_tags_in_couchdb(self, tags: List[str]) -> None:
        """Saves tags in CouchDB."""
        for tag in tags:
            tag_data = CouchTagSchema(
                id=self._generate_unique_id_from_text(tag),
                tag=tag
            )
            self.couch_tag_db.create_tag(tag_data)

    def _save_section_in_couchdb(self, section_id: str, question_id: str, document_id: str, section_data: EmbeddingSchema, tags: List[str], date_time: str, user: str) -> None:
        """Saves a section in CouchDB."""
        section_couch_data = CouchSectionSchema(
            id=section_id,
            question_id=question_id,
            document_id=document_id,
            date_time=date_time,
            section=section_data.section_chunk,
            token_count=section_data.token_size,
            tags=tags,
            embeddings_version="Current_version",
            owner_id=user
        )
        self.couch_section_db.create_section(section_couch_data)

    def _save_section_in_qdrant(self, section_id: str, question_id: str, document_id: str, section_data: EmbeddingSchema, tags: List[str], user: str) -> None:
        """Saves a section's embeddings in Qdrant."""
        try:
            payload = SectionPayload(
                document_id=document_id,
                question_id=question_id,
                content=section_data.section_chunk,
                token_count=section_data.token_size,
                tags=tags,
                embeddings_version=self.config.OPENAI_EMBEDDING_MODEL,
                owner_id=user,
                metadata=SectionMetadata(additional_info=None)
            )

            section_qdrant_data = QdrantSection(
                id=section_id,
                vector={self.config.QUERY_VECTOR_NAME: section_data.embeddings},
                payload=payload.dict()
            )
            self.qdrant_section_db.insert_section(section_qdrant_data)
        except Exception as e:
            print("ERROR: ", str(e))
            raise Exception(f"Failed to save section in Qdrant: {str(e)}")

    def _generate_unique_id(self) -> str:
        """Generates a unique ID using UUID."""
        return generate_unique_id()

    def _generate_unique_id_from_text(self, text: str) -> str:
        """Generates a unique ID from text."""
        return generate_unique_id_from_text(text)
   
    
    
    