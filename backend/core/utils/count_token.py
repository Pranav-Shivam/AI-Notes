import tiktoken

class CountTokens:
    def count_tokens(self, text):
        # Initialize tiktoken encoder (use the encoder for your chosen model, e.g., GPT-3.5)
        encoder = tiktoken.get_encoding("cl100k_base")
        """Return the number of tokens in the provided text using tiktoken."""
        return len(encoder.encode(text))