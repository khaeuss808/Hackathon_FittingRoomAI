from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from database import DatabaseManager
from nlp import NLPProcessor

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database and NLP processor
db = DatabaseManager("products.db")
nlp_processor = NLPProcessor()


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "The Fitting Room API is running"})


@app.route("/api/search", methods=["GET"])
def search_products():
    """
    Search products based on aesthetic keywords and filters
    Query params:
    - aesthetic: string (e.g., "clean girl aesthetic", "cottagecore")
    - minPrice: number
    - maxPrice: number
    - sizes: comma-separated string (e.g., "2,4,6")
    - heights: comma-separated string (e.g., "< 5'1", "< 5'5")
    - brands: comma-separated string (e.g., "H&M,Zara")
    - page: number (default: 1)
    - limit: number (default: 20)
    """
    try:
        # Get query parameters
        aesthetic = request.args.get("aesthetic", "")
        min_price = request.args.get("minPrice", type=float)
        max_price = request.args.get("maxPrice", type=float)
        sizes = request.args.get("sizes", "")
        heights = request.args.get("heights", "")
        brands = request.args.get("brands", "")
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)

        logger.info(
            f"Search request - aesthetic: {aesthetic}, price: {min_price}-{max_price}"
        )

        # Process aesthetic input through NLP to extract keywords
        style_keywords = []
        if aesthetic:
            style_keywords = nlp_processor.extract_keywords(aesthetic)
            logger.info(f"Extracted keywords: {style_keywords}")

        # Parse filters
        size_list = (
            [s.strip() for s in sizes.split(",") if s.strip()] if sizes else None
        )
        brand_list = (
            [b.strip() for b in brands.split(",") if b.strip()] if brands else None
        )

        # Query database
        products = db.search_products(
            style_keywords=style_keywords,
            min_price=min_price,
            max_price=max_price,
            sizes=size_list,
            brands=brand_list,
            page=page,
            limit=limit,
        )

        # Get total count for pagination
        total_count = db.get_product_count(
            style_keywords=style_keywords,
            min_price=min_price,
            max_price=max_price,
            sizes=size_list,
            brands=brand_list,
        )

        return jsonify(
            {
                "products": products,
                "total": total_count,
                "page": page,
                "limit": limit,
                "totalPages": (total_count + limit - 1) // limit,
            }
        )

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/brands", methods=["GET"])
def get_brands():
    """Get all available brands from the database"""
    try:
        brands = db.get_all_brands()
        return jsonify({"brands": brands})
    except Exception as e:
        logger.error(f"Error in get_brands: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = db.get_product_by_id(product_id)
        if product:
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        logger.error(f"Error in get_product: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
