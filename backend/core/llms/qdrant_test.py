from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, ScoredPoint
from typing import List, Any, Tuple
from openai import OpenAI
from pydantic import BaseModel
import tiktoken
import ast
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class QueryResult:
    query: str
    response: str
    tags: List[str]
    document_ids: List[str]
    processing_time: float

OPENAI_API_KEY = 'abc'
QDRANT_HOST = "http://localhost"
QDRANT_PORT = 6333
QDRANT_SECTIONS_COLLECTION = "sections"
QUERY_VECTOR_NAME = "text_vector"

# Initialize OpenAI Client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Utility Classes
class QdrantSectionResponse(BaseModel):
    section: str
    score: float


class QdrantSectionResponseList(BaseModel):
    sections: List[QdrantSectionResponse]


class BotTagResponse(BaseModel):
    tags: List[str]


class DocumentIdResponse(BaseModel):
    document_id: List[str]


class ListResponse(BaseModel):
    sections: List[str]

# Functions
def initialize_qdrant_client() -> QdrantClient:
    """Initialize the Qdrant client."""
    return QdrantClient(url=f"{QDRANT_HOST}:{QDRANT_PORT}")


def generate_embeddings(text: str) -> List[float]:
    """Generate embeddings using OpenAI's API."""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []


def search_query(
    client: QdrantClient,
    coll_name: str,
    query_vector: List[float],
    top_k: int = 5
) -> List[ScoredPoint]:
    """Search for similar points in the specified collection."""
    try:
        return client.search(
            collection_name=coll_name,
            query_vector=(QUERY_VECTOR_NAME, query_vector),
            with_payload=True,
            limit=top_k
        )
    except Exception as e:
        print(f"Error during search: {e}")
        return []


def _process_search_results(sections: List[ScoredPoint]) -> Tuple[BotTagResponse, QdrantSectionResponseList, DocumentIdResponse]:
    """Process the search results into structured responses."""
    tag_response = BotTagResponse(tags=[])
    section_response = QdrantSectionResponseList(sections=[])
    document_id_response = DocumentIdResponse(document_id=[])

    for sec in sections:
        section_response.sections.append(QdrantSectionResponse(
            section=sec.payload.get("content", ""),
            score=sec.score
        ))
        document_id_response.document_id.append(sec.id)
        tag_response.tags.extend(
            set(sec.payload.get("tags", [])) - set(tag_response.tags)
        )

    return tag_response, section_response, document_id_response


def filter_sections_by_score(
    sections: List[QdrantSectionResponse], min_score: float = 0.1
) -> ListResponse:
    """Filter sections based on a minimum score."""
    filtered_sections = [section.section for section in sections if section.score >= min_score]
    return ListResponse(sections=filtered_sections)


def combine_sentences_to_paragraph(text: str) -> str:
    """Combine sentences into a single paragraph."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return " ".join(lines)


def combine_all_sections(sections: List[str]) -> str:
    """Combine all sections into a single context."""
    context = " ".join(section.strip() for section in sections if section.strip())
    return combine_sentences_to_paragraph(context)


def count_tokens(text: str) -> int:
    """Count tokens in a given text."""
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))


def create_prompt_for_bot(query: str, context: str) -> str:
    """Create a prompt for the OpenAI bot."""
    return (
        f"Context:\n{context}\n\n"
        f"Instruction: Answer the question as truthfully and in as much detail as possible based on the given context. "
        f"If you're unsure of the answer, respond with 'Sorry, I don't know.' Maintain the integrity and conciseness of the context.\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )


def response_from_openai(prompt: str) -> str:
    """Fetch a response from OpenAI."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip() if response.choices else None
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return None

def generate_hyde_prompt_query(query: str):
    prompt = f"""
    Given the following query: {query}

    Generate three distinct and insightful questions using these approaches:

    1. Essence Question:
       Rephrase the query to explore its underlying principles and offer a fresh perspective.
    2. Systems Question:
       Examine the relationships and interdependencies between the key concepts in the query.
    3. Application Question:
       Focus on real-world implementations, challenges, or actionable insights related to the query.

    Each question must be directly related to the original query. 
    Return only the three questions, formatted as a Python list of strings with no additional commentary.

    Example Output:
    ["<Essence Question>", "<Systems Question>", "<Application Question>"]
    """
    return prompt





def process_single_query(query: str, client) -> QueryResult:
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

def process_queries_parallel(query_list: List[str], max_workers: int = 4) -> List[QueryResult]:
    # Initialize client once to be shared across threads
    client = initialize_qdrant_client()
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
    
    return sorted(results, key=lambda x: query_list.index(x.query))

# Example Workflow
if __name__ == "__main__":
    query = "What is AI?"
    query_list = []
    prompt = generate_hyde_prompt_query(query=query)
    response = response_from_openai(prompt)  # Response is a string
    # print(response)
    # print(type(response))  # Shows <class 'str'>

    # Convert string response to a list
    query_list = ast.literal_eval(response)  # Safe conversion
    query_list.insert(0, query) 
    
    
    
    # Process queries in parallel
    results = process_queries_parallel(query_list)
    
    # Print final summary
    print("\nFinal Summary:")
    print(f"Total queries processed: {len(results)}")
    total_time = sum(r.processing_time for r in results)
    print(f"Total processing time: {total_time:.2f} seconds")
    # print(query_list)
    # print(type(query_list))  # Now should be <class 'list'>
    
    # client = initialize_qdrant_client()
    # for que in query_list:
    #     que = str(que)
    #     print("Query : " ,que)
    #     query_vector = generate_embeddings(que)

    #     sections = search_query(client, QDRANT_SECTIONS_COLLECTION, query_vector)
    #     tag_response, section_response, document_id_response = _process_search_results(sections)

    #     filtered_sections = filter_sections_by_score(section_response.sections)
    #     context = combine_all_sections(filtered_sections.sections)
    #     prompt = create_prompt_for_bot(que, context)
    #     response = response_from_openai(prompt)
    #     print("Response : ",response)
    #     print("Tags:", tag_response.tags)
    #     print("Document Ids: ", document_id_response)

        
    #     print("\n\nNext Query\n\n")
