#!/bin/bash

# Script to run all scrapers and ingest data
# Usage: ./scripts/scrape_all.sh

set -e  # Exit on error

BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BACKEND_DIR"

echo "🕷️  Starting scraping process..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Scrape Zara
echo "🛍️  Scraping Zara products..."
python scrapers/zara_fetch.py
echo ""

# Ingest CSVs
echo "💾 Ingesting products to database..."
python scrapers/ingest_csv.py
echo ""

echo "✅ Scraping complete!"
echo ""

# Show summary
echo "📊 Database Summary:"
sqlite3 data/fittingroom.db "SELECT source, COUNT(*) as count FROM products GROUP BY source;"
