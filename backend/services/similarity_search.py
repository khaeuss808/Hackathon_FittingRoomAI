from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from database.db import get_db
from dotenv import load_dotenv
import os

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

index = get_db()

# Generate embedding for your query
query_text = "oversized mustard jacket medium"
query_emb = (
    client.embeddings.create(model="text-embedding-3-large", input=query_text)
    .data[0]
    .embedding
)

# Query Pinecone
results = index.query(vector=query_emb, top_k=5, include_metadata=True)

print("Top similar products:")
for match in results.matches:
    print(match.id, match.score)
