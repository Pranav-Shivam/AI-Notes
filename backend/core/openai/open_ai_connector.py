from openai import OpenAI
from core.configurations import Configurations
class OpenAIConnector:
    def __init__(self):
        self.client = OpenAI(api_key=Configurations.OPENAI_API_KEY)
