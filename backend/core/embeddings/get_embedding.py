import numpy as np
from core.configurations import Configurations
from core.embeddings.schemas import EmbeddingSchema, EmbeddingSchemaList
from core.open_ai.open_ai_connector import OpenAIConnector
from core.utils.count_token import CountTokens
import openai
import tiktoken
import re
from typing import List, Dict

class EmbeddingModels:
    def __init__(self):
        self.client = OpenAIConnector().client
        self.config = Configurations()
        self.token_size = self.config.TOKEN_SIZE
        self.count_token = CountTokens()
        self.model = self.config.OPENAI_EMBEDDING_MODEL

    def create_embeddings(self, text_chunks):
        embeddings = []
        for chunk in text_chunks:
            response = self.client.embeddings.create(
                input=chunk,
                model="contriever"
            )
            embeddings.append(np.array(response.data[0].embedding))
        return embeddings
    
    def generate_embeddings(self, text):
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            # Extract the embeddings
            embeddings = response.data[0].embedding
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None
    
    def generate_chunks_with_embeddings(self, text: str) -> EmbeddingSchemaList:
        """
        Chunk the text into smaller parts considering token limits, while avoiding sentence splits.
        Each chunk includes the token size, the section, and its embeddings.
        """
        
        # Split the text into sentences based on punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)  
        
        # Initialize variables
        chunks = []
        current_chunk = ""
        chunks_with_embeddings = []

        # Loop through each sentence to build chunks
        for sentence in sentences:
            sentence = sentence.strip()
            # Check if adding the sentence to the current chunk exceeds the token limit
            if self.count_token.count_tokens(current_chunk + " " + sentence) > self.token_size:
                if current_chunk:
                    chunks_with_embeddings.append(EmbeddingSchema(
                        token_size= self.count_token.count_tokens(current_chunk),
                        section_chunk= current_chunk,
                        embeddings= self.generate_embeddings(current_chunk)
                    ))
                    chunks.append(current_chunk)
                
                # Start a new chunk with the current sentence
                current_chunk = sentence
            else:
                # Add the sentence to the current chunk
                current_chunk += " " + sentence if current_chunk else sentence

        # Handle the final chunk
        if current_chunk:
            chunks_with_embeddings.append(EmbeddingSchema(
                        token_size= self.count_token.count_tokens(current_chunk),
                        section_chunk= current_chunk,
                        embeddings= self.generate_embeddings(current_chunk)
                    ))
            chunks.append(current_chunk)

        return EmbeddingSchemaList(chunks=chunks_with_embeddings)
    
