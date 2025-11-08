# Backend Architecture

## Overview

The backend follows a **modular, layered architecture** with clear separation of concerns:

\`\`\`
┌─────────────────────────────────────────┐
│          Routers (API Layer)            │  ← HTTP endpoints
├─────────────────────────────────────────┤
│        Services (Business Logic)        │  ← Core functionality
├─────────────────────────────────────────┤
│      Database (Data Access Layer)       │  ← Data operations
└─────────────────────────────────────────┘
\`\`\`

## Layer Responsibilities

### 1. Routers (`routers/`)
**Purpose:** Handle HTTP requests and responses

- Parse query parameters and request body
- Validate inputs
- Call appropriate service methods
- Format responses
- Handle HTTP errors

**Files:**
- `health_router.py` - System health checks
- `search_router.py` - Product search with NLP
- `product_router.py` - Individual product operations

### 2. Services (`services/`)
**Purpose:** Implement business logic

- Orchestrate data operations
- Apply business rules
- Transform data between layers
- Integrate external APIs (OpenAI)

**Files:**
- `nlp_service.py` - OpenAI integration for aesthetic parsing
- `product_service.py` - Product search and filtering logic

### 3. Database (`database/`)
**Purpose:** Data persistence and retrieval

- Execute SQL queries
- Manage database connections
- Transform raw data to/from models
- Handle database transactions

**Files:**
- `db_manager.py` - SQLite operations
- `models.py` - Data models and schemas

## Data Flow

### Search Request Flow

\`\`\`
1. User Request
   ↓
2. search_router.py
   - Receives GET /api/search
   - Extracts query parameters
   ↓
3. nlp_service.py
   - Sends aesthetic to OpenAI
   - Parses structured recommendations
   - Extracts search keywords
   ↓
4. product_service.py
   - Applies filters (price, size, brand)
   - Calls database layer
   ↓
5. db_manager.py
   - Builds SQL query
   - Executes search
   - Returns product records
   ↓
6. Response sent back through layers
   - Database → Service → Router → Client
\`\`\`

## Key Design Patterns

### 1. **Dependency Injection**
Services receive dependencies through constructors:

\`\`\`python
class ProductService:
    def __init__(self):
        self.db = DatabaseManager()
\`\`\`

### 2. **Factory Pattern**
Application created through factory:

\`\`\`python
def create_app():
    app = Flask(__name__)
    # Configure and register blueprints
    return app
\`\`\`

### 3. **Repository Pattern**
Database layer abstracts data access:

\`\`\`python
class DatabaseManager:
    def search_products(self, filters):
        # Build and execute query
\`\`\`

### 4. **Service Layer Pattern**
Business logic separated from routes:

\`\`\`python
# Router just coordinates
@bp.route('/api/search')
def search():
    result = product_service.search_products(...)
    return jsonify(result)
\`\`\`

## Configuration Management

Centralized in `config.py`:

\`\`\`python
class Config:
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
\`\`\`

Benefits:
- Single source of truth
- Easy to test with different configs
- Environment-specific settings

## Error Handling

**Layered approach:**

1. **Database layer** - Catches SQL errors
2. **Service layer** - Handles business logic errors
3. **Router layer** - Converts to HTTP responses

\`\`\`python
try:
    products = product_service.search(...)
    return jsonify(products)
except Exception as e:
    logger.error(f"Search failed: {str(e)}")
    return jsonify({'error': str(e)}), 500
\`\`\`

## Testing Strategy

Each layer can be tested independently:

\`\`\`python
# Test service without database
def test_product_service():
    mock_db = MockDatabase()
    service = ProductService(mock_db)
    result = service.search_products(...)
    assert result['total'] > 0
\`\`\`

## Extending the System

### Adding a New Endpoint

1. **Create router function** (`routers/`)
   \`\`\`python
   @bp.route('/api/new-endpoint')
   def new_endpoint():
       result = service.new_operation()
       return jsonify(result)
   \`\`\`

2. **Add service method** (`services/`)
   \`\`\`python
   def new_operation(self):
       data = self.db.query_data()
       return self.process(data)
   \`\`\`

3. **Add database method** (`database/`)
   \`\`\`python
   def query_data(self):
       cursor.execute("SELECT ...")
       return cursor.fetchall()
   \`\`\`

### Adding a New Integration

1. Create new service file (`services/new_integration_service.py`)
2. Add configuration to `config.py`
3. Use in routers as needed

## Performance Considerations

- **Connection pooling**: SQLite connections created per request
- **Caching**: Can add Redis/memory cache at service layer
- **Pagination**: Implemented at database layer with LIMIT/OFFSET
- **Indexing**: Add indexes to frequently queried columns

## Security

- **Input validation**: Query parameters validated in routers
- **SQL injection**: Parameterized queries in database layer
- **CORS**: Configured globally in main.py
- **API keys**: Stored in environment variables

## Future Enhancements

1. **Add caching layer** between service and database
2. **Implement rate limiting** in routers
3. **Add request/response validation** with Pydantic
4. **Use async/await** for external API calls
5. **Add comprehensive logging** middleware
