from flask import Blueprint, request, jsonify
import logging
from services.product_service import ProductService
from services.nlp_service import NLPService

logger = logging.getLogger(__name__)
bp = Blueprint("search", __name__)

product_service = ProductService()
nlp_service = NLPService()


@bp.route("/api/search", methods=["GET"])
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
            f"Search request - aesthetic: '{aesthetic}', price: {min_price}-{max_price}"
        )

        clothing_recommendations = []
        style_keywords = []

        if aesthetic and aesthetic.strip():
            # Get structured clothing recommendations from OpenAI
            recommendations = nlp_service.run_nlp_search(aesthetic)
            logger.info(f"NLP recommendations: {recommendations}")

            # Extract search terms from recommendations
            if isinstance(recommendations, list):
                clothing_recommendations = recommendations
                # Build search keywords from item types, colors, and styles
                for item in recommendations:
                    if isinstance(item, dict):
                        if "item_type" in item:
                            style_keywords.append(item["item_type"])
                        if "color" in item:
                            style_keywords.append(item["color"])
                        if "style" in item:
                            style_keywords.append(item["style"])

            logger.info(f"Extracted search keywords: {style_keywords}")

        # Parse filters
        size_list = (
            [s.strip() for s in sizes.split(",") if s.strip()] if sizes else None
        )
        brand_list = (
            [b.strip() for b in brands.split(",") if b.strip()] if brands else None
        )

        result = product_service.search_products(
            style_keywords=style_keywords if style_keywords else [],
            min_price=min_price,
            max_price=max_price,
            sizes=size_list,
            brands=brand_list,
            page=page,
            limit=limit,
        )

        response = {
            "results": result["products"],
            "total": result["total"],
            "page": result["page"],
            "limit": result["limit"],
            "totalPages": result["totalPages"],
            "recommendations": clothing_recommendations,
        }

        logger.info(f"Returning {len(response['results'])} products")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}", exc_info=True)
        return jsonify({"error": str(e), "results": [], "total": 0}), 500


@bp.route("/api/brands", methods=["GET"])
def get_brands():
    """Get all available brands from the database"""
    try:
        brands = product_service.get_all_brands()
        return jsonify({"brands": brands})
    except Exception as e:
        logger.error(f"Error in get_brands: {str(e)}")
        return jsonify({"error": str(e)}), 500
