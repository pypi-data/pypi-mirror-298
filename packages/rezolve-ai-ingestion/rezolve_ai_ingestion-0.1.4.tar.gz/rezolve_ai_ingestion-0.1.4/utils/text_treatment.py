import re
import html
import nltk
import numpy as np
import warnings
from openai import OpenAI
from datetime import datetime
from typing import List, Dict, Any
from langchain_text_splitters import NLTKTextSplitter
from openai._exceptions import BadRequestError

# Suppress nltk-related warnings if desired
warnings.filterwarnings("ignore", module="nltk")

# Download the NLTK 'punkt' package for sentence tokenization
nltk.download('punkt')

# Initialize text splitter with a chunk size
text_splitter = NLTKTextSplitter(chunk_size=2000)

def split_text(text: str) -> List[str]:
    """
    Split the given text into chunks using NLTKTextSplitter.
    
    Args:
        text (str): The text to be split into chunks.
    
    Returns:
        List[str]: A list of text chunks.
    """
    try:
        # Clean the text: remove excess newlines and join text
        cleaned_text = " ".join([line for line in text.strip().split("\n") if line.strip()])
        chunks = text_splitter.split_text(cleaned_text)
        return chunks
    except Exception as e:
        print(f"Exception during text splitting: {e}")
        return []

def clean_text(data: str) -> str:
    """
    Clean text data by removing comments, tags, entities, file paths, system directories, GUIDs, dates,
    backslashes, slashes, lines starting with dashes, structured content like table of contents, and irrelevant whitespace.
    Additionally, ensure proper separation of sentences.

    Args:
        data (str): Text data to be cleaned.

    Returns:
        str: Cleaned text data.
    """
    # Replace non-breaking spaces with regular spaces
    data = data.replace('\xa0', ' ')

    patterns = {
        'lines_with_dashes': (r'^\s*--.*$', ''),  # Remove lines starting with dashes
        'structured_headers': (r'(?:\w[\w\s]*\.){2,}|(?:\d{1,2}[\.\-]\d{1,2}[\.\-]\d{2,4})|(?:\d+\.)', ''),  # Remove structured table of contents
        'bullet_points': (r'[\u2022\u25AA\u25AB\u25A0\u25B6\u25C0\u25B6\u2713\uf0b7]+', ''),  # Remove bullet points and special characters
        'html_comments': (r'<!--.*?-->', ''),  # Remove HTML comments
        'html_tags': (r'<.*?>', ''),  # Remove HTML tags
        'guids': (r'\b[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\b', ''),  # Remove GUIDs
        'dates': (r'\b(\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[/-]\d{2}[/-]\d{4})\b', ''),  # Remove dates in various formats
        'slashes': (r'[\\/]', ''),  # Remove backslashes and slashes
        'bracketed_content': (r'\[\[(user:[^:\]]*):[^\]]+\]\]', r'[[\1:]]'),  # Remove content within [[...]] but keep the user identifier
    }

    # Apply each pattern in turn
    for key, value in patterns.items():
        pattern, repl = value
        data = re.sub(pattern, repl, data, flags=re.MULTILINE | re.UNICODE)

    # Replace HTML entities
    data = html.unescape(data)

    # Ensure proper separation of sentences
    # These patterns ensure that there is a space after periods, exclamation marks, and question marks when followed by a capital letter or digit
    data = re.sub(r'(?<=[.!?])\s*(?=[A-Z])', ' ', data)
    data = re.sub(r'(?<=[.!?])\s*(?=\d)', ' ', data)

    # Remove leading and trailing whitespace
    data = data.strip()

    # Replace sequences of whitespace (spaces, newlines, tabs) with a single space, but preserve spaces around punctuation.
    return re.sub(r'\s+', ' ', data)  # Replace multiple whitespace characters with a single space

def get_text_embedding(chunk: str, API_KEY: str, EMBED_MODEL) -> np.ndarray:
    client = OpenAI(api_key=API_KEY)
    response = client.embeddings.create(model=EMBED_MODEL, input=chunk)
    return response.data[0].embedding

def create_vector(metadata: Dict[str, str], API_KEY, EMBED_MODEL) -> List[Dict[str, Any]]:
    """
    Create vectors with embeddings for each chunk of text from metadata.

    Args:
        metadata (Dict[str, str]): Metadata dictionary containing 'id', 'source', 'text', and other optional fields.

    Returns:
        List[Dict[str, Any]]: List of dictionaries containing 'id', 'values' (embeddings), and 'metadata'.
    """
    text = metadata.get('text')

    # Check if text is available
    if text == None or text == "":  # This handles both None and empty string cases
        print(">>> Text not available... Skipping vector creation for", metadata.get("source"))
        return None  # Return None to signify no vectors created

    content_to_embed = metadata.get('source') + text
    chunks = split_text(content_to_embed)
    vector_list = []
    
    for i, chunk in enumerate(chunks):
        try:
            vector = get_text_embedding(chunk, API_KEY, EMBED_MODEL)
        except BadRequestError as e:
            print(f"Token limit passed, skipping vector creation for {metadata.get('source')} chunk {i}...")
            continue  # Skip this chunk and proceed with the next one

        # Only append if vector creation was successful
        chunk_metadata = {
            'id': f"{metadata.get('id')}_{i}",
            'article_id': metadata.get('id'),
            'source': metadata.get('source'),
            'text': chunk,
            'type': metadata.get('type'),
            'url': metadata.get('url', 'No URL Available'),  
            'timestamp': metadata.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")), # Set current date as the timestamp if not provided
            'workflow_state': metadata.get('workflow_state', 'default'),
            'file_name': metadata.get('file_name', 'View More'),
            'attachment_url': metadata.get('attachment_url', 'No URL Available'),
            'chunk_index': i  # Changed to an integer index for consistency
        }

        vector_list.append({
            'id': f"{metadata.get('id')}_{i}",
            'values': vector,
            'metadata': chunk_metadata
        })
    
    return vector_list
