from uuid import uuid4
import hashlib

def generate_unique_id():
    # Generate a UUID4 (random UUID)
    return str(uuid4())

def generate_unique_id_from_text(text: str) -> str:
    """
    Generate a consistent unique document ID based on text content.
    
    Args:
        text (str): Input text to generate unique ID from
    
    Returns:
        str: Unique identifier generated from text content
    """
    # Use MD5 hash to generate a consistent ID from text
    content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return content_hash