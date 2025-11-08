import logging
from typing import Dict, List
from scrapers.zara_fetch import fetch_zara_products
from scrapers.ingest_csv import ingest_csvs_to_db, get_engine, init_schema
from sqlalchemy import text
import datetime as dt

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for managing web scraping and data ingestion"""
    
    def __init__(self):
        self.engine = get_engine()
        init_schema(self.engine)
    
    def scrape_and_ingest_zara(self) -> Dict:
        """
        Scrape Zara products and immediately ingest into database
        Returns: status report with count of products added
        """
        try:
            # Fetch products from Zara
            products = fetch_zara_products(save_raw=True, save_csv=True)
            
            # Directly insert into database
            inserted_count = 0
            with self.engine.begin() as conn:
                for product in products:
                    # Check if product already exists
                    result = conn.execute(
                        text("SELECT id FROM products WHERE source = :source AND reference = :ref"),
                        {"source": product.get("source", "zara"), "ref": product.get("reference")}
                    )
                    existing = result.fetchone()
                    
                    if not existing:
                        conn.execute(
                            text("""
                                INSERT INTO products 
                                (source, reference, name, brand, category, color, price_cents, 
                                 price, image_url, product_url, scraped_at)
                                VALUES 
                                (:source, :reference, :name, :brand, :category, :color, 
                                 :price_cents, :price, :image_url, :product_url, :scraped_at)
                            """),
                            {
                                "source": product.get("source", "zara"),
                                "reference": product.get("reference"),
                                "name": product.get("name"),
                                "brand": product.get("brand"),
                                "category": product.get("category"),
                                "color": product.get("color"),
                                "price_cents": product.get("price_cents"),
                                "price": product.get("price"),
                                "image_url": product.get("image_url"),
                                "product_url": product.get("product_url"),
                                "scraped_at": dt.datetime.utcnow().isoformat()
                            }
                        )
                        inserted_count += 1
            
            logger.info(f"Scraped and ingested {inserted_count} new products from Zara")
            
            return {
                "success": True,
                "source": "zara",
                "total_scraped": len(products),
                "new_products": inserted_count,
                "duplicates_skipped": len(products) - inserted_count,
                "timestamp": dt.datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error during scrape and ingest: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": dt.datetime.utcnow().isoformat()
            }
    
    def ingest_from_csv(self, csv_pattern: str = "data/processed/zara_*.csv") -> Dict:
        """
        Ingest products from CSV files
        Returns: status report
        """
        try:
            count = ingest_csvs_to_db(csv_pattern)
            return {
                "success": True,
                "products_ingested": count,
                "csv_pattern": csv_pattern,
                "timestamp": dt.datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error ingesting CSV: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": dt.datetime.utcnow().isoformat()
            }
