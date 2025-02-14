import asyncio
import time
import hashlib
import openai
from qdrant_client import QdrantClient
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
        
    
    

class BotService:
    def __init__(self):
        self.qdrant_client = QdrantClient(url="http://localhost:6333")
        self.cache = {}
        self.conversation_history = []
        self.max_memory_size = 5

    async def generate_embedding(self, text: str) -> List[float]:
        cache_key = hashlib.sha256(text.encode()).hexdigest()
        if cache_key in self.cache:
            return self.cache[cache_key]
        response = await openai.Embedding.acreate(input=text, model="text-embedding-ada-002")
        embedding = response['data'][0]['embedding']
        self.cache[cache_key] = embedding
        return embedding

    async def retrieve_relevant_sections(self, query_embedding: List[float], top_k: int = 3) -> List[str]:
        results = self.qdrant_client.search(
            collection_name="your_collection",
            query_vector=query_embedding,
            limit=top_k
        )
        return [hit.payload.get("text", "") for hit in results if "text" in hit.payload]

    async def call_small_llm(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    async def rewrite_followup_query(self, followup_question: str) -> str:
        return await self.call_small_llm(f"Rewrite this question clearly: {followup_question}")

    async def summarize_conversation_history(self):
        if len(self.conversation_history) > self.max_memory_size:
            history_text = "\n".join(
                [f"Q: {qa['query']}\nA: {qa['response']}" for qa in self.conversation_history]
            )
            summary = await self.call_small_llm(f"Summarize: {history_text}")
            embedding = await self.generate_embedding(summary)
            self.qdrant_client.upsert(
                collection_name="conversation_summaries",
                points=[{"vector": embedding, "payload": {"summary": summary}}]
            )
            self.conversation_history = [{"query": "Summary", "response": summary}]

    def assemble_prompt(self, followup_question: str, context_sections: List[str]) -> str:
        history = "\n".join([f"Q: {qa['query']}\nA: {qa['response']}" for qa in self.conversation_history])
        context = "\n".join(context_sections)
        return f"Conversation History:\n{history}\n\nContext:\n{context}\n\nFollow-Up: {followup_question}\nAnswer:"

    async def call_gpt4(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4", messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    async def validate_response(self, generated_answer: str) -> bool:
        embedding = await self.generate_embedding(generated_answer)
        retrieved_context = await self.retrieve_relevant_sections(embedding)
        context_text = " ".join(retrieved_context).lower()
        return any(len(word) > 3 and word.lower() in context_text for word in generated_answer.split())

    async def get_follow_up_answer(self, qna_list: List[Dict[str, str]], follow_up_question: str) -> str:
        for qa in qna_list:
            self.conversation_history.append(qa)
        await self.summarize_conversation_history()
        rewritten_query = await self.rewrite_followup_query(follow_up_question)
        followup_embedding = await self.generate_embedding(rewritten_query)
        retrieved_context = await self.retrieve_relevant_sections(followup_embedding)
        prompt = self.assemble_prompt(rewritten_query, retrieved_context)
        response = await self.call_gpt4(prompt)
        self.conversation_history.append({"query": follow_up_question, "response": response})
        return response

    async def benchmark_get_follow_up_answer(self, qna_list: List[Dict[str, str]], follow_up_question: str, threshold: float = 5.0) -> str:
        start_time = time.time()
        response = await self.get_follow_up_answer(qna_list, follow_up_question)
        elapsed = time.time() - start_time
        return response

async def main():
    bot_service = BotService()
    qna_list = [
        {"query": "What is the project timeline?", "response": "The project is scheduled over 6 months."},
        {"query": "What are the main risks?", "response": "Budget overruns and staffing issues are the primary risks."}
    ]
    follow_up_question = "What about the deadline adjustments due to the new budget constraints?"
    response = await bot_service.benchmark_get_follow_up_answer(qna_list, follow_up_question, threshold=5.0)
    print(f"Final Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
