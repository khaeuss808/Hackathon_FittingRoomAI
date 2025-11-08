from flask import Blueprint, jsonify
import logging
from services.product_service import ProductService

logger = logging.getLogger(__name__)
bp = Blueprint('product', __name__)

product_service = ProductService()

@bp.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = product_service.get_product_by_id(product_id)
        if product:
            return jsonify(product)
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logger.error(f"Error in get_product: {str(e)}")
        return jsonify({'error': str(e)}), 500
