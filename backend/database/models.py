from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Product:
    """Product data model"""
    id: Optional[int]
    name: str
    brand: str
    price: float
    currency: str = 'USD'
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    sizes: List[str] = None
    colors: List[str] = None
    styles: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'price': self.price,
            'currency': self.currency,
            'image': self.image_url,
            'url': self.product_url,
            'sizes': self.sizes or [],
            'colors': self.colors or [],
            'styles': self.styles,
            'category': self.category,
            'description': self.description
        }
