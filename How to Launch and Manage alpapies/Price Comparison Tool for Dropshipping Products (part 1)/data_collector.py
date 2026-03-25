import requests
import time
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

from src.models.product import (
    db, Product, Category, Vendor, ProductVendor, 
    PriceHistory, AffiliateProgram
)

class DataCollector:
    """Base class for collecting product data from various vendors"""
    
    def __init__(self, vendor_config: Dict):
        self.vendor_config = vendor_config
        self.vendor_name = vendor_config.get('name')
        self.base_url = vendor_config.get('base_url')
        self.rate_limit = vendor_config.get('rate_limit', 1)  # seconds between requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for products - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement search_products")
    
    def get_product_details(self, product_url: str) -> Dict:
        """Get detailed product information - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement get_product_details")
    
    def respect_rate_limit(self):
        """Respect rate limiting"""
        time.sleep(self.rate_limit)
    
    def clean_price(self, price_str: str) -> Optional[float]:
        """Extract numeric price from string"""
        if not price_str:
            return None
        
        # Remove currency symbols and extract numbers
        price_str = re.sub(r'[^\d.,]', '', str(price_str))
        price_str = price_str.replace(',', '')
        
        try:
            return float(price_str)
        except (ValueError, TypeError):
            return None
    
    def generate_product_hash(self, name: str, brand: str = None) -> str:
        """Generate a hash for product deduplication"""
        identifier = f"{name.lower().strip()}"
        if brand:
            identifier += f"_{brand.lower().strip()}"
        return hashlib.md5(identifier.encode()).hexdigest()

class AmazonCollector(DataCollector):
    """Collector for Amazon products (simulated - would need actual API)"""
    
    def __init__(self, vendor_config: Dict):
        super().__init__(vendor_config)
        self.api_key = vendor_config.get('api_key')
        self.associate_tag = vendor_config.get('associate_tag')
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """Simulate Amazon product search"""
        # In a real implementation, this would use Amazon Product Advertising API
        # For demo purposes, we'll return mock data
        
        mock_products = [
            {
                'name': f'iPhone 15 Pro Max 256GB - {query}',
                'brand': 'Apple',
                'price': 1199.00,
                'original_price': 1199.00,
                'image_url': 'https://example.com/iphone15.jpg',
                'product_url': 'https://amazon.com/iphone-15-pro-max',
                'availability': 'in_stock',
                'rating': 4.8,
                'review_count': 1234,
                'description': 'Latest iPhone with advanced features'
            },
            {
                'name': f'Samsung Galaxy S24 Ultra - {query}',
                'brand': 'Samsung',
                'price': 1099.00,
                'original_price': 1199.00,
                'image_url': 'https://example.com/galaxy-s24.jpg',
                'product_url': 'https://amazon.com/galaxy-s24-ultra',
                'availability': 'in_stock',
                'rating': 4.7,
                'review_count': 892,
                'description': 'Premium Android smartphone'
            }
        ]
        
        return mock_products[:limit]
    
    def get_product_details(self, product_url: str) -> Dict:
        """Get detailed Amazon product information"""
        # Mock implementation
        return {
            'specifications': {
                'display': '6.7-inch Super Retina XDR',
                'processor': 'A17 Pro chip',
                'storage': '256GB',
                'camera': 'Pro camera system'
            },
            'shipping_cost': 0,
            'shipping_time': '1-2 days'
        }

class TemuCollector(DataCollector):
    """Collector for Temu products"""
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """Search Temu products"""
        # Mock implementation - in reality would scrape or use API
        mock_products = [
            {
                'name': f'Wireless Earbuds - {query}',
                'brand': 'Generic',
                'price': 29.99,
                'original_price': 59.99,
                'image_url': 'https://example.com/earbuds.jpg',
                'product_url': 'https://temu.com/wireless-earbuds',
                'availability': 'in_stock',
                'rating': 4.2,
                'review_count': 567,
                'description': 'High-quality wireless earbuds'
            },
            {
                'name': f'Phone Case - {query}',
                'brand': 'Generic',
                'price': 9.99,
                'original_price': 19.99,
                'image_url': 'https://example.com/phone-case.jpg',
                'product_url': 'https://temu.com/phone-case',
                'availability': 'in_stock',
                'rating': 4.0,
                'review_count': 234,
                'description': 'Protective phone case'
            }
        ]
        
        return mock_products[:limit]

class SheinCollector(DataCollector):
    """Collector for Shein products"""
    
    def search_products(self, query: str, limit: int = 20) -> List[Dict]:
        """Search Shein products"""
        # Mock implementation
        mock_products = [
            {
                'name': f'Summer Dress - {query}',
                'brand': 'SHEIN',
                'price': 15.99,
                'original_price': 25.99,
                'image_url': 'https://example.com/dress.jpg',
                'product_url': 'https://shein.com/summer-dress',
                'availability': 'in_stock',
                'rating': 4.3,
                'review_count': 445,
                'description': 'Trendy summer dress'
            },
            {
                'name': f'Casual T-Shirt - {query}',
                'brand': 'SHEIN',
                'price': 8.99,
                'original_price': 12.99,
                'image_url': 'https://example.com/tshirt.jpg',
                'product_url': 'https://shein.com/casual-tshirt',
                'availability': 'in_stock',
                'rating': 4.1,
                'review_count': 678,
                'description': 'Comfortable casual t-shirt'
            }
        ]
        
        return mock_products[:limit]

class ProductDataManager:
    """Manages product data collection and storage"""
    
    def __init__(self):
        self.collectors = {}
        self.setup_collectors()
    
    def setup_collectors(self):
        """Initialize collectors for different vendors"""
        vendor_configs = [
            {
                'name': 'Amazon',
                'base_url': 'https://amazon.com',
                'rate_limit': 1,
                'collector_class': AmazonCollector
            },
            {
                'name': 'Temu',
                'base_url': 'https://temu.com',
                'rate_limit': 0.5,
                'collector_class': TemuCollector
            },
            {
                'name': 'Shein',
                'base_url': 'https://shein.com',
                'rate_limit': 0.5,
                'collector_class': SheinCollector
            }
        ]
        
        for config in vendor_configs:
            collector_class = config.pop('collector_class')
            self.collectors[config['name']] = collector_class(config)
    
    def search_all_vendors(self, query: str, limit_per_vendor: int = 10) -> Dict[str, List[Dict]]:
        """Search all vendors for products"""
        results = {}
        
        for vendor_name, collector in self.collectors.items():
            try:
                products = collector.search_products(query, limit_per_vendor)
                results[vendor_name] = products
                collector.respect_rate_limit()
            except Exception as e:
                print(f"Error searching {vendor_name}: {str(e)}")
                results[vendor_name] = []
        
        return results
    
    def save_products_to_db(self, search_results: Dict[str, List[Dict]], query: str):
        """Save search results to database"""
        try:
            # Get or create default category
            category = Category.query.filter_by(slug='general').first()
            if not category:
                category = Category(
                    name='General',
                    slug='general',
                    description='General products'
                )
                db.session.add(category)
                db.session.flush()
            
            for vendor_name, products in search_results.items():
                # Get or create vendor
                vendor = Vendor.query.filter_by(name=vendor_name).first()
                if not vendor:
                    vendor = Vendor(
                        name=vendor_name,
                        domain=self.collectors[vendor_name].base_url.replace('https://', ''),
                        is_active=True
                    )
                    db.session.add(vendor)
                    db.session.flush()
                
                for product_data in products:
                    # Check if product already exists (by name and brand)
                    existing_product = Product.query.filter(
                        Product.name == product_data['name'],
                        Product.brand == product_data.get('brand')
                    ).first()
                    
                    if not existing_product:
                        # Create new product
                        product = Product(
                            name=product_data['name'],
                            brand=product_data.get('brand'),
                            description=product_data.get('description'),
                            category_id=category.id,
                            image_url=product_data.get('image_url')
                        )
                        db.session.add(product)
                        db.session.flush()
                    else:
                        product = existing_product
                    
                    # Check if product-vendor relationship exists
                    existing_pv = ProductVendor.query.filter(
                        ProductVendor.product_id == product.id,
                        ProductVendor.vendor_id == vendor.id
                    ).first()
                    
                    if existing_pv:
                        # Update existing relationship
                        old_price = existing_pv.current_price
                        existing_pv.current_price = product_data['price']
                        existing_pv.original_price = product_data.get('original_price', product_data['price'])
                        existing_pv.product_url = product_data.get('product_url')
                        existing_pv.availability_status = product_data.get('availability', 'unknown')
                        existing_pv.last_updated = datetime.utcnow()
                        
                        # Calculate discount
                        if existing_pv.original_price and existing_pv.current_price:
                            discount = ((existing_pv.original_price - existing_pv.current_price) / existing_pv.original_price) * 100
                            existing_pv.discount_percentage = round(discount, 2)
                        
                        # Record price history if price changed
                        if old_price != existing_pv.current_price:
                            price_history = PriceHistory(
                                product_vendor_id=existing_pv.id,
                                price=existing_pv.current_price,
                                original_price=existing_pv.original_price,
                                discount_percentage=existing_pv.discount_percentage
                            )
                            db.session.add(price_history)
                    else:
                        # Create new product-vendor relationship
                        current_price = product_data['price']
                        original_price = product_data.get('original_price', current_price)
                        
                        discount_percentage = 0
                        if original_price and current_price and original_price > current_price:
                            discount_percentage = ((original_price - current_price) / original_price) * 100
                        
                        product_vendor = ProductVendor(
                            product_id=product.id,
                            vendor_id=vendor.id,
                            product_url=product_data.get('product_url'),
                            current_price=current_price,
                            original_price=original_price,
                            discount_percentage=round(discount_percentage, 2),
                            availability_status=product_data.get('availability', 'unknown'),
                            is_active=True
                        )
                        db.session.add(product_vendor)
                        db.session.flush()
                        
                        # Create initial price history record
                        price_history = PriceHistory(
                            product_vendor_id=product_vendor.id,
                            price=current_price,
                            original_price=original_price,
                            discount_percentage=product_vendor.discount_percentage
                        )
                        db.session.add(price_history)
            
            db.session.commit()
            print(f"Successfully saved products for query: {query}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error saving products to database: {str(e)}")
            raise
    
    def update_product_prices(self):
        """Update prices for all products"""
        try:
            # Get all active product-vendor relationships
            product_vendors = ProductVendor.query.filter(
                ProductVendor.is_active == True
            ).all()
            
            for pv in product_vendors:
                try:
                    # Get updated product details
                    collector = self.collectors.get(pv.vendor.name)
                    if collector and pv.product_url:
                        details = collector.get_product_details(pv.product_url)
                        
                        # Update price if available
                        if 'price' in details:
                            old_price = pv.current_price
                            pv.current_price = details['price']
                            pv.last_updated = datetime.utcnow()
                            
                            # Record price history if price changed
                            if old_price != pv.current_price:
                                price_history = PriceHistory(
                                    product_vendor_id=pv.id,
                                    price=pv.current_price,
                                    original_price=pv.original_price,
                                    discount_percentage=pv.discount_percentage
                                )
                                db.session.add(price_history)
                        
                        collector.respect_rate_limit()
                        
                except Exception as e:
                    print(f"Error updating p
(Content truncated due to size limit. Use page ranges or line ranges to read remaining content)