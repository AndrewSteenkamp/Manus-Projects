# Price Comparison Website - Database Schema Design

## Core Tables

### 1. Products Table
```sql
CREATE TABLE products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(100),
    model VARCHAR(100),
    category_id INT,
    image_url VARCHAR(500),
    specifications JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_brand (brand),
    INDEX idx_category (category_id)
);
```

### 2. Categories Table
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_id INT NULL,
    slug VARCHAR(100) UNIQUE,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);
```

### 3. Vendors Table
```sql
CREATE TABLE vendors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    domain VARCHAR(100) UNIQUE,
    logo_url VARCHAR(500),
    affiliate_program_id INT,
    base_commission_rate DECIMAL(5,2),
    cookie_duration_days INT DEFAULT 30,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_domain (domain)
);
```

### 4. Product_Vendors Table (Many-to-Many)
```sql
CREATE TABLE product_vendors (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT,
    vendor_id INT,
    vendor_product_id VARCHAR(100),
    product_url VARCHAR(1000),
    affiliate_url VARCHAR(1000),
    current_price DECIMAL(10,2),
    original_price DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    availability_status ENUM('in_stock', 'out_of_stock', 'limited_stock', 'unknown'),
    shipping_cost DECIMAL(8,2),
    shipping_time VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    INDEX idx_product_vendor (product_id, vendor_id),
    INDEX idx_price (current_price),
    INDEX idx_last_updated (last_updated)
);
```

### 5. Price_History Table
```sql
CREATE TABLE price_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_vendor_id BIGINT,
    price DECIMAL(10,2),
    original_price DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_vendor_id) REFERENCES product_vendors(id) ON DELETE CASCADE,
    INDEX idx_product_vendor_date (product_vendor_id, recorded_at),
    INDEX idx_recorded_at (recorded_at)
);
```

### 6. Affiliate_Programs Table
```sql
CREATE TABLE affiliate_programs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    network VARCHAR(100),
    commission_structure JSON, -- Store different commission rates by category
    tracking_domain VARCHAR(200),
    api_endpoint VARCHAR(500),
    api_key_encrypted VARCHAR(500),
    terms_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. User_Searches Table
```sql
CREATE TABLE user_searches (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(100),
    search_query VARCHAR(500),
    category_id INT,
    filters JSON, -- Store search filters (price range, brand, etc.)
    results_count INT,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_ip VARCHAR(45),
    user_agent TEXT,
    INDEX idx_search_query (search_query),
    INDEX idx_timestamp (search_timestamp)
);
```

### 8. Click_Tracking Table
```sql
CREATE TABLE click_tracking (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(100),
    product_vendor_id BIGINT,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_ip VARCHAR(45),
    user_agent TEXT,
    referrer_url VARCHAR(1000),
    conversion_tracked BOOLEAN DEFAULT FALSE,
    commission_earned DECIMAL(8,2),
    FOREIGN KEY (product_vendor_id) REFERENCES product_vendors(id),
    INDEX idx_session_product (session_id, product_vendor_id),
    INDEX idx_clicked_at (clicked_at)
);
```

### 9. Price_Alerts Table
```sql
CREATE TABLE price_alerts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255),
    product_id BIGINT,
    target_price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked TIMESTAMP,
    alert_sent_at TIMESTAMP NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_email (email),
    INDEX idx_product_active (product_id, is_active)
);
```

### 10. Product_Reviews Table
```sql
CREATE TABLE product_reviews (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT,
    vendor_id INT,
    rating DECIMAL(2,1), -- 1.0 to 5.0
    review_count INT,
    review_summary TEXT,
    source_url VARCHAR(1000),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    INDEX idx_product_rating (product_id, rating)
);
```

## Indexes and Performance Optimization

### Key Indexes for Fast Queries
- Product search: `idx_name`, `idx_brand`, `idx_category`
- Price comparison: `idx_product_vendor`, `idx_price`
- Analytics: `idx_clicked_at`, `idx_timestamp`
- Price history: `idx_product_vendor_date`

### Caching Strategy
- **Redis Cache Keys**:
  - `product:{id}` - Product details
  - `prices:{product_id}` - Current prices from all vendors
  - `search:{query_hash}` - Search results
  - `trending:{category}` - Trending products by category
  - `vendor:{id}:status` - Vendor availability status

## Data Relationships

1. **Products** have many **Categories** (hierarchical)
2. **Products** have many **Vendors** through **Product_Vendors**
3. **Product_Vendors** have many **Price_History** records
4. **Vendors** belong to **Affiliate_Programs**
5. **Users** can create **Price_Alerts** for **Products**
6. **Click_Tracking** records user interactions with **Product_Vendors**

## Scalability Considerations

### Partitioning Strategy
- **Price_History**: Partition by date (monthly partitions)
- **Click_Tracking**: Partition by date (weekly partitions)
- **User_Searches**: Partition by date (monthly partitions)

### Data Archival
- Archive price history older than 2 years
- Archive click tracking data older than 1 year
- Keep aggregated analytics data for historical reporting

### Read Replicas
- Use read replicas for:
  - Search queries
  - Price comparison displays
  - Analytics and reporting
  - Price history charts

