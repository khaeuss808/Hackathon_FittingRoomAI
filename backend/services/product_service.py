from typing import List, Dict, Optional
import logging
from database.db_manager import DatabaseManager
from config import Config

logger = logging.getLogger(__name__)


class ProductService:
    """
    Product service layer - handles business logic for product operations
    """

    def __init__(self):
        self.db = DatabaseManager()

    def search_products(
        self,
        style_keywords: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sizes: Optional[List[str]] = None,
        brands: Optional[List[str]] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Dict:
        """
        Search products with filters and return paginated results
        """
        logger.info(f"Searching products with keywords: {style_keywords}")

        products = self.db.search_products(
            style_keywords=style_keywords,
            min_price=min_price,
            max_price=max_price,
            sizes=sizes,
            brands=brands,
            page=page,
            limit=limit,
        )

        total_count = self.db.get_product_count(
            style_keywords=style_keywords,
            min_price=min_price,
            max_price=max_price,
            sizes=sizes,
            brands=brands,
        )

        return {
            "products": products,
            "total": total_count,
            "page": page,
            "limit": limit,
            "totalPages": (total_count + limit - 1) // limit,
        }

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get a single product by ID"""
        return self.db.get_product_by_id(product_id)

    def get_all_brands(self) -> List[str]:
        """Get list of all available brands"""
        return self.db.get_all_brands()

    def add_product(self, product_data: Dict) -> int:
        """Add a new product to the database"""
        return self.db.insert_product(product_data)
