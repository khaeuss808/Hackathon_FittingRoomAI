import sqlite3
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Manage database connections and queries for product data
    """
    
    def __init__(self, db_path: str = 'products.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create a new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database schema if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                image_url TEXT,
                product_url TEXT,
                sizes TEXT,
                colors TEXT,
                styles TEXT,
                category TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def search_products(
        self,
        style_keywords: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sizes: Optional[List[str]] = None,
        brands: Optional[List[str]] = None,
        page: int = 1,
        limit: int = 20
    ) -> List[Dict]:
        """
        Search products with filters
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        # Style keywords filter (search in styles column)
        if style_keywords:
            style_conditions = []
            for keyword in style_keywords:
                style_conditions.append("styles LIKE ?")
                params.append(f"%{keyword}%")
            if style_conditions:
                query += f" AND ({' OR '.join(style_conditions)})"
        
        # Price filter
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        # Size filter
        if sizes:
            size_conditions = []
            for size in sizes:
                size_conditions.append("sizes LIKE ?")
                params.append(f"%{size}%")
            if size_conditions:
                query += f" AND ({' OR '.join(size_conditions)})"
        
        # Brand filter
        if brands:
            brand_conditions = []
            for brand in brands:
                brand_conditions.append("brand LIKE ?")
                params.append(f"%{brand}%")
            if brand_conditions:
                query += f" AND ({' OR '.join(brand_conditions)})"
        
        # Pagination
        offset = (page - 1) * limit
        query += f" ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        products = []
        for row in rows:
            products.append({
                'id': row['id'],
                'name': row['name'],
                'brand': row['brand'],
                'price': row['price'],
                'currency': row['currency'],
                'image': row['image_url'],
                'url': row['product_url'],
                'sizes': row['sizes'].split(',') if row['sizes'] else [],
                'colors': row['colors'].split(',') if row['colors'] else [],
                'styles': row['styles'],
                'category': row['category'],
                'description': row['description']
            })
        
        conn.close()
        return products
    
    def get_product_count(
        self,
        style_keywords: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sizes: Optional[List[str]] = None,
        brands: Optional[List[str]] = None
    ) -> int:
        """
        Get total count of products matching filters
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) as count FROM products WHERE 1=1"
        params = []
        
        if style_keywords:
            style_conditions = []
            for keyword in style_keywords:
                style_conditions.append("styles LIKE ?")
                params.append(f"%{keyword}%")
            if style_conditions:
                query += f" AND ({' OR '.join(style_conditions)})"
        
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        if sizes:
            size_conditions = []
            for size in sizes:
                size_conditions.append("sizes LIKE ?")
                params.append(f"%{size}%")
            if size_conditions:
                query += f" AND ({' OR '.join(size_conditions)})"
        
        if brands:
            brand_conditions = []
            for brand in brands:
                brand_conditions.append("brand LIKE ?")
                params.append(f"%{brand}%")
            if brand_conditions:
                query += f" AND ({' OR '.join(brand_conditions)})"
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        return result['count'] if result else 0
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Get a single product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'name': row['name'],
                'brand': row['brand'],
                'price': row['price'],
                'currency': row['currency'],
                'image': row['image_url'],
                'url': row['product_url'],
                'sizes': row['sizes'].split(',') if row['sizes'] else [],
                'colors': row['colors'].split(',') if row['colors'] else [],
                'styles': row['styles'],
                'category': row['category'],
                'description': row['description']
            }
        return None
    
    def get_all_brands(self) -> List[str]:
        """Get list of all unique brands"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT brand FROM products ORDER BY brand")
        rows = cursor.fetchall()
        conn.close()
        
        return [row['brand'] for row in rows]
    
    def insert_product(self, product_data: Dict) -> int:
        """Insert a new product into the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, brand, price, currency, image_url, product_url, 
                                sizes, colors, styles, category, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_data.get('name'),
            product_data.get('brand'),
            product_data.get('price'),
            product_data.get('currency', 'USD'),
            product_data.get('image_url'),
            product_data.get('product_url'),
            ','.join(product_data.get('sizes', [])),
            ','.join(product_data.get('colors', [])),
            product_data.get('styles'),
            product_data.get('category'),
            product_data.get('description')
        ))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
