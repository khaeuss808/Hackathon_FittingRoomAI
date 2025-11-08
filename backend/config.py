import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# BASE_DIR = Path(__file__).resolve().parent  # .../backend
# DATA_DIR = BASE_DIR / "data"
# DATA_DIR.mkdir(parents=True, exist_ok=True)


class Config:
    """Application configuration"""

    # Flask settings
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5001))  # CHANGE PORT
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Database settings
    # DATABASE_PATH = os.getenv("DATABASE_PATH", "products.db")
    # kayla: commenting out
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Database path — resolve relative to backend/
    DATABASE_PATH = os.path.join(BASE_DIR, "data", "fittingroom.db")

    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
