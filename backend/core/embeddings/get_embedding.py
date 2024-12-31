import numpy as np
from core.configurations import Configurations
from core.open_ai.open_ai_connector import OpenAIConnector
import openai

class EmbeddingModels:
    def __init__(self):
        self.client = OpenAIConnector().client
        self.config = Configurations()
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
