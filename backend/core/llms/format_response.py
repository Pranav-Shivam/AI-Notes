import subprocess
import re
from typing import List, Union, Dict, Optional
from dataclasses import dataclass
import re
import time
import tiktoken
from concurrent.futures import ThreadPoolExecutor, as_completed

# # Given sections
# sections = ['Section 1: Narrow AI: Specialized in performing a specific task (e.g., facial recognition, virtual assistants). General AI: Hypothetical AI with the ability to understand and learn any intellectual task that humans can perform. Superintelligent AI: AI that surpasses human intelligence and capabilities (still theoretical).',
# 'Section 2: In 1956, at a scientific conference at \nDartmouth University, American computer \nscientist, John McCarthy, first coined \nthe term “Artificial Intelligence”. During \nthis conference, the audience reached a \nconsensus that AI referred to the creation of \nmachines with intelligence similar to that of \nhumans. AI development can be broadly categorized \ninto three stages: ANI, AGI, and ASI. Artificial \nNarrow Intelligence (ANI), also known as \nweak AI, refers to the development of \ncomputer systems that are designed to \nperform a specific task or solve a particular \nproblem. Artificial General Intelligence (AGI), \n - 2 - \nA happy-suprised reaction by John Maccarthy (the founder of \nAI), when he found out about AI for the first time. Assume that \nthis was 1956 --v 5 --q 2 --s 750\nA person scouting a book that is made out of AI --v 5 --q 2 --s \n750 -\nalso known as strong AI or human-level \nAI, refers to the development of computer \nsystems that can perform any intellectual \ntask that a human can. Artificial Super \nIntelligence (ASI) refers to the development \nof computer systems that surpass human \nintelligence and can perform intellectual \ntasks that exceed human capacity. There are various Artificial Intelligence \ntechnologies that are used in our daily \nlives. Some examples include “smart \nwriting” features that offer suggestions \nfor email composition, spam message \nclassifiers, and voice assistant applications \nlike Amazon’s Alexa or Microsoft’s Cortana, \nwhich utilize natural language processing. Artificial intelligence applications possess \nthe capability to continuously learn from \nnew experiences and make deductions \nbased on past experiences gathered from \ndata. In so-doing, the machine is taught \nhow to execute specific tasks based on the \nknowledge it has acquired from such data. What is Artificial \nIntelligence? AI-generated image showing the reaction \nof John McCarthy’s (founder of AI) when he \ndiscovered Artificial Intelligence for the first time \nin 1956. The image was created on Midjourney. You can copy the text below to get a similar result. AI Image of a person exploring a book made \nwith Artificial Intelligence. The image was created \non Midjourney. You can copy the text below to get a similar result.',
# 'Section 3: AI will likely automate certain jobs, especially repetitive and routine tasks. However, it will also create new opportunities in fields like AI development, data analysis, and ethical governance. Human-centric roles requiring emotional intelligence are less likely to be replaced.',
# 'Section 4: These expectations are underpinned by the \nsignificant demand for these technologies, \nwhich has culminated in an unparalleled \ntransformation in the field of Artificial \nIntelligence. According to many global studies, Artificial \nIntelligence will change the shape of the \nworld in the coming years. We have seen \nArtificial Intelligence play a significant \nrole in shaping how humans interact with \nmodern technologies and machines, and we \ncan use it as a driver of future diverse and \nflexible innovations that keep up with rapid \ncultural and technological transformations \nand open up new horizons for innovation. In line with the wise leadership’s directives \nto ensure future readiness, the United Arab \nEmirates is keen to keep abreast of the \nemerging technologies,  with the aim of \nresearching the most effective means of \nleveraging generative Artificial Intelligence \nin diverse fields such as education, \nhealthcare, media, advanced sciences, and \nmore. ChatGPT’s emergence has attracted \na remarkable turnout, with 100 million users \nfrom November 2022 to January 2023, and \nover one million users in the first five days. In response to these developments, the UAE \ngovernment issued the ‘Generative Artificial \nIntelligence Guide,’ which aims to address \nthe challenges and opportunities presented \nby this technology. The guide examines \nvarious prompt models that can be used \nto obtain optimal and efficient Artificial \nIntelligence responses, as well as data \nprivacy protection in the context of these \ndigital advancements. The ‘Generative Artificial Intelligence Guide’ \nalso highlights the vast capabilities of \ngenerative Artificial Intelligence and its \npotential to significantly improve business \nproductivity and quality of life, as well as \nvarious other recommendations on how to \nharness these innovative technologies to \novercome present and future challenges \nacross all sectors and service fields. Breakthrough Technology and \nPromising Prospects\nHis Excellency Omar Sultan Al Olama\nMinister of State for Artificial Intelligence,  \nDigital Economy and Remote Work Applications\nAccording to the OECD, Artificial \nIntelligence (AI) refers to a machine-based \nsystem that can, for a given set of human \ndefined objectives, make predictions, \nrecommendations, or decisions influencing \nreal or virtual environemnts. Since its inception, Artificial Intelligence \nhas undergone numerous developments.']


def count_tokens(text):
    # Initialize tiktoken encoder (use the encoder for your chosen model, e.g., GPT-3.5)
    encoder = tiktoken.get_encoding("cl100k_base")
    """Return the number of tokens in the provided text using tiktoken."""
    return len(encoder.encode(text))


# constrained_prompt = f"""IMPORTANT INSTRUCTIONS:
# - Do NOT reorganize or move any content between sections
# - Do NOT add any new information or interpretations
# - Do NOT change section titles or numbers
# - Do NOT combine or split paragraphs
# - Do NOT add formatting or markup
# - Only improve clarity of existing sentences while keeping their meaning exactly the same
# - Preserve all technical terms and proper names exactly as they appear
# - Keep all content in its original section

# Text to refine:

# {prompt}"""


@dataclass
class ModelConfig:
    """Configuration for the AI model."""
    name: str
    timeout: int = 60
    temperature: float = 0.3

class TextProcessor:
    """Processes text into a cohesive, accurate document."""
    
    def __init__(self):
        self.model_config = ModelConfig(
                                name="llama3.2:3b",
                                temperature=0.3)

    def clean_text(self, text: str) -> str:
        """Clean text while preserving important content."""
        # Remove technical artifacts and normalize spacing
        text = re.sub(r'--v\s+\d+\s+--q\s+\d+\s+--s\s+\d+', '', text)
        text = re.sub(r'-\s*\d+\s*-', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def merge_sections(self, sections: List[Union[str, List]]) -> str:
        """Merge all sections into a single coherent text."""
        merged_content = []
        
        for section in sections:
            if isinstance(section, list) and len(section) >= 2:
                content = section[1]
            else:
                content = str(section)
            
            cleaned = self.clean_text(content)
            if cleaned:
                merged_content.append(cleaned)
        
        text:str = ' '.join(merged_content)
        print("Orginal text ", text)
        print("Token Count of Original text: ", count_tokens(text))
        return text
    
    def section_text_prompt():
        prompt = f"""Merge and refine the following text into a single cohesive document. 
Maintain complete accuracy while improving clarity and removing redundancy.
Do NOT add any new information or interpretations, formatting or markup
Do Not divide them into sections merge them into one
Only improve clarity of existing sentences while keeping their meaning exactly the same
Preserve all technical terms and proper names exactly as they appear
Preserve all key information, technical terms, and proper names.

Text to process:

"""
        return prompt

    def run_model(self, text: str, query: str, prompt: str) -> Optional[str]:
        """Process text through the AI model."""
        query_prompt = query + prompt + text
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_config.name],
                input=prompt,
                text=True,
                capture_output=True,
                encoding="utf-8",
                timeout=self.model_config.timeout
            )
            
            response = result.stdout.strip()
            # Remove any meta-commentary
            response = re.sub(r'^(Here is|This is|The following is).*?\n', '', response)
            response = re.sub(r'\n(Note:|PS:).*$', '', response)
            
            return response
            
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return None

    def process_document(self, sections: List[Union[str, List]]) -> Dict:
        """Process sections into a single refined document."""
        # Merge all sections
        merged_text = self.merge_sections(sections)
        query = ""
        prompt = ""
        
        # Get model response
        response = self.run_model(merged_text, query, prompt)
        
        return {
            "success": bool(response),
            "refined_text": response,
            "original_text": merged_text
        }

    def generate_response(self, sections):
        result = self.process_document(sections)
        
        # Output result
        if result["success"]:
            text_response:str = result["refined_text"]
            return text_response
        else:
            return "\nProcessing failed"
    
    def process_single_query(query: str, client, context) -> QueryResult:
        start_time = time.time()
        
        # Convert query to string and generate embeddings
        query = str(query)
        query_vector = generate_embeddings(query)
        
        # Search and process results
        sections = search_query(client, QDRANT_SECTIONS_COLLECTION, query_vector)
        tag_response, section_response, document_id_response = _process_search_results(sections)
        
        # Filter and combine sections
        filtered_sections = filter_sections_by_score(section_response.sections)
        context = combine_all_sections(filtered_sections.sections)
        
        # Generate response
        prompt = create_prompt_for_bot(query, context)
        response = response_from_openai(prompt)
        
        processing_time = time.time() - start_time
        
        return QueryResult(
            query=query,
            response=response,
            tags=tag_response.tags,
            document_ids=document_id_response,
            processing_time=processing_time
        )
    
    def process_queries_parallel(self, query_list: List[str], client,max_workers: int = 4) -> List[QueryResult]:
        # Initialize client once to be shared across threads
        results = []
        
        # Using ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all queries to the executor
            future_to_query = {
                executor.submit(process_single_query, query, client): query 
                for query in query_list
            }
            
            # Process completed futures as they finish
            for future in as_completed(future_to_query):
                try:
                    result = future.result()
                    results.append(result)
                    
                    # Print results as they come in
                    print(f"\nResults for query: {result.query}")
                    print(f"Response: {result.response}")
                    print(f"Tags: {result.tags}")
                    print(f"Document IDs: {result.document_ids}")
                    print(f"Processing time: {result.processing_time:.2f} seconds")
                    print("-" * 50)
                    
                except Exception as e:
                    query = future_to_query[future]
                    print(f"Query '{query}' generated an exception: {e}")