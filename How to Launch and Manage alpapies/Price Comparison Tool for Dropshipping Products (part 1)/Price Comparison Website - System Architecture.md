# Price Comparison Website - System Architecture

## Technology Stack

### Backend
- **Framework**: Flask (Python 3.11)
- **Database**: MySQL 8.0 with Redis for caching
- **API**: RESTful API with JSON responses
- **Task Queue**: Celery with Redis broker
- **Web Server**: Gunicorn with Nginx reverse proxy

### Frontend
- **Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Tailwind CSS
- **Charts**: Chart.js for price history
- **HTTP Client**: Axios

### Infrastructure
- **Deployment**: Docker containers
- **Caching**: Redis for session and data caching
- **Search**: Elasticsearch for product search
- **Monitoring**: Application performance monitoring
- **CDN**: Static asset delivery

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────┤
│ Web Browser │ Mobile App │ Search Engines │ Price Bots      │
└─────────────┬───────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────┐
│                    CDN / LOAD BALANCER                      │
└─────────────┬───────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────┐
│                    WEB SERVER (Nginx)                       │
└─────────────┬───────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────┐
│                 APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│ │   React     │ │   Flask     │ │   Celery    │            │
│ │  Frontend   │ │   API       │ │ Background  │            │
│ │             │ │             │ │   Tasks     │            │
│ └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────┬───────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────┐
│                   DATA LAYER                                │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│ │   MySQL     │ │    Redis    │ │Elasticsearch│            │
│ │  Database   │ │   Cache     │ │   Search    │            │
│ └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────┬───────────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────┐
│                EXTERNAL SERVICES                            │
├─────────────────────────────────────────────────────────────┤
│ Amazon API │ Temu API │ Shein API │ Web Scrapers │ Email    │
└─────────────────────────────────────────────────────────────┘
```

## API Design

### Core Endpoints

#### Product Search
```
GET /api/v1/search
Parameters:
- q: search query (required)
- category: product category (optional)
- min_price: minimum price filter (optional)
- max_price: maximum price filter (optional)
- brands: comma-separated brand list (optional)
- sort: price_asc|price_desc|rating|popularity (optional)
- page: page number (default: 1)
- limit: results per page (default: 20)

Response:
{
  "products": [
    {
      "id": 12345,
      "name": "iPhone 15 Pro Max 256GB",
      "brand": "Apple",
      "category": "Electronics",
      "image_url": "https://...",
      "specifications": {...},
      "vendors": [
        {
          "vendor_id": 1,
          "vendor_name": "Amazon",
          "price": 1199.00,
          "original_price": 1199.00,
          "discount_percentage": 0,
          "affiliate_url": "https://...",
          "availability": "in_stock",
          "shipping_cost": 0,
          "rating": 4.8,
          "review_count": 1234
        }
      ],
      "best_price": 1089.00,
      "savings": 110.00
    }
  ],
  "total_results": 1234,
  "page": 1,
  "total_pages": 62
}
```

#### Product Details
```
GET /api/v1/products/{product_id}
Response:
{
  "id": 12345,
  "name": "iPhone 15 Pro Max 256GB",
  "description": "...",
  "brand": "Apple",
  "category": "Electronics",
  "specifications": {...},
  "images": ["url1", "url2"],
  "vendors": [...],
  "price_history": [
    {
      "date": "2025-08-01",
      "vendor_id": 1,
      "price": 1199.00
    }
  ],
  "reviews_summary": {
    "average_rating": 4.7,
    "total_reviews": 3456,
    "vendor_ratings": {...}
  }
}
```

#### Price Alerts
```
POST /api/v1/alerts
Body:
{
  "email": "user@example.com",
  "product_id": 12345,
  "target_price": 999.00
}

GET /api/v1/alerts/{email}
DELETE /api/v1/alerts/{alert_id}
```

#### Click Tracking
```
POST /api/v1/track/click
Body:
{
  "product_vendor_id": 67890,
  "session_id": "abc123",
  "user_agent": "...",
  "referrer": "..."
}
```

## Data Collection Architecture

### 1. API Integration (Preferred)
```python
class VendorAPIClient:
    def __init__(self, vendor_config):
        self.api_key = vendor_config['api_key']
        self.base_url = vendor_config['base_url']
        self.rate_limit = vendor_config['rate_limit']
    
    def search_products(self, query, filters=None):
        # Implement API calls with rate limiting
        pass
    
    def get_product_details(self, product_id):
        # Get detailed product information
        pass
```

### 2. Web Scraping (Fallback)
```python
class VendorScraper:
    def __init__(self, vendor_config):
        self.base_url = vendor_config['base_url']
        self.selectors = vendor_config['selectors']
        self.rate_limit = vendor_config['rate_limit']
    
    def scrape_search_results(self, query):
        # Implement respectful web scraping
        pass
    
    def scrape_product_page(self, product_url):
        # Extract product details from HTML
        pass
```

### 3. Background Tasks
```python
# Celery tasks for data collection
@celery.task
def update_product_prices():
    # Update prices for all products
    pass

@celery.task
def check_price_alerts():
    # Check if any price alerts should be triggered
    pass

@celery.task
def scrape_vendor_products(vendor_id, product_ids):
    # Scrape specific products from a vendor
    pass
```

## Caching Strategy

### Redis Cache Structure
```
# Product cache (TTL: 1 hour)
product:{product_id} -> JSON product data

# Search results cache (TTL: 30 minutes)
search:{query_hash} -> JSON search results

# Price cache (TTL: 15 minutes)
prices:{product_id} -> JSON price comparison data

# Vendor status cache (TTL: 5 minutes)
vendor:{vendor_id}:status -> availability status

# User session cache (TTL: 24 hours)
session:{session_id} -> JSON session data
```

### Cache Invalidation
- Product data: Invalidate when prices update
- Search results: Invalidate when new products added
- Price data: Invalidate on price changes
- Vendor status: Invalidate on API errors

## Security Considerations

### Data Protection
- Encrypt sensitive data (API keys, user emails)
- Use HTTPS for all communications
- Implement rate limiting to prevent abuse
- Sanitize all user inputs

### Affiliate Link Security
- Generate unique tracking tokens
- Validate affiliate URLs before redirecting
- Monitor for click fraud
- Implement session-based tracking

### Privacy Compliance
- GDPR compliance for EU users
- CCPA compliance for California users
- Clear privacy policy and cookie consent
- Data retention policies

## Performance Optimization

### Database Optimization
- Index frequently queried columns
- Use read replicas for search queries
- Implement database connection pooling
- Regular query performance monitoring

### Application Performance
- Implement response compression
- Use CDN for static assets
- Optimize image loading and sizing
- Implement lazy loading for search results

### Monitoring and Analytics
- Application performance monitoring (APM)
- Database query performance tracking
- User behavior analytics
- Error tracking and alerting

## Scalability Plan

### Horizontal Scaling
- Load balancer for multiple app instances
- Database sharding by product category
- Separate read/write database instances
- Microservices architecture for future growth

### Vertical Scaling
- Optimize database queries and indexes
- Implement efficient caching strategies
- Use async processing for heavy operations
- Regular performance profiling and optimization

## Deployment Architecture

### Docker Configuration
```dockerfile
# Flask API container
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# React frontend container
FROM node:18-alpine
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Docker Compose Setup
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql://...
      - REDIS_URL=redis://...
  
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=...
  
  redis:
    image: redis:7-alpine
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

