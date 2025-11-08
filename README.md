# The Fitting Room - Frontend Integration

A personalized fashion discovery platform that helps users find clothing matching their style, body type, and preferences.

## Architecture Overview

### Frontend (Next.js)
- **Home Page** (`/`): Personalized search interface for user preferences
- **About Page** (`/about`): Platform information and values
- **Brands Page** (`/brands`): Featured brand showcase
- **Shop Page** (`/shop`): Product results with filtering and pagination

### Backend (Flask - Python)
Located in your `backend/` directory with the following endpoints:

- `GET /api/health` - Health check for database connection
- `GET /api/zara` - Browse all products with pagination
- `POST /api/search` - Filter-based search with NLP-powered keyword matching

## Backend Integration

### Flask API Endpoints

#### 1. Health Check
\`\`\`bash
GET http://127.0.0.1:5000/api/health
\`\`\`
Returns database connection status.

#### 2. Browse Products
\`\`\`bash
GET http://127.0.0.1:5000/api/zara?page=1&per_page=20
\`\`\`
Returns paginated product list from the database.

#### 3. Search Products
\`\`\`bash
POST http://127.0.0.1:5000/api/search
Content-Type: application/json

{
  "styles": ["clean girl", "minimalist"],
  "category": "clothing",
  "min_price": 0,
  "max_price": 200,
  "page": 1,
  "per_page": 20
}
\`\`\`
Filters products based on:
- `styles` - Array of keywords processed by your NLP.py (searches in styles column)
- `category` - Exact category match
- `min_price` / `max_price` - Price range filtering
- `page` / `per_page` - Pagination

## Setup Instructions

### 1. Backend Setup (Flask)

\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

Update the database path in `backend/app.py`:
\`\`\`python
DB_FILE_PATH = "/path/to/your/fittingroom.db"
\`\`\`

Start the Flask server:
\`\`\`bash
python app.py
\`\`\`
The API will run on `http://127.0.0.1:5000`

### 2. Frontend Setup (Next.js)

\`\`\`bash
npm install
\`\`\`

Create `.env.local` file:
\`\`\`env
NEXT_PUBLIC_API_URL=http://127.0.0.1:5000
\`\`\`

Start the development server:
\`\`\`bash
npm run dev
\`\`\`
The frontend will run on `http://localhost:3000`

## User Flow

1. **Home Page** - User enters preferences:
   - Clothing size selection (0-16)
   - Height range
   - Price range
   - Aesthetic keywords (e.g., "clean girl aesthetic", "cottagecore")
   - Brand preferences

2. **Search Processing**:
   - Frontend sends preferences to Flask `/api/search` endpoint
   - Backend uses NLP.py to extract keywords from aesthetic input
   - Database query filters products by styles, price, and other criteria
   - Results returned with pagination

3. **Shop Page** - Displays results:
   - Product grid with images, names, prices
   - Sidebar filters for refining search
   - Pagination controls
   - Direct links to product URLs

## Database Structure

Your SQLite database (`fittingroom.db`) should have a `zara_data` table with columns:
- `id` - Unique product identifier
- `name` or `product_name` - Product name
- `brand` - Brand name
- `price` or `price_raw` - Product price
- `image_url` or `image` - Product image URL
- `product_url` or `url` - Link to product page
- `category` - Product category
- `styles` - Comma-separated style keywords (used for NLP matching)
- `availability` - Stock status

## Adding NLP Integration

Your `backend/nlp.py` should export a function that processes aesthetic keywords:

\`\`\`python
# backend/nlp.py
def extract_keywords(user_input: str) -> list[str]:
    """
    Process user input like "clean girl aesthetic" and return
    relevant keywords for database search.
    
    Example:
    extract_keywords("clean girl aesthetic") 
    -> ["minimal", "neutral", "simple", "modern"]
    """
    # Your NLP processing logic here
    pass
\`\`\`

Then integrate into `backend/app.py`:
\`\`\`python
from nlp import extract_keywords

@app.post("/api/search")
def traditional_search():
    filters = request.get_json(silent=True) or {}
    
    # Process aesthetic keywords with NLP
    if filters.get("aesthetic"):
        raw_aesthetic = filters["aesthetic"]
        processed_keywords = extract_keywords(raw_aesthetic)
        filters["styles"] = processed_keywords
    
    # ... rest of your search logic
\`\`\`

## Deployment

### Deploy to Vercel (Frontend)
\`\`\`bash
vercel
\`\`\`

### Backend Deployment Options
1. **Fly.io** - Easy Python deployment
2. **Railway** - One-click Flask hosting  
3. **Heroku** - Traditional PaaS option

Update `NEXT_PUBLIC_API_URL` to your deployed backend URL.

## Troubleshooting

### CORS Issues
Ensure Flask CORS is enabled:
\`\`\`python
from flask_cors import CORS
CORS(app)
\`\`\`

### Database Connection
Check the DB_FILE_PATH in `backend/app.py` points to your SQLite file.

### API Not Connecting
1. Verify Flask server is running on port 5000
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Test endpoints with curl or Postman:
\`\`\`bash
curl http://127.0.0.1:5000/api/health
\`\`\`

## Features

- ✅ Personalized search based on user preferences
- ✅ NLP-powered aesthetic keyword matching
- ✅ Real-time filtering and pagination
- ✅ Responsive design matching provided screenshots
- ✅ Direct integration with your Python backend
- ✅ SQLite database querying
- ✅ Price range filtering
- ✅ Multi-brand support

## Tech Stack

**Frontend:**
- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui components

**Backend:**
- Flask
- SQLite
- Python NLP processing
- Flask-CORS

## Next Steps

1. Implement NLP keyword extraction in `backend/nlp.py`
2. Add user authentication (optional)
3. Expand database with more brands
4. Add product detail pages
5. Implement favorites/wishlist functionality
6. Add filtering by specific brands from homepage
