# Standard Library Imports
from typing import List, Optional, Tuple
from fastapi import HTTPException

# Database Imports
from core.db.couch_db.couch_sections_db import CouchSectionDB
from core.db.couch_db.couch_documents_db import CouchDocumentsDB
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB

# API Request/Response Models
from api.bot.request.bot import BotRequest, BotDocumentsQueryRequest
from api.bot.response.bot import BotResponse, BotDocumentsQueryResponse

# Schema Models
from app.bot.schemas import BotTagResponse, SectionList, DocumentIdResponse
from core.db.qdrant_db.qdrant_schemas import (
    QdrantSection, 
    QdrantSectionResponse, 
    QdrantSectionResponseList
)

# Core Utilities
from core.configurations import Configurations
from core.utils.count_token import CountTokens
from core.utils.current_date_time import CurrentDateTime
from core.utils.prompt_generator import PromptGenerator

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

# Management and Configuration Enums
from core.utils.enums import (
    SearchManagements,
    TokenManagements,
    MemoryManagement,
    SystemConfigurations,
    BotStrategy
)

# File Related Enums
from core.utils.enums import (
    FileTypes,
    FileExtensions
)

# HTTP Status Enums
from core.utils.enums import (
    HTTPStatus,
    HTTPStatusCode
)

# AI/ML Related
from core.open_ai.open_ai_connector import OpenAIConnector
from core.embeddings.get_embedding import EmbeddingModels

class BotService:
    def __init__(self):
        self.strategies = {
            BotStrategy.NORMAL: NormalBotService(),
            BotStrategy.DOCUMENT: DocumentBotService(),
            BotStrategy.DOCUMENT_THREAD: DocumentThreadBotService(),
            BotStrategy.DOCUMENT_THREAD: BotThreadService()
        }

    def get_answer_from_bot(self, bot_request: BotRequest) -> BotResponse:
        
        if bot_request.document_id and bot_request.thread_id:
            service = BotStrategy.DOCUMENT_THREAD
        elif bot_request.document_id:
            service = BotStrategy.DOCUMENT
        elif bot_request.thread_id:
            service = BotStrategy.THREAD
        else:
            service = BotStrategy.NORMAL

        response = service.get_response(bot_request.query, bot_request.document_id, bot_request.thread_id, bot_request.tags)

        return response

class NormalBotService:
    def get_response(self, bot_request: BotRequest) -> BotResponse:
        sections = BotHelper().retrieve_sections(bot_request.query)
        filtered_sections = BotHelper().filter_sections(sections)
        combined_context = BotHelper().combine_sections(filtered_sections)
        prompt = BotHelper().generate_prompt(bot_request.query, combined_context)
        response = BotHelper().call_llm(prompt)
        return BotHelper().format_response(response)
    

class DocumentBotService:
    
    def __init__(self):
        self.config = Configurations()
        self.couch_sections = CouchSectionDB()
        self.couch_documents = CouchDocumentsDB()
        self.qdrant_sections = QdrantSectionDB()
        self.embedding_models = EmbeddingModels()
        self.create_prompt = PromptGenerator()
        self.open_ai = OpenAIConnector()
        self.date_time = CurrentDateTime()
        self.count_tokens = CountTokens()
        self.sections_utils = QdrantSectionFields
        self.tags_response = BotTagResponse(tags = [])
    
    def get_response(self, bot_request: BotRequest) -> BotResponse:
        sections = BotHelper().retrieve_sections(query= bot_request.query, document_id= bot_request.document_id)
        filtered_sections = BotHelper().filter_sections(sections)
        combined_context = BotHelper().combine_sections(filtered_sections)
        prompt = BotHelper().generate_prompt(bot_request.query, combined_context)
        response = BotHelper().call_llm(prompt)
        return BotHelper().format_response(response)
    
    def _retrieve_sections_from_qdrant(self, bot_request: BotRequest):
        tag_response, section_response, document_id_response = self.qdrant_sections.filter_sections_based_on_document_id(document_id= bot_request.document_id, query= bot_request.query)
    
class DocumentThreadBotService:
    def get_response(self, query: str, document_id: str, thread_id: str) -> BotResponse:
        sections = BotHelper().retrieve_sections(query, document_id=document_id, thread_id=thread_id)
        filtered_sections = BotHelper().filter_sections(sections)
        combined_context = BotHelper().combine_sections(filtered_sections)
        prompt = BotHelper().generate_prompt(query, combined_context)
        response = BotHelper().call_llm(prompt)
        return BotHelper().format_response(response)
    
class BotThreadService:
    def get_response(self, query: str, thread_id: str) -> BotResponse:
        sections = BotHelper().retrieve_sections(query, thread_id=thread_id)
        filtered_sections = BotHelper().filter_sections(sections)
        combined_context = BotHelper().combine_sections(filtered_sections)
        prompt = BotHelper().generate_prompt(query, combined_context)
        response = BotHelper().call_llm(prompt)
        return BotHelper().format_response(response)

class BotHelper:
    def __init__(self):
        self.config = Configurations()
        self.couch_sections = CouchSectionDB()
        self.couch_documents = CouchDocumentsDB()
        self.qdrant_sections = QdrantSectionDB()
        self.embedding_models = EmbeddingModels()
        self.create_prompt = PromptGenerator()
        self.open_ai = OpenAIConnector()
        self.date_time = CurrentDateTime()
        self.count_tokens = CountTokens()
        self.tags_response = BotTagResponse(tags = [])
        
    def filter_sections_by_score(self, sections: QdrantSectionResponseList, min_score: float = 0.74) -> SectionList:
        """Filter sections based on a minimum score."""
        filtered_sections = []
        for section in sections:
            if section.score >= min_score: 
                # Append only the 'sections' attribute 
                filtered_sections.append(section.section) 
        return SectionList(sections=filtered_sections) 

    def combine_sections(self, sections, max_tokens=TokenManagements.MAX_TOTAL_TOKENS, reserved_tokens=TokenManagements.RESERVED_TOKENS):
        # Combine sections into a single context string while respecting token limits
        pass

    def generate_prompt(self, query, context):
        # Generate the prompt to be sent to the LLM
        pass

    def call_llm(self, prompt):
        # Call the LLM and return the response
        pass

    def format_response(self, response):
        # Format the LLM response for the user
        pass

    def retrieve_sections(self, bot_request: BotRequest):
        sections = self._retrive_sections_from_qdrant(bot_request= bot_request)
    
    def _retrieve_sections_from_qdrant(self, bot_request: BotRequest) -> Tuple[Optional[BotTagResponse], Optional[QdrantSectionResponseList], Optional[DocumentIdResponse]]:
        if not bot_request.query:
            raise HTTPException(status_code=400, detail="Query is missing in the bot request.")

        try:
            # Define conditions
            has_document_id = bool(bot_request.document_id)
            has_thread_id = bool(bot_request.thread_id)
            has_tags = len(bot_request.tags) > 0

            # Determine the appropriate case and fetch data
            if has_document_id and has_thread_id and has_tags:
                return self.qdrant_sections.filter_by_document_thread_tags(
                    document_id=bot_request.document_id,
                    thread_id=bot_request.thread_id,
                    tags=bot_request.tags
                )
            elif has_document_id and has_thread_id:
                return self.qdrant_sections.filter_by_document_and_thread(
                    document_id=bot_request.document_id,
                    thread_id=bot_request.thread_id
                )
            elif has_thread_id:
                return self.qdrant_sections.filter_by_thread_id(
                    thread_id=bot_request.thread_id
                )
            elif has_document_id:
                return self.qdrant_sections.filter_by_document_id(
                    document_id=bot_request.document_id
                )
            else:
                return self.qdrant_sections.search_sections_based_query(
                    query=bot_request.query
                )

        except Exception as e:
            # Raise HTTPException for any unexpected errors
            raise HTTPException(status_code=500, detail=f"Failed to retrieve sections from Qdrant: {str(e)}")

