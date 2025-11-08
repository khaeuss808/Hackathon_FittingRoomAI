from flask import Blueprint, jsonify, request
from services.scraper_service import ScraperService
import logging

logger = logging.getLogger(__name__)

scraper_bp = Blueprint('scraper', __name__)
scraper_service = ScraperService()


@scraper_bp.route('/api/scrape/zara', methods=['POST'])
def scrape_zara():
    """
    Trigger Zara product scraping and ingestion
    POST /api/scrape/zara
    """
    try:
        result = scraper_service.scrape_and_ingest_zara()
        status_code = 200 if result.get("success") else 500
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error in scrape_zara endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@scraper_bp.route('/api/scrape/ingest-csv', methods=['POST'])
def ingest_csv():
    """
    Ingest products from CSV files
    POST /api/scrape/ingest-csv
    Body: { "csv_pattern": "data/processed/zara_*.csv" } (optional)
    """
    try:
        data = request.get_json() or {}
        csv_pattern = data.get("csv_pattern", "data/processed/zara_*.csv")
        result = scraper_service.ingest_from_csv(csv_pattern)
        status_code = 200 if result.get("success") else 500
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error in ingest_csv endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@scraper_bp.route('/api/scrape/status', methods=['GET'])
def scraper_status():
    """
    Get scraper service status and available scrapers
    GET /api/scrape/status
    """
    return jsonify({
        "status": "active",
        "available_scrapers": ["zara"],
        "endpoints": {
            "scrape_zara": "POST /api/scrape/zara",
            "ingest_csv": "POST /api/scrape/ingest-csv"
        }
    })
