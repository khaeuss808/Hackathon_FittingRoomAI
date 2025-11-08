import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load env vars
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# In many cases the environment/region is now set via spec, not via init
# PINECONE_ENV = os.getenv("PINECONE_ENV")  # you may still use this for region
INDEX_NAME = "product-embeddings"
EMBED_DIM = 3072  # adjust according to your embedding model


def get_db():
    # Instantiate Pinecone client
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create index if it doesn't exist
    existing_indexes = pc.list_indexes().names()
    if INDEX_NAME not in existing_indexes:
        # Here you create the index, you may need to specify region via spec
        spec = ServerlessSpec(
            cloud="aws",  # or "gcp"/"azure" depending on region/plan
            region="us-east-1",  # e.g., "us‑east‑1" or similar
        )
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBED_DIM,
            metric="cosine",  # or "euclidean" depending on use‑case
            spec=spec,
        )
        print(f"Created Pinecone index: {INDEX_NAME}")
    else:
        print(f"Pinecone index ready: {INDEX_NAME}")

    # Return the index object
    index = pc.Index(name=INDEX_NAME)
    return index
