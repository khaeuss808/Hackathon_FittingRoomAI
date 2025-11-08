# The Fitting Room - Backend API

Modularized Flask backend with OpenAI-powered NLP search for personalized fashion recommendations.

## 📁 Project Structure

\`\`\`
backend/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── health_router.py   # Health check endpoint
│   ├── search_router.py   # Product search with NLP
│   └── product_router.py  # Product details endpoint
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── nlp_service.py     # OpenAI NLP integration
│   └── product_service.py # Product operations
├── database/              # Data access layer
│   ├── __init__.py
│   ├── db_manager.py      # Database operations
│   └── models.py          # Data models
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
\`\`\`

## 🚀 Quick Start

### 1. Install Dependencies

\`\`\`bash
cd backend
pip install -r requirements.txt
\`\`\`

### 2. Configure Environment

\`\`\`bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
\`\`\`

### 3. Seed Database

\`\`\`bash
python seed_data.py
\`\`\`

This creates `products.db` with sample fashion products.

### 4. Run Server

\`\`\`bash
python main.py
\`\`\`

Or use the convenience script:

\`\`\`bash
chmod +x run.sh
./run.sh
\`\`\`

Server will start at `http://localhost:5000`

## 🔌 API Endpoints

### Health Check
\`\`\`
GET /api/health
\`\`\`
Returns API status.

**Response:**
\`\`\`json
{
  "status": "healthy",
  "message": "The Fitting Room API is running"
}
\`\`\`

### Search Products
\`\`\`
GET /api/search?aesthetic=clean girl aesthetic&minPrice=20&maxPrice=150
\`\`\`

**Query Parameters:**
- `aesthetic` (string) - Natural language aesthetic description
- `minPrice` (number) - Minimum price filter
- `maxPrice` (number) - Maximum price filter
- `sizes` (string) - Comma-separated sizes (e.g., "2,4,6")
- `brands` (string) - Comma-separated brands (e.g., "Zara,H&M")
- `page` (number) - Page number (default: 1)
- `limit` (number) - Items per page (default: 20)

**Response:**
\`\`\`json
{
  "products": [...],
  "total": 45,
  "page": 1,
  "limit": 20,
  "totalPages": 3,
  "recommendations": [
    {
      "item_type": "white t-shirt",
      "color": "white",
      "style": "minimalist casual"
    }
  ]
}
\`\`\`

### Get Product by ID
\`\`\`
GET /api/product/1
\`\`\`

**Response:**
\`\`\`json
{
  "id": 1,
  "name": "Oversized White Tee",
  "brand": "Zara",
  "price": 29.90,
  "image": "/placeholder.svg",
  "sizes": ["XS", "S", "M", "L"],
  "colors": ["White", "Cream"],
  "styles": "minimal, clean girl, modern",
  "description": "Classic oversized white t-shirt"
}
\`\`\`

### Get All Brands
\`\`\`
GET /api/brands
\`\`\`

**Response:**
\`\`\`json
{
  "brands": ["Zara", "H&M", "Reformation", "Everlane"]
}
\`\`\`

## 🤖 NLP Integration

The backend uses OpenAI's GPT-4 to convert natural language aesthetic descriptions into structured clothing recommendations.

**Example:**
\`\`\`
Input: "I want the clean girl aesthetic"

OpenAI Output:
[
  {
    "item_type": "white t-shirt",
    "color": "white", 
    "style": "minimalist casual"
  },
  {
    "item_type": "high-waisted jeans",
    "color": "light blue",
    "style": "casual denim"
  }
]

Search Keywords: ["white t-shirt", "white", "minimalist casual", "high-waisted jeans", "light blue", "casual denim"]
\`\`\`

These keywords are then used to search the product database.

## 🗄️ Database Schema

\`\`\`sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    image_url TEXT,
    product_url TEXT,
    sizes TEXT,              -- Comma-separated
    colors TEXT,             -- Comma-separated
    styles TEXT,             -- Space/comma-separated keywords
    category TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
\`\`\`

## 🔧 Configuration

Edit `.env` to configure:

\`\`\`env
# Flask settings
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# Database
DATABASE_PATH=products.db

# OpenAI (Required for NLP search)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
\`\`\`

## 📝 Adding Products from Web Scraper

To integrate your web scraper data:

\`\`\`python
from database.db_manager import DatabaseManager

db = DatabaseManager()
product_id = db.insert_product({
    'name': 'Product Name',
    'brand': 'Brand Name',
    'price': 99.99,
    'image_url': 'https://...',
    'product_url': 'https://...',
    'sizes': ['S', 'M', 'L'],
    'colors': ['Black', 'White'],
    'styles': 'minimal, clean, modern',  # Important for search!
    'category': 'Tops',
    'description': 'Product description'
})
\`\`\`

## 🧪 Testing

Test the API:

\`\`\`bash
# Health check
curl http://localhost:5000/api/health

# Search with aesthetic
curl "http://localhost:5000/api/search?aesthetic=boho%20chic"

# Get specific product
curl http://localhost:5000/api/product/1

# Get all brands
curl http://localhost:5000/api/brands
\`\`\`

## 🔗 Frontend Integration

The backend is designed to work with the Next.js frontend. Set the frontend's `NEXT_PUBLIC_API_URL` environment variable to:

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:5000
\`\`\`

You can set this in the Vars section of the v0 in-chat sidebar.

## 📦 Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **OpenAI 1.12.0** - GPT-4 integration for NLP
- **python-dotenv 1.0.0** - Environment variable management
- **SQLite3** - Built-in database (no installation needed)

## 🚨 Troubleshooting

**OpenAI API errors:**
- Make sure `OPENAI_API_KEY` is set in `.env`
- Check your OpenAI account has credits
- The system will fallback to basic keyword extraction if OpenAI fails

**Database errors:**
- Delete `products.db` and run `python seed_data.py` again
- Check file permissions in the backend directory

**CORS errors:**
- Make sure Flask-CORS is installed
- Check frontend URL matches allowed origins

**Module import errors:**
- Make sure you're running from the backend directory
- Check all `__init__.py` files exist in subdirectories

## 📄 Architecture

See `ARCHITECTURE.md` for detailed information about the modular backend structure, data flow, and design patterns.
