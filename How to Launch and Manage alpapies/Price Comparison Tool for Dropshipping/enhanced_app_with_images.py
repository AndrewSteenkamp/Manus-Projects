from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import random
import requests
from urllib.parse import quote

app = Flask(__name__)
CORS(app)

# Enhanced mock data with real product images and brand information
ENHANCED_PRODUCTS = {
    "iphone": [
        {
            "title": "Apple iPhone 15 Pro Max 256GB",
            "brand": "Apple",
            "model": "iPhone 15 Pro Max",
            "platform": "Amazon",
            "price": 1199.99,
            "total_cost": 1299.99,
            "rating": 4.8,
            "review_count": 2847,
            "location": "Ships to your location",
            "delivery_time": "2-3 days",
            "recommendation_level": "Highly Recommended",
            "savings_amount": 100.00,
            "affiliate_url": "https://amazon.com/iphone15pro",
            "product_image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png",
            "features": ["A17 Pro chip", "Titanium design", "Action Button", "USB-C"],
            "condition": "New",
            "warranty": "1 year Apple warranty",
            "seller_rating": 4.9,
            "free_shipping": True,
            "prime_eligible": True
        },
        {
            "title": "Apple iPhone 15 Pro Max 256GB - Unlocked",
            "brand": "Apple", 
            "model": "iPhone 15 Pro Max",
            "platform": "eBay",
            "price": 1149.99,
            "total_cost": 1199.99,
            "rating": 4.7,
            "review_count": 1523,
            "location": "California, USA",
            "delivery_time": "3-5 days",
            "recommendation_level": "Recommended",
            "savings_amount": 150.00,
            "affiliate_url": "https://ebay.com/iphone15pro",
            "product_image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png",
            "features": ["Factory Unlocked", "Original Box", "Fast Shipping"],
            "condition": "New",
            "warranty": "30-day return policy",
            "seller_rating": 4.8,
            "free_shipping": True,
            "prime_eligible": False
        },
        {
            "title": "iPhone 15 Pro Max 256GB - Natural Titanium",
            "brand": "Apple",
            "model": "iPhone 15 Pro Max", 
            "platform": "Best Buy",
            "price": 1199.99,
            "total_cost": 1279.99,
            "rating": 4.9,
            "review_count": 892,
            "location": "Best Buy Store",
            "delivery_time": "Same day pickup",
            "recommendation_level": "Highly Recommended",
            "savings_amount": 20.00,
            "affiliate_url": "https://bestbuy.com/iphone15pro",
            "product_image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png",
            "features": ["In-store pickup", "Geek Squad support", "Trade-in available"],
            "condition": "New",
            "warranty": "Apple warranty + Best Buy protection",
            "seller_rating": 4.9,
            "free_shipping": True,
            "prime_eligible": False
        }
    ],
    "laptop": [
        {
            "title": "MacBook Air 15-inch M3 Chip 8GB RAM 256GB SSD",
            "brand": "Apple",
            "model": "MacBook Air 15-inch",
            "platform": "Amazon",
            "price": 1299.99,
            "total_cost": 1399.99,
            "rating": 4.8,
            "review_count": 1247,
            "location": "Ships worldwide",
            "delivery_time": "2-4 days",
            "recommendation_level": "Highly Recommended",
            "savings_amount": 200.00,
            "affiliate_url": "https://amazon.com/macbook-air-15",
            "product_image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png",
            "features": ["M3 chip", "15.3-inch display", "18-hour battery", "1080p camera"],
            "condition": "New",
            "warranty": "1 year limited warranty",
            "seller_rating": 4.9,
            "free_shipping": True,
            "prime_eligible": True
        },
        {
            "title": "Dell XPS 13 Plus Intel i7 16GB RAM 512GB SSD",
            "brand": "Dell",
            "model": "XPS 13 Plus",
            "platform": "Dell Direct",
            "price": 1199.99,
            "total_cost": 1299.99,
            "rating": 4.6,
            "review_count": 892,
            "location": "Dell Warehouse",
            "delivery_time": "5-7 days",
            "recommendation_level": "Recommended",
            "savings_amount": 300.00,
            "affiliate_url": "https://dell.com/xps13plus",
            "product_image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Dell_Logo.svg/200px-Dell_Logo.svg.png",
            "features": ["12th Gen Intel i7", "13.4-inch OLED", "Windows 11 Pro", "Thunderbolt 4"],
            "condition": "New",
            "warranty": "1 year premium support",
            "seller_rating": 4.7,
            "free_shipping": True,
            "prime_eligible": False
        },
        {
            "title": "HP Spectre x360 14-inch 2-in-1 Laptop",
            "brand": "HP",
            "model": "Spectre x360 14",
            "platform": "HP Store",
            "price": 999.99,
            "total_cost": 1099.99,
            "rating": 4.5,
            "review_count": 634,
            "location": "HP Direct",
            "delivery_time": "3-5 days",
            "recommendation_level": "Good Option",
            "savings_amount": 400.00,
            "affiliate_url": "https://hp.com/spectre-x360",
            "product_image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/HP_logo_2012.svg/200px-HP_logo_2012.svg.png",
            "features": ["360° convertible", "Intel Evo platform", "Pen included", "Privacy camera"],
            "condition": "New",
            "warranty": "1 year limited warranty",
            "seller_rating": 4.6,
            "free_shipping": True,
            "prime_eligible": False
        }
    ],
    "headphones": [
        {
            "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
            "brand": "Sony",
            "model": "WH-1000XM5",
            "platform": "Amazon",
            "price": 349.99,
            "total_cost": 379.99,
            "rating": 4.7,
            "review_count": 3421,
            "location": "Ships globally",
            "delivery_time": "1-2 days",
            "recommendation_level": "Highly Recommended",
            "savings_amount": 50.00,
            "affiliate_url": "https://amazon.com/sony-wh1000xm5",
            "product_image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Sony_logo.svg/200px-Sony_logo.svg.png",
            "features": ["Industry-leading noise canceling", "30-hour battery", "Multipoint connection"],
            "condition": "New",
            "warranty": "1 year manufacturer warranty",
            "seller_rating": 4.8,
            "free_shipping": True,
            "prime_eligible": True
        },
        {
            "title": "Apple AirPods Pro (2nd Generation) with MagSafe Case",
            "brand": "Apple",
            "model": "AirPods Pro 2nd Gen",
            "platform": "Apple Store",
            "price": 249.99,
            "total_cost": 249.99,
            "rating": 4.8,
            "review_count": 2156,
            "location": "Apple Store",
            "delivery_time": "Same day pickup",
            "recommendation_level": "Highly Recommended",
            "savings_amount": 0.00,
            "affiliate_url": "https://apple.com/airpods-pro",
            "product_image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400&h=400&fit=crop",
            "brand_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png",
            "features": ["Active Noise Cancellation", "Spatial Audio", "MagSafe charging", "Sweat resistant"],
            "condition": "New",
            "warranty": "1 year limited warranty",
            "seller_rating": 4.9,
            "free_shipping": True,
            "prime_eligible": False
        }
    ]
}

ENHANCED_SERVICES = {
    "web development": [
        {
            "title": "Professional WordPress Website Development",
            "provider_name": "WebMaster Pro",
            "provider_image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            "platform": "Fiverr",
            "starting_price": 299,
            "provider_rating": 4.9,
            "review_count": 1247,
            "location": "United States",
            "delivery_time": "7 days",
            "recommendation_level": "Highly Recommended",
            "provider_level": "Level 2 Seller",
            "affiliate_url": "https://fiverr.com/webmaster-pro",
            "portfolio_images": [
                "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=300&h=200&fit=crop",
                "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=300&h=200&fit=crop"
            ],
            "skills": ["WordPress", "PHP", "JavaScript", "SEO"],
            "languages": ["English", "Spanish"],
            "response_time": "1 hour",
            "completion_rate": "98%",
            "packages": {
                "basic": {"price": 299, "delivery": "7 days", "features": ["5 pages", "Responsive design", "Basic SEO"]},
                "standard": {"price": 599, "delivery": "10 days", "features": ["10 pages", "Premium design", "Advanced SEO", "Contact forms"]},
                "premium": {"price": 999, "delivery": "14 days", "features": ["Unlimited pages", "E-commerce", "Premium plugins", "1 month support"]}
            }
        },
        {
            "title": "Custom React.js Web Application Development",
            "provider_name": "ReactDev Expert",
            "provider_image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
            "platform": "Upwork",
            "hourly_rate": 85,
            "provider_rating": 4.8,
            "review_count": 892,
            "location": "Canada",
            "response_time": "2 hours",
            "recommendation_level": "Recommended",
            "provider_level": "Top Rated Plus",
            "affiliate_url": "https://upwork.com/react-expert",
            "portfolio_images": [
                "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=300&h=200&fit=crop",
                "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=300&h=200&fit=crop"
            ],
            "skills": ["React.js", "Node.js", "TypeScript", "MongoDB"],
            "languages": ["English", "French"],
            "total_earned": "$125K+",
            "success_rate": "97%",
            "availability": "Available now"
        }
    ],
    "graphic design": [
        {
            "title": "Professional Logo Design & Brand Identity",
            "provider_name": "DesignMaster",
            "provider_image": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
            "platform": "Fiverr",
            "starting_price": 149,
            "provider_rating": 4.9,
            "review_count": 2341,
            "location": "United Kingdom",
            "delivery_time": "3 days",
            "recommendation_level": "Highly Recommended",
            "provider_level": "Top Rated Seller",
            "affiliate_url": "https://fiverr.com/design-master",
            "portfolio_images": [
                "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=300&h=200&fit=crop",
                "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop"
            ],
            "skills": ["Adobe Illustrator", "Photoshop", "Brand Strategy", "Typography"],
            "languages": ["English"],
            "response_time": "30 minutes",
            "completion_rate": "99%",
            "packages": {
                "basic": {"price": 149, "delivery": "3 days", "features": ["Logo design", "3 concepts", "2 revisions"]},
                "standard": {"price": 299, "delivery": "5 days", "features": ["Logo + business card", "5 concepts", "Unlimited revisions"]},
                "premium": {"price": 499, "delivery": "7 days", "features": ["Complete brand package", "Logo variations", "Brand guidelines"]}
            }
        }
    ]
}

def get_product_suggestions(query):
    """Get product suggestions based on query"""
    query_lower = query.lower()
    
    # Map common search terms to our product categories
    if any(term in query_lower for term in ['iphone', 'phone', 'mobile', 'smartphone']):
        return ENHANCED_PRODUCTS.get('iphone', [])
    elif any(term in query_lower for term in ['laptop', 'computer', 'macbook', 'pc']):
        return ENHANCED_PRODUCTS.get('laptop', [])
    elif any(term in query_lower for term in ['headphones', 'earbuds', 'airpods', 'audio']):
        return ENHANCED_PRODUCTS.get('headphones', [])
    else:
        # Return a mix of products for general searches
        all_products = []
        for category in ENHANCED_PRODUCTS.values():
            all_products.extend(category[:1])  # Take first item from each category
        return all_products

def get_service_suggestions(query):
    """Get service suggestions based on query"""
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['web', 'website', 'development', 'coding']):
        return ENHANCED_SERVICES.get('web development', [])
    elif any(term in query_lower for term in ['design', 'logo', 'graphic', 'branding']):
        return ENHANCED_SERVICES.get('graphic design', [])
    else:
        # Return a mix of services for general searches
        all_services = []
        for category in ENHANCED_SERVICES.values():
            all_services.extend(category[:1])
        return all_services

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "PricePulse Enhanced API is running!",
        "features": ["Product Images", "Brand Information", "Enhanced UI"],
        "timestamp": time.time()
    })

@app.route('/api/search', methods=['GET'])
def enhanced_search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'products')
    currency = request.args.get('currency', 'USD')
    
    # Simulate search delay for realism
    time.sleep(random.uniform(0.8, 1.5))
    
    if search_type == 'services':
        results = get_service_suggestions(query)
        total_key = 'total_services'
        results_key = 'services'
    else:
        results = get_product_suggestions(query)
        total_key = 'total_products'
        results_key = 'products'
    
    # Add some randomization to make it feel more real
    if results:
        # Shuffle results slightly
        results = results.copy()
        random.shuffle(results)
        
        # Add slight price variations
        for item in results:
            if 'price' in item:
                variation = random.uniform(0.95, 1.05)
                item['price'] = round(item['price'] * variation, 2)
                item['total_cost'] = round(item['total_cost'] * variation, 2)
    
    # Generate smart recommendations
    recommendations = []
    if results:
        # Best overall (highest rated)
        best_overall = max(results, key=lambda x: x.get('rating', x.get('provider_rating', 0)))
        recommendations.append(f"Best overall: {best_overall['title']} from {best_overall['platform']} - {best_overall['recommendation_level']}")
        
        # Best value (lowest price)
        if search_type == 'products':
            best_value = min(results, key=lambda x: x.get('total_cost', float('inf')))
            recommendations.append(f"Best value: {best_value['title']} from {best_value['platform']} at ${best_value['total_cost']}")
        else:
            best_value = min([r for r in results if 'starting_price' in r], 
                           key=lambda x: x.get('starting_price', float('inf')), default=None)
            if best_value:
                recommendations.append(f"Best value: {best_value['title']} from {best_value['platform']} starting at ${best_value['starting_price']}")
        
        # Fastest delivery
        fastest = min(results, key=lambda x: len(x.get('delivery_time', x.get('response_time', 'long'))))
        recommendations.append(f"Fastest delivery: {fastest['title']} from {fastest['platform']} - {fastest.get('delivery_time', fastest.get('response_time', 'Quick'))}")
    
    return jsonify({
        "query": query,
        total_key: len(results),
        "search_duration_seconds": round(random.uniform(1.2, 2.8), 2),
        "currency": currency,
        "recommendations": recommendations,
        results_key: results,
        "search_metadata": {
            "platforms_searched": len(set(item['platform'] for item in results)),
            "has_images": True,
            "has_brand_info": True,
            "enhanced_features": True
        },
        "timestamp": time.time()
    })

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    return jsonify({
        "platforms": [
            {"name": "Amazon", "status": "active", "trust_score": 95, "logo": "🛒"},
            {"name": "eBay", "status": "active", "trust_score": 88, "logo": "🏪"},
            {"name": "Best Buy", "status": "active", "trust_score": 92, "logo": "💻"},
            {"name": "Apple Store", "status": "active", "trust_score": 98, "logo": "🍎"},
            {"name": "Dell Direct", "status": "active", "trust_score": 89, "logo": "💼"},
            {"name": "HP Store", "status": "active", "trust_score": 87, "logo": "🖥️"},
            {"name": "Fiverr", "status": "active", "trust_score": 87, "logo": "💼"},
            {"name": "Upwork", "status": "active", "trust_score": 92, "logo": "👨‍💻"}
        ],
        "total_platforms": 8,
        "features": ["Real product images", "Brand information", "Enhanced search"]
    })

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get information about supported brands"""
    return jsonify({
        "featured_brands": [
            {"name": "Apple", "trust_score": 98, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/200px-Apple_logo_black.svg.png"},
            {"name": "Sony", "trust_score": 94, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Sony_logo.svg/200px-Sony_logo.svg.png"},
            {"name": "Dell", "trust_score": 89, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Dell_Logo.svg/200px-Dell_Logo.svg.png"},
            {"name": "HP", "trust_score": 87, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/HP_logo_2012.svg/200px-HP_logo_2012.svg.png"}
        ],
        "total_brands": 50
    })

if __name__ == '__main__':
    print("🚀 Starting PricePulse Enhanced Backend...")
    print("📡 API available at: http://localhost:5000")
    print("🖼️  Features: Product Images, Brand Info, Enhanced Search")
    print("🔍 Test: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
