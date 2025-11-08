import re
from typing import List

class NLPProcessor:
    """
    Process user aesthetic descriptions and extract relevant style keywords
    """
    
    def __init__(self):
        # Define aesthetic keyword mappings
        self.aesthetic_keywords = {
            'clean girl': ['minimal', 'clean', 'simple', 'neutral', 'sleek', 'modern'],
            'cottagecore': ['floral', 'vintage', 'romantic', 'soft', 'pastoral', 'feminine'],
            'dark academia': ['vintage', 'classic', 'preppy', 'scholarly', 'tweed', 'plaid'],
            'streetwear': ['urban', 'casual', 'oversized', 'athletic', 'sporty', 'contemporary'],
            'minimalist': ['minimal', 'simple', 'clean', 'basic', 'essential', 'timeless'],
            'boho': ['bohemian', 'eclectic', 'flowy', 'ethnic', 'relaxed', 'artistic'],
            'preppy': ['classic', 'collegiate', 'neat', 'polished', 'traditional', 'nautical'],
            'grunge': ['edgy', 'distressed', 'dark', 'oversized', 'vintage', 'rebellious'],
            'romantic': ['feminine', 'soft', 'delicate', 'floral', 'lace', 'dreamy'],
            'sporty': ['athletic', 'active', 'comfortable', 'functional', 'casual', 'dynamic'],
            'elegant': ['sophisticated', 'refined', 'polished', 'classic', 'graceful', 'formal'],
            'casual': ['relaxed', 'comfortable', 'everyday', 'effortless', 'laid-back', 'simple'],
            'vintage': ['retro', 'classic', 'timeless', 'antique', 'nostalgic', 'old-fashioned'],
            'modern': ['contemporary', 'current', 'sleek', 'minimalist', 'fresh', 'innovative'],
            'edgy': ['bold', 'daring', 'unconventional', 'rebellious', 'dark', 'dramatic']
        }
        
        # Color keywords
        self.color_keywords = [
            'black', 'white', 'beige', 'cream', 'brown', 'tan', 'navy', 'blue',
            'red', 'pink', 'green', 'yellow', 'purple', 'gray', 'grey', 'neutral'
        ]
        
        # Pattern keywords
        self.pattern_keywords = [
            'striped', 'plaid', 'floral', 'checkered', 'polka dot', 'solid',
            'geometric', 'abstract', 'paisley', 'animal print'
        ]
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract style keywords from user input text
        Returns a list of relevant keywords for database querying
        """
        if not text:
            return []
        
        text_lower = text.lower()
        keywords = set()
        
        # Check for aesthetic keywords
        for aesthetic, related_keywords in self.aesthetic_keywords.items():
            if aesthetic in text_lower:
                keywords.update(related_keywords)
        
        # Check for color keywords
        for color in self.color_keywords:
            if color in text_lower:
                keywords.add(color)
        
        # Check for pattern keywords
        for pattern in self.pattern_keywords:
            if pattern in text_lower:
                keywords.add(pattern)
        
        # Extract individual words (filter out common stop words)
        stop_words = {'i', 'want', 'looking', 'for', 'like', 'style', 'aesthetic', 'the', 'a', 'an'}
        words = re.findall(r'\b\w+\b', text_lower)
        for word in words:
            if word not in stop_words and len(word) > 2:
                keywords.add(word)
        
        return list(keywords)
    
    def match_score(self, product_styles: str, keywords: List[str]) -> int:
        """
        Calculate how well a product's styles match the search keywords
        Returns a score (higher is better)
        """
        if not product_styles or not keywords:
            return 0
        
        product_styles_lower = product_styles.lower()
        score = 0
        
        for keyword in keywords:
            if keyword.lower() in product_styles_lower:
                score += 1
        
        return score
