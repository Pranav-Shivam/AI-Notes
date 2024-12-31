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

