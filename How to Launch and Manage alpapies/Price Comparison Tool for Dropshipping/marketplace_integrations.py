"""
Marketplace Integration Service for PricePulse
Handles integration with multiple e-commerce platforms and marketplaces
"""

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import urljoin, quote
import time
import random

logger = logging.getLogger(__name__)

class MarketplaceType(Enum):
    AMAZON = "amazon"
    SHOPIFY = "shopify"
    EBAY = "ebay"
    FACEBOOK_MARKETPLACE = "facebook_marketplace"
    GUMTREE = "gumtree"
    TAKEALOT = "takealot"
    TEMU = "temu"
    SHEIN = "shein"
    ALIBABA = "alibaba"
    ETSY = "etsy"

@dataclass
class ProductListing:
    """Product listing from a marketplace"""
    title: str
    price: float
    currency: str
    marketplace: MarketplaceType
    url: str
    image_url: str = ""
    seller: str = ""
    rating: float = 0.0
    reviews_count: int = 0
    shipping_cost: float = 0.0
    availability: str = "in_stock"
    location: str = ""
    condition: str = "new"
    marketplace_id: str = ""

@dataclass
class SearchQuery:
    """Search query parameters"""
    keyword: str
    category: str = ""
    min_price: float = 0.0
    max_price: float = 0.0
    location: str = ""
    condition: str = ""
    sort_by: str = "relevance"  # relevance, price_low, price_high, rating

class MarketplaceIntegration:
    """Base class for marketplace integrations"""
    
    def __init__(self, marketplace_type: MarketplaceType):
        self.marketplace_type = marketplace_type
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search for products on the marketplace"""
        raise NotImplementedError("Subclasses must implement search_products")
    
    def get_product_details(self, product_id: str) -> Optional[ProductListing]:
        """Get detailed information about a specific product"""
        raise NotImplementedError("Subclasses must implement get_product_details")

class AmazonIntegration(MarketplaceIntegration):
    """Amazon marketplace integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.AMAZON)
        self.base_url = "https://www.amazon.com"
        self.search_url = "/s"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Amazon for products"""
        try:
            self._rate_limit()
            
            params = {
                'k': query.keyword,
                'ref': 'sr_pg_1'
            }
            
            if query.category:
                params['i'] = query.category
            
            # Note: This is a simplified implementation
            # In production, you would use Amazon's Product Advertising API
            # or a proper web scraping solution with legal compliance
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Amazon")
            
        except Exception as e:
            logger.error(f"Error searching Amazon: {e}")
            return []

class ShopifyIntegration(MarketplaceIntegration):
    """Shopify stores integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.SHOPIFY)
        self.shopify_stores = [
            "allbirds.com",
            "gymshark.com",
            "colourpop.com",
            "mvmt.com",
            "bombas.com"
        ]
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search across multiple Shopify stores"""
        all_listings = []
        
        for store in self.shopify_stores:
            try:
                listings = self._search_shopify_store(store, query)
                all_listings.extend(listings)
            except Exception as e:
                logger.error(f"Error searching Shopify store {store}: {e}")
                continue
        
        return all_listings
    
    def _search_shopify_store(self, store_domain: str, query: SearchQuery) -> List[ProductListing]:
        """Search a specific Shopify store"""
        try:
            self._rate_limit()
            
            # Use Shopify's search API endpoint
            search_url = f"https://{store_domain}/search/suggest.json"
            params = {
                'q': query.keyword,
                'resources[type]': 'product',
                'resources[limit]': 10
            }
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, f"Shopify ({store_domain})")
            
        except Exception as e:
            logger.error(f"Error searching Shopify store {store_domain}: {e}")
            return []

class EbayIntegration(MarketplaceIntegration):
    """eBay marketplace integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.EBAY)
        self.base_url = "https://www.ebay.com"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search eBay for products"""
        try:
            self._rate_limit()
            
            # Note: In production, use eBay's Finding API
            # This is a simplified mock implementation
            return self._generate_mock_listings(query, "eBay")
            
        except Exception as e:
            logger.error(f"Error searching eBay: {e}")
            return []

class TakealotIntegration(MarketplaceIntegration):
    """Takealot (South African marketplace) integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.TAKEALOT)
        self.base_url = "https://www.takealot.com"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Takealot for products"""
        try:
            self._rate_limit()
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Takealot")
            
        except Exception as e:
            logger.error(f"Error searching Takealot: {e}")
            return []

class FacebookMarketplaceIntegration(MarketplaceIntegration):
    """Facebook Marketplace integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.FACEBOOK_MARKETPLACE)
        self.base_url = "https://www.facebook.com/marketplace"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Facebook Marketplace for products"""
        try:
            self._rate_limit()
            
            # Note: Facebook Marketplace requires special handling due to login requirements
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Facebook Marketplace")
            
        except Exception as e:
            logger.error(f"Error searching Facebook Marketplace: {e}")
            return []

class GumtreeIntegration(MarketplaceIntegration):
    """Gumtree integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.GUMTREE)
        self.base_url = "https://www.gumtree.co.za"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Gumtree for products"""
        try:
            self._rate_limit()
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Gumtree")
            
        except Exception as e:
            logger.error(f"Error searching Gumtree: {e}")
            return []

class TemuIntegration(MarketplaceIntegration):
    """Temu marketplace integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.TEMU)
        self.base_url = "https://www.temu.com"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Temu for products"""
        try:
            self._rate_limit()
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Temu")
            
        except Exception as e:
            logger.error(f"Error searching Temu: {e}")
            return []

class SheinIntegration(MarketplaceIntegration):
    """Shein marketplace integration"""
    
    def __init__(self):
        super().__init__(MarketplaceType.SHEIN)
        self.base_url = "https://www.shein.com"
    
    def search_products(self, query: SearchQuery) -> List[ProductListing]:
        """Search Shein for products"""
        try:
            self._rate_limit()
            
            # For demo purposes, return mock data
            return self._generate_mock_listings(query, "Shein")
            
        except Exception as e:
            logger.error(f"Error searching Shein: {e}")
            return []

class MarketplaceAggregator:
    """Aggregates search results from multiple marketplaces"""
    
    def __init__(self):
        self.integrations = {
            MarketplaceType.AMAZON: AmazonIntegration(),
            MarketplaceType.SHOPIFY: ShopifyIntegration(),
            MarketplaceType.EBAY: EbayIntegration(),
            MarketplaceType.TAKEALOT: TakealotIntegration(),
            MarketplaceType.FACEBOOK_MARKETPLACE: FacebookMarketplaceIntegration(),
            MarketplaceType.GUMTREE: GumtreeIntegration(),
            MarketplaceType.TEMU: TemuIntegration(),
            MarketplaceType.SHEIN: SheinIntegration()
        }
        self.user_suggested_sites = []
    
    def search_all_marketplaces(self, query: SearchQuery, 
                              marketplaces: Optional[List[MarketplaceType]] = None) -> Dict[str, List[ProductListing]]:
        """Search across all or specified marketplaces"""
        
        if marketplaces is None:
            marketplaces = list(self.integrations.keys())
        
        results = {}
        
        for marketplace_type in marketplaces:
            if marketplace_type in self.integrations:
                try:
                    integration = self.integrations[marketplace_type]
                    listings = integration.search_products(query)
                    results[marketplace_type.value] = listings
                    logger.info(f"Found {len(listings)} products on {marketplace_type.value}")
                except Exception as e:
                    logger.error(f"Error searching {marketplace_type.value}: {e}")
                    results[marketplace_type.value] = []
        
        return results
    
    def get_best_deals(self, query: SearchQuery, limit: int = 10) -> List[ProductListing]:
        """Get the best deals across all marketplaces"""
        all_results = self.search_all_marketplaces(query)
        
        # Flatten all results
        all_listings = []
        for marketplace_listings in all_results.values():
            all_listings.extend(marketplace_listings)
        
        # Sort by price (ascending)
        all_listings.sort(key=lambda x: x.price)
        
        return all_listings[:limit]
    
    def add_user_suggested_site(self, site_info: Dict[str, str]) -> bool:
        """Add a user-suggested site to the search"""
        try:
            required_fields = ['name', 'url', 'search_pattern']
            if not all(field in site_info for field in required_fields):
                return False
            
            self.user_suggested_sites.append(site_info)
            logger.info(f"Added user-suggested site: {site_info['name']}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding user-suggested site: {e}")
            return False
    
    def get_supported_marketplaces(self) -> List[Dict[str, str]]:
        """Get list of supported marketplaces"""
        marketplaces = []
        
        for marketplace_type in self.integrations.keys():
            marketplaces.append({
                'id': marketplace_type.value,
                'name': marketplace_type.value.replace('_', ' ').title(),
                'status': 'active'
            })
        
        # Add user-suggested sites
        for site in self.user_suggested_sites:
            marketplaces.append({
                'id': site['name'].lower().replace(' ', '_'),
                'name': site['name'],
                'status': 'user_suggested'
            })
        
        return marketplaces
    
    def _generate_mock_listings(self, query: SearchQuery, marketplace: str) -> List[ProductListing]:
        """Generate mock product listings for demonstration"""
        listings = []
        
        # Generate 3-8 mock listings per marketplace
        num_listings = random.randint(3, 8)
        
        for i in range(num_listings):
            # Generate realistic price variations
            base_price = random.uniform(10, 500)
            
            # Add marketplace-specific price adjustments
            if "Amazon" in marketplace:
                price_multiplier = random.uniform(0.9, 1.2)
            elif "Temu" in marketplace or "Shein" in marketplace:
                price_multiplier = random.uniform(0.3, 0.8)  # Generally cheaper
            elif "Takealot" in marketplace:
                price_multiplier = random.uniform(1.1, 1.4)  # Local premium
            else:
                price_multiplier = random.uniform(0.8, 1.3)
            
            final_price = base_price * price_multiplier
            
            listing = ProductListing(
                title=f"{query.keyword} - {marketplace} Product {i+1}",
                price=round(final_price, 2),
                currency="USD",
                marketplace=MarketplaceType(marketplace.lower().replace(' ', '_').replace('(', '').replace(')', '').split('.')[0]),
                url=f"https://example.com/{marketplace.lower()}/product/{i+1}",
                image_url=f"https://via.placeholder.com/300x300?text={marketplace}+Product",
                seller=f"{marketplace} Seller {i+1}",
                rating=round(random.uniform(3.5, 5.0), 1),
                reviews_count=random.randint(10, 1000),
                shipping_cost=round(random.uniform(0, 25), 2),
                availability="in_stock" if random.random() > 0.1 else "limited_stock",
                location=random.choice(["US", "CN", "UK", "DE", "ZA"]),
                condition=random.choice(["new", "used", "refurbished"]),
                marketplace_id=f"{marketplace.lower()}_{i+1}"
            )
            listings.append(listing)
        
        return listings

# Global marketplace aggregator instance
marketplace_aggregator = MarketplaceAggregator()

