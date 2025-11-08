# backend/database/db_manager.py
import sqlite3
from typing import List, Dict, Optional
import logging
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self.init_database()

    def get_connection(self):
        # ensure folder exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        conn = self.get_connection()
        c = conn.cursor()

        c.execute(
            """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            reference TEXT,
            product_id TEXT,              -- ⬅️ from CSV
            name TEXT,
            brand TEXT,
            category TEXT,
            color TEXT,
            price REAL,
            price_cents INTEGER,
            availability TEXT,            -- ⬅️ from CSV
            image_url TEXT,
            product_url TEXT,
            sizes TEXT,
            colors TEXT,
            styles TEXT,
            description TEXT,
            raw JSON,
            scraped_at TEXT DEFAULT (datetime('now')),  -- ⬅️ default timestamp
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        c.execute(
            "CREATE INDEX IF NOT EXISTS idx_products_source   ON products(source)"
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_products_brand    ON products(brand)")
        c.execute(
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)"
        )
        c.execute("CREATE INDEX IF NOT EXISTS idx_products_price    ON products(price)")

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
        limit: int = 20,
    ) -> List[Dict]:
        conn = self.get_connection()
        c = conn.cursor()

        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if style_keywords:
            blocks = []
            for kw in style_keywords:
                blocks.append(
                    "(styles LIKE ? OR name LIKE ? OR description LIKE ? OR category LIKE ?)"
                )
                params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%", f"%{kw}%"])
            query += f" AND ({' OR '.join(blocks)})"

        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)

        if sizes:
            blocks = []
            for s in sizes:
                blocks.append("sizes LIKE ?")
                params.append(f"%{s}%")
            query += f" AND ({' OR '.join(blocks)})"

        if brands:
            blocks = []
            for b in brands:
                blocks.append("brand LIKE ?")
                params.append(f"%{b}%")
            query += f" AND ({' OR '.join(blocks)})"

        offset = (page - 1) * limit
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        c.execute(query, params)
        rows = c.fetchall()
        conn.close()

        products = []
        for row in rows:
            d = dict(row)
            products.append(
                {
                    "id": d.get("id"),
                    "source": d.get("source"),
                    "reference": d.get("reference"),
                    "product_id": d.get("product_id"),
                    "name": d.get("name"),
                    "brand": d.get("brand"),
                    "category": d.get("category"),
                    "color": d.get("color"),
                    "price": d.get("price"),
                    "price_cents": d.get("price_cents"),
                    "availability": d.get("availability"),
                    "image": d.get("image_url"),
                    "url": d.get("product_url"),
                }
            )
        return products

    def get_product_count(
        self,
        style_keywords: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sizes: Optional[List[str]] = None,
        brands: Optional[List[str]] = None,
    ) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        query = "SELECT COUNT(*) AS count FROM products WHERE 1=1"
        params = []

        if style_keywords:
            blocks = []
            for kw in style_keywords:
                blocks.append(
                    "(styles LIKE ? OR name LIKE ? OR description LIKE ? OR category LIKE ?)"
                )
                params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%", f"%{kw}%"])
            query += f" AND ({' OR '.join(blocks)})"

        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)

        if sizes:
            blocks = []
            for s in sizes:
                blocks.append("sizes LIKE ?")
                params.append(f"%{s}%")
            query += f" AND ({' OR '.join(blocks)})"

        if brands:
            blocks = []
            for b in brands:
                blocks.append("brand LIKE ?")
                params.append(f"%{b}%")
            query += f" AND ({' OR '.join(blocks)})"

        c.execute(query, params)
        row = c.fetchone()
        conn.close()
        return int(row["count"]) if row else 0

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return None
        d = dict(row)
        return {
            "id": d.get("id"),
            "source": d.get("source"),
            "reference": d.get("reference"),
            "product_id": d.get("product_id"),
            "name": d.get("name"),
            "brand": d.get("brand"),
            "category": d.get("category"),
            "color": d.get("color"),
            "price": d.get("price"),
            "price_cents": d.get("price_cents"),
            "availability": d.get("availability"),
            "image": d.get("image_url"),
            "url": d.get("product_url"),
        }

    def get_all_brands(self) -> List[str]:
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT DISTINCT brand FROM products ORDER BY brand")
        rows = c.fetchall()
        conn.close()
        return [r["brand"] for r in rows if r["brand"]]

    def insert_product(self, product_data: Dict) -> int:
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO products (
                source, reference, product_id, name, brand, category, color,
                price, price_cents, availability, image_url, product_url, scraped_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?, datetime('now')))
        """,
            (
                product_data.get("source"),
                product_data.get("reference"),
                product_data.get("product_id"),
                product_data.get("name"),
                product_data.get("brand"),
                product_data.get("category"),
                product_data.get("color"),
                product_data.get("price"),
                product_data.get("price_cents"),
                product_data.get("availability"),
                product_data.get("image_url"),
                product_data.get("product_url"),
                product_data.get("scraped_at"),
            ),
        )
        pid = c.lastrowid
        conn.commit()
        conn.close()
        return pid
