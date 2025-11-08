from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('health', __name__)

@bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'message': 'The Fitting Room API is running'
    })
