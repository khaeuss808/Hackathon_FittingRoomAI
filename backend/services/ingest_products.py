import os
import csv
from openai import OpenAI
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from database.db import get_db

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Get Pinecone index
index = get_db()

BATCH_SIZE = 50  # adjust based on API rate limits


def ingest_products(csv_path: str):
    """
    Reads products CSV, generates embeddings in batches,
    and upserts them into Pinecone.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    products = []

    # Read CSV and prepare text for embeddings
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product_id = row.get("reference")
            name = row.get("name", "")
            brand = row.get("brand", "")
            category = row.get("category_hint", "")
            color = row.get("color", "")

            text_to_embed = f"{name} {brand} {category} {color}".strip()
            if not text_to_embed:
                print(f"⚠️ Skipping {product_id} — no text to embed")
                continue

            products.append((product_id, text_to_embed))

    print(f"📦 Loaded {len(products)} products for embedding.")

    # Process in batches
    for i in range(0, len(products), BATCH_SIZE):
        batch = products[i : i + BATCH_SIZE]
        texts = [p[1] for p in batch]

        # Generate embeddings in batch
        response = client.embeddings.create(model="text-embedding-3-large", input=texts)
        embeddings = [item.embedding for item in response.data]

        # Upsert into Pinecone
        vectors_to_upsert = [(pid, emb) for (pid, _), emb in zip(batch, embeddings)]
        index.upsert(vectors_to_upsert)

        print(
            f"✅ Upserted batch {i // BATCH_SIZE + 1} ({len(vectors_to_upsert)} products)"
        )

    print("🎉 All embeddings ingested into Pinecone successfully.")


if __name__ == "__main__":
    CSV_PATH = "data/processed/zara_combined.csv"  # adjust path
    ingest_products(CSV_PATH)
