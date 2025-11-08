from openai import OpenAI
from config import Config
import json
import logging

logger = logging.getLogger(__name__)

class NLPService:
    """
    NLP service using OpenAI to convert aesthetic descriptions 
    into structured clothing recommendations
    """
    
    SYSTEM_PROMPT = """
You are a fashion assistant. Convert any aesthetic or vibe description into a structured JSON list of clothing recommendations.

Each item must be a real, shoppable clothing type found on common fashion retail sites.

For each item, include:
- "item_type": specific and realistic item name (e.g., "white t-shirt", "high-waisted jeans", "leather jacket")
- "color": a simple, descriptive color (e.g., "black", "beige", "light blue")
- "style": a short phrase describing the overall aesthetic (e.g., "minimalist streetwear", "boho chic")

Output only valid JSON array — no commentary or extra text.

Example output format:
[
  {"item_type": "oversized white t-shirt", "color": "white", "style": "minimalist casual"},
  {"item_type": "high-waisted mom jeans", "color": "light blue", "style": "casual denim"}
]
"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info("OpenAI client initialized")
    
    def run_nlp_search(self, user_description: str):
        """
        Convert natural language vibe description into structured clothing recommendations.
        
        Args:
            user_description: User's aesthetic description (e.g., "clean girl aesthetic")
            
        Returns:
            List of structured clothing recommendations or fallback data
        """
        if not self.client:
            logger.error("OpenAI client not initialized - API key missing")
            # Fallback to basic keyword extraction
            return self._fallback_extraction(user_description)
        
        try:
            logger.info(f"Processing NLP search for: '{user_description}'")
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_description},
                ],
                temperature=0.7
            )

            # Parse the model output
            content = response.choices[0].message.content.strip()
            logger.debug(f"OpenAI response: {content}")
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            structured_output = json.loads(content)
            logger.info(f"Successfully parsed {len(structured_output)} recommendations")
            
            return structured_output
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Raw content: {content}")
            return self._fallback_extraction(user_description)
            
        except Exception as e:
            logger.error(f"Error in run_nlp_search: {str(e)}", exc_info=True)
            return self._fallback_extraction(user_description)
    
    def _fallback_extraction(self, description: str):
        """
        Fallback method when OpenAI is unavailable
        Returns basic keyword extraction
        """
        logger.info("Using fallback keyword extraction")
        
        # Basic aesthetic to style mapping
        aesthetic_map = {
            'clean girl': [
                {'item_type': 'white t-shirt', 'color': 'white', 'style': 'minimalist'},
                {'item_type': 'straight leg jeans', 'color': 'blue', 'style': 'casual'}
            ],
            'boho': [
                {'item_type': 'flowy maxi dress', 'color': 'earth tones', 'style': 'bohemian'},
                {'item_type': 'embroidered top', 'color': 'cream', 'style': 'boho chic'}
            ],
            'cottagecore': [
                {'item_type': 'floral dress', 'color': 'pastel', 'style': 'romantic'},
                {'item_type': 'lace blouse', 'color': 'white', 'style': 'vintage'}
            ],
            'streetwear': [
                {'item_type': 'oversized hoodie', 'color': 'black', 'style': 'urban'},
                {'item_type': 'cargo pants', 'color': 'olive', 'style': 'street'}
            ]
        }
        
        # Try to match aesthetic
        description_lower = description.lower()
        for aesthetic, items in aesthetic_map.items():
            if aesthetic in description_lower:
                return items
        
        # Generic fallback
        return [
            {'item_type': 'basic top', 'color': 'neutral', 'style': description},
            {'item_type': 'pants', 'color': 'neutral', 'style': description}
        ]
