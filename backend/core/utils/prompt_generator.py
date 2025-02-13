from typing import List

class PromptGenerator:
    def create_prompt_for_bot(self, query: str, sections: str) -> str:
        return (
            f"Context:\n{sections}\n\n"
            f"Instruction: Answer the question as truthfully and in as much detail as possible based on the given context. "
            f"If you're unsure of the answer, respond with 'Sorry, I don't know.' Maintain the integrity and conciseness of the context.\n\n"
            f"Question: {query}\n"
            f"Answer:"
        )
    
    def generate_hyde_prompt_query(self, query: str):
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

