# Web Scraper Integration Guide

## Overview

The Fitting Room includes a web scraping system that automatically fetches product data from fashion retailers and ingests it into your database. Currently supports **Zara** with the ability to add more retailers.

## Architecture

\`\`\`
backend/
├── scrapers/
│   ├── __init__.py
│   ├── zara_fetch.py      # Scrapes Zara product API
│   └── ingest_csv.py      # Ingests CSV data to database
├── services/
│   └── scraper_service.py # Business logic for scraping
└── routers/
    └── scraper_router.py  # API endpoints for scraping
\`\`\`

## How It Works

### 1. Zara Scraper (`zara_fetch.py`)

Fetches products from Zara's public API:
- Sends requests to Zara's category API
- Parses JSON response for product details
- Normalizes data (name, price, images, URLs)
- Saves raw JSON and processed CSV

**Data Collected:**
- Product ID & reference
- Name, brand, category
- Price (in cents and dollars)
- Color variants
- Product images (high-res URLs)
- Product page URLs

### 2. CSV Ingestion (`ingest_csv.py`)

Imports CSV data into SQLite database:
- Reads CSV files from `data/processed/`
- Normalizes column names
- Handles price conversions
- Deduplicates products by source + reference
- Creates indexes for fast querying

### 3. Scraper Service (`scraper_service.py`)

Orchestrates scraping workflow:
- `scrape_and_ingest_zara()` - Fetch & insert in one operation
- `ingest_from_csv()` - Import existing CSV files
- Handles errors gracefully
- Returns detailed status reports

## API Endpoints

### Trigger Zara Scraping

\`\`\`bash
POST /api/scrape/zara
\`\`\`

**Response:**
\`\`\`json
{
  "success": true,
  "source": "zara",
  "total_scraped": 47,
  "new_products": 42,
  "duplicates_skipped": 5,
  "timestamp": "2025-01-08T12:34:56.789Z"
}
\`\`\`

### Ingest CSV Files

\`\`\`bash
POST /api/scrape/ingest-csv
Content-Type: application/json

{
  "csv_pattern": "data/processed/zara_*.csv"
}
\`\`\`

**Response:**
\`\`\`json
{
  "success": true,
  "products_ingested": 150,
  "csv_pattern": "data/processed/zara_*.csv",
  "timestamp": "2025-01-08T12:34:56.789Z"
}
\`\`\`

### Check Scraper Status

\`\`\`bash
GET /api/scrape/status
\`\`\`

**Response:**
\`\`\`json
{
  "status": "active",
  "available_scrapers": ["zara"],
  "endpoints": {
    "scrape_zara": "POST /api/scrape/zara",
    "ingest_csv": "POST /api/scrape/ingest-csv"
  }
}
\`\`\`

## Usage

### Option 1: API-Triggered Scraping

Use the REST API to scrape on-demand:

\`\`\`bash
# Start Flask server
cd backend
python main.py

# Trigger scraping (from another terminal)
curl -X POST http://localhost:5000/api/scrape/zara
\`\`\`

### Option 2: Command-Line Scraping

Run scrapers directly as Python scripts:

\`\`\`bash
cd backend

# Fetch Zara products
python scrapers/zara_fetch.py

# Ingest CSV to database
python scrapers/ingest_csv.py
\`\`\`

### Option 3: Scheduled Scraping (Cron)

Set up automatic scraping with cron jobs:

\`\`\`bash
# Edit crontab
crontab -e

# Add this line to scrape Zara daily at 2 AM
0 2 * * * cd /path/to/backend && python scrapers/zara_fetch.py && python scrapers/ingest_csv.py
\`\`\`

## Database Schema

Products table includes scraper-specific fields:

\`\`\`sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,           -- 'zara', 'hm', etc.
    reference TEXT,                 -- Product SKU/reference
    name TEXT,
    brand TEXT,
    category TEXT,
    color TEXT,
    price_cents INTEGER,
    price REAL,
    image_url TEXT,
    product_url TEXT,
    sizes TEXT,                     -- Comma-separated
    colors TEXT,                    -- Comma-separated
    styles TEXT,                    -- For aesthetic matching
    description TEXT,
    raw JSON,                       -- Original data for debugging
    scraped_at TEXT NOT NULL,       -- When scraped
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\`\`\`

**Indexes for performance:**
- `idx_products_source_ref` - Prevent duplicates
- `idx_products_category` - Filter by category
- `idx_products_price` - Price range queries
- `idx_products_brand` - Brand filtering

## Adding New Scrapers

### 1. Create Scraper Module

\`\`\`python
# backend/scrapers/hm_fetch.py

def fetch_hm_products():
    """Fetch products from H&M"""
    # 1. Make API request
    # 2. Parse response
    # 3. Normalize data format
    # 4. Save CSV (optional)
    # 5. Return list of products
    pass
\`\`\`

### 2. Update Scraper Service

\`\`\`python
# backend/services/scraper_service.py

def scrape_and_ingest_hm(self):
    """Scrape H&M and ingest"""
    from scrapers.hm_fetch import fetch_hm_products
    products = fetch_hm_products()
    # ... insert logic ...
\`\`\`

### 3. Add API Endpoint

\`\`\`python
# backend/routers/scraper_router.py

@scraper_bp.route('/api/scrape/hm', methods=['POST'])
def scrape_hm():
    result = scraper_service.scrape_and_ingest_hm()
    return jsonify(result)
\`\`\`

## Configuration

Set environment variables in `.env`:

\`\`\`bash
# Database location
DB_PATH=backend/data/fittingroom.db

# CSV storage
CSV_PATH=data/raw/zara_*.csv

# Scraping rate limits (optional)
SCRAPE_DELAY=1.0  # seconds between requests
MAX_RETRIES=3
\`\`\`

## Data Flow

\`\`\`
┌─────────────┐
│ Zara API    │
└──────┬──────┘
       │ HTTP Request
       ↓
┌─────────────────────┐
│ zara_fetch.py       │  Fetch & parse
│ - Normalize data    │
│ - Save raw JSON     │
│ - Export CSV        │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│ data/processed/*.csv│
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│ ingest_csv.py       │  Load to DB
│ - Read CSV          │
│ - Deduplicate       │
│ - Insert products   │
└──────┬──────────────┘
       │
       ↓
┌─────────────────────┐
│ SQLite Database     │
│ products table      │
└─────────────────────┘
       │
       ↓
┌─────────────────────┐
│ Search API          │  Query
│ /api/search         │
└─────────────────────┘
\`\`\`

## Best Practices

### 1. Rate Limiting
Add delays between requests to avoid being blocked:

\`\`\`python
import time
for product in products:
    fetch_product_details(product)
    time.sleep(1)  # 1 second delay
\`\`\`

### 2. Error Handling
Always catch and log errors:

\`\`\`python
try:
    products = fetch_zara_products()
except requests.RequestException as e:
    logger.error(f"Network error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
\`\`\`

### 3. Deduplication
Check for existing products before inserting:

\`\`\`python
existing = conn.execute(
    "SELECT id FROM products WHERE source = ? AND reference = ?",
    (source, reference)
).fetchone()

if not existing:
    conn.execute("INSERT INTO products ...")
\`\`\`

### 4. Data Validation
Validate required fields:

\`\`\`python
if not product.get('name') or not product.get('price'):
    logger.warning(f"Invalid product: {product}")
    continue
\`\`\`

## Troubleshooting

### No Products Scraped

**Problem:** `total_scraped: 0`

**Solutions:**
1. Check Zara's website structure hasn't changed
2. Verify the API URL is still valid
3. Check your internet connection
4. Review logs for HTTP errors

### Duplicate Products

**Problem:** Same products appearing multiple times

**Solutions:**
1. Ensure `reference` field is properly set
2. Check deduplication logic in scraper service
3. Manually clean database:
   \`\`\`sql
   DELETE FROM products WHERE id NOT IN (
       SELECT MIN(id) FROM products GROUP BY source, reference
   );
   \`\`\`

### CSV Import Fails

**Problem:** `ingest_csv` returns 0 products

**Solutions:**
1. Check CSV file path is correct
2. Verify CSV files exist in `data/processed/`
3. Check CSV column names match expected format
4. Review normalization logic in `ingest_csv.py`

### Scraper Gets Blocked

**Problem:** HTTP 403 or 429 errors

**Solutions:**
1. Add user-agent headers (already included)
2. Increase delays between requests
3. Use proxy rotation (advanced)
4. Contact retailer for API access

## Monitoring

### Check Database Status

\`\`\`bash
sqlite3 backend/data/fittingroom.db

-- Count total products
SELECT COUNT(*) FROM products;

-- Products by source
SELECT source, COUNT(*) FROM products GROUP BY source;

-- Recent scrapes
SELECT source, COUNT(*), MAX(scraped_at) 
FROM products 
GROUP BY source;
\`\`\`

### View Scraper Logs

\`\`\`bash
# If running as service
tail -f backend/scraper.log

# Or check Flask logs
tail -f backend/flask.log
\`\`\`

## Future Enhancements

- [ ] Add more retailers (H&M, Forever 21, Urban Outfitters)
- [ ] Implement proxy rotation for scale
- [ ] Add product availability tracking
- [ ] Schedule automatic scraping with Celery
- [ ] Add webhook notifications on new products
- [ ] Create admin dashboard for scraper management
- [ ] Implement incremental updates (only fetch new products)

## Resources

- Zara API Documentation: (reverse-engineered)
- Web Scraping Best Practices: https://www.scraperapi.com/blog/web-scraping-best-practices/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Pandas CSV Handling: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
