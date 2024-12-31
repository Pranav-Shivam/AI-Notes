from openai import OpenAI
from core.configurations import Configurations
class OpenAIConnector:
    def __init__(self):
        self.client = OpenAI(api_key=Configurations.OPENAI_API_KEY)
    
    def response_from_openai(self, prompt):
        try:
            response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7 
            )
            return response.choices[0].message.content.strip() if response.choices else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None