from core.configurations import Configurations
from core.db.couch_db.couch_sections_db import CouchSectionDB
from core.db.couch_db.couch_documents_db import CouchDocumentsDB
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB
from api.bot.request.bot import BotQueryRequest, BotDocumentsQueryRequest, BotRequest
from api.bot.response.bot import BotQueryResponse, BotDocumentsQueryResponse, BotResponse
from typing import List, Dict
from core.db.couch_db.couch_thread_db import CouchThreadDB
from core.utils.enums import *
from core.utils.count_token import CountTokens
from core.utils.current_date_time import CurrentDateTime
from core.llms.open_ai_connector import OpenAIConnector
from core.utils.prompt_generator import PromptGenerator
from core.embeddings.get_embedding import EmbeddingModels
from app.bot.schemas import BotTagResponse, SectionList
from core.db.qdrant_db.qdrant_schemas import QdrantSection, QdrantSectionResponse, QdrantSectionResponseList

class BotService: 
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
    
    def get_answer_from_bot(self, bot: BotQueryRequest) -> BotQueryResponse:
        tag_response, section_response, document_id_response = self.qdrant_sections.search_sections_based_query(query=bot.query)
        combined_sections = self.filter_sections_by_score(section_response.sections)
        combined_all_section: str = self.combine_all_sections(combined_sections.sections)
        # print(combined_all_section)

        # Log token counts
        # total_tokens = self.count_tokens.count_tokens(combined_all_section)
        # print(f"Combined context token count: {total_tokens}")

        prompt = self.generate_prompts_from_query_sections(query=bot.query, sections=combined_all_section)
        open_ai_response = self.call_llm_to_generate_response(prompt=prompt)

        # print([bot.query, open_ai_response, document_id_response.document_ids, tag_response.tags, self.date_time.get_current_time()])
        return BotQueryResponse(
            query=bot.query,
            response=open_ai_response or "No response",
            document_ids=document_id_response.document_ids,
            tags=tag_response.tags,
            date_time=self.date_time.get_current_time()
        )
        
        
    def combine_all_sections(self, sections: List[str], max_total_tokens: int = 8192, reserved_tokens: int = 1500) -> str:

        max_context_tokens = max_total_tokens - reserved_tokens
        context = []
        current_tokens = 0
        # print(sections)
        for section in sections:
            section_tokens = self.count_tokens.count_tokens(section)
            print(["Section X", section, section_tokens])
            if current_tokens + section_tokens > max_context_tokens:
                break
            context.append(section)
            current_tokens += section_tokens
            print("\n\n")
        

        return self.combine_sentences_to_paragraph(" ".join(context))

     
    
    def filter_sections_by_score(self, sections: QdrantSectionResponseList, min_score: float = 0.1) -> SectionList:
        """Filter sections based on a minimum score."""
        filtered_sections = []
        for section in sections:
            # if section.score >= min_score: 
                # Append only the 'sections' attribute 
            filtered_sections.append(section.section) 
        return SectionList(sections=filtered_sections) 
            
    
    def generate_prompts_from_query_sections(self, query: str, sections: str)-> str:
        prompt = self.create_prompt.create_prompt_for_bot(query=query, sections= sections)
        return prompt
    
    
    def call_llm_to_generate_response(self, prompt: str) -> str:
 
        # Calculate total tokens
        # system_message = "You are a helpful assistant."
        # reserved_tokens = 1000  # For completion
        # total_tokens = (
        #     self.count_tokens.count_tokens(system_message)
        #     + self.count_tokens.count_tokens(prompt)
        #     + reserved_tokens
        # )
        # print(total_tokens)
        # print(prompt)

        # if total_tokens > 8192:
        #     print(f"Error: Total tokens ({total_tokens}) exceed the limit of 8192.")
        #     return "Error: Token limit exceeded."

        try:
            response = self.open_ai.response_from_openai(prompt=prompt)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    
    def combine_sentences_to_paragraph(self, text: str) -> str:
        """Combine sentences into a single paragraph."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return " ".join(lines)
    
    def get_follow_up_answer(self, qna_list: List[Dict[str, str]], follow_up_question: str) -> str:
        # Combine Q&A pairs into a context string
        qna_strings = [f"Q: {qa['query']}\nA: {qa['response']}" for qa in qna_list]
        context = self.combine_all_sections(qna_strings, max_total_tokens=8192, reserved_tokens=1500)

        # Generate prompt with follow-up question and context
        prompt = self.generate_prompt_for_follow_up(follow_up_question, context)

        # Call LLM to generate response
        response = self.call_llm_to_generate_response(prompt)

        return response or "No response"

    def generate_prompt_for_follow_up(self, question: str, context: str) -> str:
        # Construct prompt using the context and question
        prompt = f"Context:\n{context}\n\nFollow-up Question: {question}\nAnswer:"
        return prompt
    

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
        self.bot_service = BotService()
        self.tags_response = BotTagResponse(tags = [])
    
    def get_response_from_bot_on_document(self, bot_request: BotDocumentsQueryRequest) -> BotResponse:
        tag_response, section_response, document_id_response = self.retrieve_sections_from_qdrant(bot_request)
        combined_sections = self.bot_service.filter_sections_by_score(section_response.sections)
        combined_all_section: str = self.bot_service.combine_all_sections(combined_sections.sections)

        # # Log token counts
        # total_tokens = self.count_tokens.count_tokens(combined_all_section)
        # print(f"Combined context token count: {total_tokens}")

        prompt = self.bot_service.generate_prompts_from_query_sections(query=bot_request.query, sections=combined_all_section)
        open_ai_response = self.bot_service.call_llm_to_generate_response(prompt=prompt)

        # print([bot_request.query, open_ai_response, document_id_response.document_ids, tag_response.tags, self.date_time.get_current_time()])
        return BotQueryResponse(
            query=bot_request.query,
            response=open_ai_response or "No response",
            document_ids=document_id_response.document_ids,
            tags=tag_response.tags,
            date_time=self.date_time.get_current_time()
        )
    
    def retrieve_sections_from_qdrant(self, bot_request: BotDocumentsQueryRequest):
        return self.qdrant_sections.filter_sections_based_on_document_id(document_id= bot_request.document_id, query= bot_request.query)
    

class BotThreadService:
    
    def __init__(self) -> None:
        self.thread_db = CouchThreadDB()
        self.bot_service = BotService()
        self.qdrant_sections = QdrantSectionDB()
    
    def get_answer_from_thread_bot(bot_request: BotRequest):
        pass
    
    def get_thread_list(self, thread_id:str):
        if thread_id:
            qna_list = self.thread_db.get_query_response_by_thread_id(thread_id=thread_id)
            return qna_list
        else:
            return []
    
    def check_for_thread(self, bot_request: BotRequest):
        if self.thread_db.check_for_thread(thread_id= bot_request.thread_id):
            tag_response, section_response, document_id_response = self.qdrant_sections.search_sections_based_query(query=bot_request.query)
            combined_sections = self.bot_service.filter_sections_by_score(section_response.sections)
            combined_all_section: str = self.bot_service.combine_all_sections(combined_sections.sections)
            qna_list= self.get_thread_list(thread_id= bot_request.thread_id)
            # answer_from_vdb = True
            self.combine_follow_up_context(query= bot_request.query, qna_list= qna_list, context=combined_all_section)
        else:
            bot_req = BotQueryRequest(
                query= bot_request.query
            )
            return self.bot_service.get_answer_from_bot(bot= bot_req)
        
    def combine_follow_up_context(self, query, qna_list, context):
        
        pass
    
    def update_thread_with_new_follow_up(self, qna_list, new_qna):
        pass
    
    
    

class HyDEBotService: 
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
    
    def get_answer_from_bot(self, bot: BotQueryRequest) -> BotQueryResponse:
        tag_response, section_response, document_id_response = self.qdrant_sections.search_sections_based_query(query=bot.query)
        combined_sections = self.filter_sections_by_score(section_response.sections)
        combined_all_section: str = self.combine_all_sections(combined_sections.sections)
        # print(combined_all_section)

        # Log token counts
        # total_tokens = self.count_tokens.count_tokens(combined_all_section)
        # print(f"Combined context token count: {total_tokens}")

        prompt = self.generate_prompts_from_query_sections(query=bot.query, sections=combined_all_section)
        open_ai_response = self.call_llm_to_generate_response(prompt=prompt)

        # print([bot.query, open_ai_response, document_id_response.document_ids, tag_response.tags, self.date_time.get_current_time()])
        return BotQueryResponse(
            query=bot.query,
            response=open_ai_response or "No response",
            document_ids=document_id_response.document_ids,
            tags=tag_response.tags,
            date_time=self.date_time.get_current_time()
        )
        
        
    def combine_all_sections(self, sections: List[str], max_total_tokens: int = 8192, reserved_tokens: int = 1500) -> str:

        max_context_tokens = max_total_tokens - reserved_tokens
        context = []
        current_tokens = 0
        # print(sections)
        for section in sections:
            section_tokens = self.count_tokens.count_tokens(section)
            print(["Section X", section, section_tokens])
            if current_tokens + section_tokens > max_context_tokens:
                break
            context.append(section)
            current_tokens += section_tokens
            print("\n\n")
        

        return self.combine_sentences_to_paragraph(" ".join(context))

     
    
    def filter_sections_by_score(self, sections: QdrantSectionResponseList, min_score: float = 0.1) -> SectionList:
        """Filter sections based on a minimum score."""
        filtered_sections = []
        for section in sections:
            # if section.score >= min_score: 
                # Append only the 'sections' attribute 
            filtered_sections.append(section.section) 
        return SectionList(sections=filtered_sections) 
            
    
    def generate_prompts_from_query_sections(self, query: str, sections: str)-> str:
        prompt = self.create_prompt.create_prompt_for_bot(query=query, sections= sections)
        return prompt
    
    
    def call_llm_to_generate_response(self, prompt: str) -> str:
 
        # Calculate total tokens
        # system_message = "You are a helpful assistant."
        # reserved_tokens = 1000  # For completion
        # total_tokens = (
        #     self.count_tokens.count_tokens(system_message)
        #     + self.count_tokens.count_tokens(prompt)
        #     + reserved_tokens
        # )
        # print(total_tokens)
        # print(prompt)

        # if total_tokens > 8192:
        #     print(f"Error: Total tokens ({total_tokens}) exceed the limit of 8192.")
        #     return "Error: Token limit exceeded."

        try:
            response = self.open_ai.response_from_openai(prompt=prompt)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    
    def combine_sentences_to_paragraph(self, text: str) -> str:
        """Combine sentences into a single paragraph."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return " ".join(lines)
    
    def get_follow_up_answer(self, qna_list: List[Dict[str, str]], follow_up_question: str) -> str:
        # Combine Q&A pairs into a context string
        qna_strings = [f"Q: {qa['query']}\nA: {qa['response']}" for qa in qna_list]
        context = self.combine_all_sections(qna_strings, max_total_tokens=8192, reserved_tokens=1500)

        # Generate prompt with follow-up question and context
        prompt = self.generate_prompt_for_follow_up(follow_up_question, context)

        # Call LLM to generate response
        response = self.call_llm_to_generate_response(prompt)

        return response or "No response"

    def generate_prompt_for_follow_up(self, question: str, context: str) -> str:
        # Construct prompt using the context and question
        prompt = f"Context:\n{context}\n\nFollow-up Question: {question}\nAnswer:"
        return prompt
        
    
    
    