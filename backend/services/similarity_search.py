from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from database.db import get_db  # your existing DB/Pinecone wrapper
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Connect to Pinecone index
index = get_db()


def generate_embedding(text: str):
    """Generate an embedding vector for the given text."""
    response = client.embeddings.create(
        model="text-embedding-3-large", input=text  # or 'text-embedding-3-small'
    )
    return response.data[0].embedding


def find_similar_items(item: str, color: str, size: str = ""):
    """Search Pinecone using item + color (+ optional size)."""

    # Build natural text description for better semantic matching
    query_text = f"{color} {item} {size}".strip()

    print(f"\n🔎 Searching for: '{query_text}'")

    # Generate embedding
    query_embedding = generate_embedding(query_text)

    # Query Pinecone index
    results = index.query(vector=query_embedding, top_k=15, include_metadata=True)

    print("\nTop similar products:")
    for match in results.matches:
        print(match.id, match.score)


# find_similar_items(item="jacket", color="mustard", size="medium")
