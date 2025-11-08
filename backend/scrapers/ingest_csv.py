import os, datetime as dt
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)


def get_db_path():
    """Get database path from environment or default"""
    return os.environ.get("DB_PATH", "../data/fittingroom.db")


def get_engine():
    """Create SQLAlchemy engine for database operations"""
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return create_engine(f"sqlite:///{db_path}", future=True)


def init_schema(engine):
    """Initialize database schema with scraped product structure"""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            reference TEXT,
            name TEXT,
            brand TEXT,
            category TEXT,
            color TEXT,
            price_cents INTEGER,
            price REAL,
            image_url TEXT,
            product_url TEXT,
            sizes TEXT,
            colors TEXT,
            styles TEXT,
            description TEXT,
            raw JSON,
            scraped_at TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
            )
        )
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_products_source_ref ON products(source, reference);"
            )
        )
        conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_products_cat ON products(category);")
        )
        conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);")
        )
        conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);")
        )
    logger.info("Database schema initialized")


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize CSV data to match database schema"""
    cols = {c.lower(): c for c in df.columns}
    pick = {
        "reference": cols.get("reference")
        or cols.get("canonicalreference")
        or cols.get("ref")
        or cols.get("product_id"),
        "name": cols.get("name"),
        "brand": cols.get("brand", None),
        "category": cols.get("category", None) or cols.get("category_hint", None),
        "color": cols.get("color", None),
        "price": cols.get("price") or cols.get("price_usd") or cols.get("price_cents"),
        "image_url": cols.get("image_url")
        or cols.get("pdpimage")
        or cols.get("pdpmedia"),
        "product_url": cols.get("product_url")
        or cols.get("url")
        or cols.get("seo_url"),
    }
    df2 = pd.DataFrame(
        {k: df[v] if v and v in df.columns else None for k, v in pick.items()}
    )

    def to_price(v):
        try:
            v = float(v)
            return v / 100.0 if v > 200 and int(v) == v else v
        except Exception:
            return None

    df2["price"] = df2["price"].apply(to_price)
    df2["price_cents"] = (df2["price"].fillna(0) * 100).round().astype(int)
    df2["source"] = (
        df.get("source", "zara").iloc[0] if "source" in df.columns else "zara"
    )
    df2["scraped_at"] = dt.datetime.utcnow().isoformat()
    df2["raw"] = df.apply(lambda r: r.to_json(), axis=1)

    return df2[
        [
            "source",
            "reference",
            "name",
            "brand",
            "category",
            "color",
            "price_cents",
            "price",
            "image_url",
            "product_url",
            "raw",
            "scraped_at",
        ]
    ]


def ingest_csvs_to_db(csv_pattern="data/processed/zara_*.csv"):
    """
    Ingest CSV files matching pattern into the database
    Returns: number of products ingested
    """
    import glob

    engine = get_engine()
    init_schema(engine)

    paths = sorted(glob.glob(csv_pattern))
    if not paths:
        logger.warning(f"No CSVs found at {csv_pattern}")
        return 0

    logger.info(f"Found {len(paths)} CSV file(s)")
    total_ingested = 0

    for p in paths:
        logger.info(f"Loading {p}")
        df = pd.read_csv(p)
        df = normalize(df)
        df.to_sql("products", engine, if_exists="append", index=False)
        total_ingested += len(df)

    logger.info(f"Successfully ingested {total_ingested} products")
    return total_ingested


if __name__ == "__main__":
    count = ingest_csvs_to_db()
    print(f"Ingested {count} products into database")
