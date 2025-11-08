from flask import Flask
from flask_cors import CORS
import logging
from config import Config
from routers import search_router, product_router, health_router
from routers.scraper_router import scraper_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
        expose_headers=["Content-Type"],
        max_age=3600,
    )

    # Register blueprints (routers)
    app.register_blueprint(health_router.bp)
    app.register_blueprint(search_router.bp)
    app.register_blueprint(product_router.bp)
    app.register_blueprint(scraper_bp)

    logger.info("The Fitting Room API initialized successfully")
    logger.info(f"CORS enabled for: http://localhost:3000, http://127.0.0.1:3000")

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info(f"Starting Flask server on {Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
