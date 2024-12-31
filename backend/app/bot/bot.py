from core.configurations import Configurations
from core.db.couch_db.couch_sections_db import CouchSectionDB
from core.db.couch_db.couch_documents_db import CouchDocumentsDB
from core.db.qdrant_db.qdrant_sections_db import QdrantSectionDB
from api.bot.request.bot import BotQueryRequest, BotDocumentsQueryRequest
from api.bot.response.bot import BotQueryResponse, BotDocumentsQueryResponse
from typing import List
from core.utils.count_token import CountTokens
from core.utils.current_date_time import CurrentDateTime
from core.open_ai.open_ai_connector import OpenAIConnector
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

        for section in sections:
            section_tokens = self.count_tokens.count_tokens(section)
            if current_tokens + section_tokens > max_context_tokens:
                break
            context.append(section)
            current_tokens += section_tokens
        
        

        return self.combine_sentences_to_paragraph(" ".join(context))

     
    
    def filter_sections_by_score(self, sections: QdrantSectionResponseList, min_score: float = 0.74) -> SectionList:
        """Filter sections based on a minimum score."""
        filtered_sections = []
        for section in sections:
            if section.score >= min_score: 
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
    
class DcoumentBotService:
    pass
class DocumentBotThreadService:
    pass
class BotThreadService:
    pass
        
        