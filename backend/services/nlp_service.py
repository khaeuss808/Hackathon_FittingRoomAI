# backend/routes/nlp_search.py
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

(
    SYSTEM_PROMPT
) = """
You are a fashion assistant. Convert any aesthetic or vibe description into a structured JSON list of clothing recommendations.

Each item must be a real, shoppable clothing type found on common fashion retail sites.

For each item, include:
- "item_type": specific and realistic item name (e.g., "white t-shirt", "high-waisted jeans", "leather jacket")
- "color": a simple, descriptive color (e.g., "black", "beige", "light blue")
- "style": a short phrase describing the overall aesthetic (e.g., "minimalist streetwear", "boho chic")

Output only valid JSON — no commentary or extra text.
"""


def run_nlp_search(user_description: str):
    """
    Convert natural language vibe description into structured clothing recommendations.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_description},
        ],
    )

    # Parse the model output safely
    content = response.choices[0].message.content.strip()
    try:
        structured_output = json.loads(content)
    except json.JSONDecodeError:
        # fallback if LLM returns invalid JSON (rare)
        structured_output = {"raw_text": content}

    return structured_output


# trying to see if it works
prompt = "I want the boho chic aesthetic"
print(run_nlp_search(prompt))
