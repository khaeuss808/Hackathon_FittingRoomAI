# Backend Integration Guide

## Quick Start

Your frontend is now fully integrated with your Flask backend. Here's what's connected:

### API Endpoints Used

1. **Health Check**: `GET /api/health`
   - Used by: Shop page to verify backend connection
   - Response: `{ "ok": true }`

2. **Browse Products**: `GET /api/zara`
   - Used by: Shop page when no search filters applied
   - Query params: `page`, `per_page`
   - Response: `{ page, per_page, total, results: [...] }`

3. **Search Products**: `POST /api/search`
   - Used by: Shop page with user filters
   - Body: `{ styles: [...], min_price, max_price, page, per_page }`
   - Response: `{ page, per_page, total, results: [...] }`

## How User Flow Works

\`\`\`
User enters "clean girl aesthetic" on homepage
          ↓
Frontend sends to /shop page with query params
          ↓
Shop page calls POST /api/search with:
  {
    "styles": ["clean girl aesthetic"],
    "min_price": 0,
    "max_price": 200,
    "page": 1,
    "per_page": 20
  }
          ↓
Your Flask backend (app.py) receives request
          ↓
Backend queries SQLite database with filters:
  - LOWER(styles) LIKE '%clean girl aesthetic%'
  - price >= 0 AND price <= 200
          ↓
Results returned to frontend
          ↓
Shop page displays products in grid
\`\`\`

## Adding NLP Processing

Currently, the search passes user input directly to your backend. To add LLM/NLP processing:

### Option 1: Backend Processing (Recommended)

Modify `backend/app.py`:

\`\`\`python
from nlp import extract_keywords  # Your NLP module

@app.post("/api/search")
def traditional_search():
    filters = request.get_json(silent=True) or {}
    
    # Process user aesthetic input with NLP
    if filters.get("styles") and len(filters["styles"]) > 0:
        raw_input = filters["styles"][0]  # "clean girl aesthetic"
        processed_keywords = extract_keywords(raw_input)  # ["minimal", "neutral", "simple"]
        filters["styles"] = processed_keywords
    
    # Continue with existing search logic...
\`\`\`

### Option 2: Frontend Pre-processing

Add an API route in Next.js to process before sending to Flask:

\`\`\`typescript
// app/api/process-aesthetic/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { aesthetic } = await request.json()
  
  // Call your LLM/NLP service
  const keywords = await processWithNLP(aesthetic)
  
  return NextResponse.json({ keywords })
}
\`\`\`

Then update shop page to call this first.

## Environment Variables

### Required for Frontend

Create `.env.local`:
\`\`\`env
NEXT_PUBLIC_API_URL=http://127.0.0.1:5000
\`\`\`

### Required for Backend

If you add external LLM/NLP services, add to backend `.env`:
\`\`\`env
OPENAI_API_KEY=your_key_here
# or
ANTHROPIC_API_KEY=your_key_here
\`\`\`

## Testing the Integration

### 1. Start Backend
\`\`\`bash
cd backend
python app.py
\`\`\`
Should see: `🚀 Starting Fitting Room API...`

### 2. Test Health Endpoint
\`\`\`bash
curl http://127.0.0.1:5000/api/health
\`\`\`
Should return: `{"ok":true}`

### 3. Test Search Endpoint
\`\`\`bash
curl -X POST http://127.0.0.1:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"styles":["modern","casual"],"min_price":0,"max_price":100}'
\`\`\`
Should return products matching those styles.

### 4. Start Frontend
\`\`\`bash
npm run dev
\`\`\`
Visit `http://localhost:3000`

### 5. Test Full Flow
1. Go to homepage
2. Enter preferences (size, aesthetic, price)
3. Click "Find My Perfect Fit"
4. Verify you see products on /shop page
5. Check browser console for any errors

## Common Issues

### Issue: Products not showing
**Check:**
- Is Flask running? (`python app.py`)
- Does `/api/health` return `{"ok": true}`?
- Check browser console for CORS errors
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### Issue: CORS errors
**Fix:** Ensure Flask has CORS enabled:
\`\`\`python
from flask_cors import CORS
CORS(app)
\`\`\`

### Issue: No search results
**Check:**
- Your database has data in `styles` column
- Style keywords match database values
- Price range includes products in DB
- Try browsing all products first (visit `/shop` directly)

## Database Requirements

Your `zara_data` table must have these columns:
\`\`\`sql
CREATE TABLE zara_data (
  id INTEGER PRIMARY KEY,
  name TEXT,           -- or product_name
  brand TEXT,
  price REAL,          -- or price_raw
  image_url TEXT,      -- or image
  product_url TEXT,    -- or url
  category TEXT,
  styles TEXT,         -- REQUIRED for search functionality
  availability TEXT
);
\`\`\`

The `styles` column should contain comma-separated keywords like:
\`\`\`
"minimalist, modern, casual, neutral"
\`\`\`

## Extending the Integration

### Add Size Filtering
Update `backend/app.py` to accept size filters:
\`\`\`python
if filters.get("sizes"):
    sizes = filters["sizes"]  # ["2", "4", "6"]
    # Add size filtering logic based on your database schema
\`\`\`

### Add Brand Filtering
\`\`\`python
if filters.get("brands"):
    brands = filters["brands"]
    ors = " OR ".join(["brand = ?"] * len(brands))
    query += f" AND ({ors})"
    params.extend(brands)
\`\`\`

### Add Favorite Brands
Store user preferences and prioritize results from favorite brands.

## Next Steps

1. ✅ Frontend is connected to your Flask API
2. ✅ Search flow is implemented
3. ⏳ Add your NLP processing to `backend/nlp.py`
4. ⏳ Populate database with more products
5. ⏳ Add size/brand filtering to backend
6. ⏳ Deploy both frontend and backend

Everything is ready for you to add your NLP keyword extraction logic!
