import sqlite3
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config


def check_database():
    print(f"\n{'='*60}")
    print(f"DATABASE DIAGNOSTIC")
    print(f"{'='*60}\n")

    db_path = Config.DATABASE_PATH
    print(f"Database path: {db_path}")

    # Check if database file exists
    if not Path(db_path).exists():
        print(f"❌ Database file does not exist at {db_path}")
        return

    print(f"✅ Database file exists\n")

    # Connect to database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Check total products
    c.execute("SELECT COUNT(*) as count FROM products")
    total = c.fetchone()["count"]
    print(f"Total products: {total}")

    if total == 0:
        print("❌ Database is empty. Run your Zara scraper to populate it.")
        conn.close()
        return

    # Check brands
    print(f"\n{'='*60}")
    print("BRANDS IN DATABASE:")
    print(f"{'='*60}")
    c.execute("SELECT DISTINCT brand, COUNT(*) as count FROM products GROUP BY brand")
    brands = c.fetchall()
    for row in brands:
        brand_name = row["brand"] if row["brand"] else "[NULL/EMPTY]"
        print(f"  • {brand_name}: {row['count']} products")

    # Check sample products
    print(f"\n{'='*60}")
    print("SAMPLE PRODUCTS (first 3):")
    print(f"{'='*60}")
    c.execute(
        "SELECT id, name, brand, price, sizes, availability FROM products LIMIT 3"
    )
    samples = c.fetchall()
    for row in samples:
        print(f"\nID: {row['id']}")
        print(f"  Name: {row['name']}")
        print(f"  Brand: {row['brand']}")
        print(f"  Price: ${row['price']}")
        print(f"  Sizes: {row['sizes']}")
        print(f"  Availability: {row['availability']}")

    # Test brand search
    print(f"\n{'='*60}")
    print("TESTING BRAND SEARCH:")
    print(f"{'='*60}")

    # Try exact match
    c.execute("SELECT COUNT(*) as count FROM products WHERE brand = 'Zara'")
    exact_match = c.fetchone()["count"]
    print(f"Exact match 'Zara': {exact_match} products")

    # Try case-insensitive LIKE
    c.execute("SELECT COUNT(*) as count FROM products WHERE brand LIKE '%zara%'")
    like_match = c.fetchone()["count"]
    print(f"LIKE '%zara%': {like_match} products")

    # Test with actual brand from database
    if brands and brands[0]["brand"]:
        test_brand = brands[0]["brand"]
        c.execute(
            "SELECT COUNT(*) as count FROM products WHERE brand LIKE ?",
            (f"%{test_brand}%",),
        )
        test_count = c.fetchone()["count"]
        print(f"LIKE '%{test_brand}%': {test_count} products")

    # Check sizes field
    print(f"\n{'='*60}")
    print("SIZE FILTERING TEST:")
    print(f"{'='*60}")
    c.execute(
        "SELECT sizes FROM products WHERE sizes IS NOT NULL AND sizes != '' LIMIT 5"
    )
    size_samples = c.fetchall()
    if size_samples:
        print("Sample sizes values:")
        for row in size_samples:
            print(f"  • {row['sizes']}")
    else:
        print("❌ No products have sizes data")

    conn.close()

    print(f"\n{'='*60}")
    print("RECOMMENDATIONS:")
    print(f"{'='*60}")
    print("1. Check if brand names in database match what you're searching for")
    print("2. Make sure Zara scraper is actually populating the 'brand' field")
    print("3. Size filtering might fail if 'sizes' field is empty")
    print("4. Consider case-insensitive brand matching in your queries")


if __name__ == "__main__":
    check_database()
