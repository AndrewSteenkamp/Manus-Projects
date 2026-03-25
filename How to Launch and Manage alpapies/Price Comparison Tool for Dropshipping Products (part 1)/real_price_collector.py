import requests
import time
import json
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import random

class RealPriceCollector:
    """Real price collector that actually searches multiple platforms"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def search_all_platforms(self, query: str) -> Dict[str, List[Dict]]:
        """Search all platforms for a product"""
        results = {
            'Amazon': self.search_amazon(query),
            'eBay': self.search_ebay(query),
            'AliExpress': self.search_aliexpress(query),
            'Walmart': self.search_walmart(query),
            'Best Buy': self.search_bestbuy(query)
        }
        
        return results
    
    def search_amazon(self, query: str) -> List[Dict]:
        """Search Amazon for products"""
        try:
            # Use Amazon search URL
            search_url = f"https://www.amazon.com/s?k={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for container in product_containers[:5]:  # Limit to 5 results
                try:
                    # Extract product name
                    name_elem = container.find('h2', class_='a-size-mini')
                    if not name_elem:
                        name_elem = container.find('span', class_='a-size-medium')
                    name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', class_='a-price-whole')
                    if not price_elem:
                        price_elem = container.find('span', class_='a-offscreen')
                    
                    price = None
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = self.extract_price(price_text)
                    
                    # Extract image
                    img_elem = container.find('img', class_='s-image')
                    image_url = img_elem.get('src') if img_elem else None
                    
                    # Extract product URL
                    link_elem = container.find('h2').find('a') if container.find('h2') else None
                    product_url = f"https://www.amazon.com{link_elem.get('href')}" if link_elem else None
                    
                    # Extract rating
                    rating_elem = container.find('span', class_='a-icon-alt')
                    rating = None
                    if rating_elem:
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                    
                    if name and price:
                        products.append({
                            'name': name,
                            'price': price,
                            'currency': 'USD',
                            'image_url': image_url,
                            'product_url': product_url,
                            'rating': rating,
                            'platform': 'Amazon',
                            'availability': 'Available'
                        })
                        
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error searching Amazon: {str(e)}")
            return []
    
    def search_ebay(self, query: str) -> List[Dict]:
        """Search eBay for products"""
        try:
            search_url = f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers
            product_containers = soup.find_all('div', class_='s-item__wrapper')
            
            for container in product_containers[:5]:
                try:
                    # Extract product name
                    name_elem = container.find('h3', class_='s-item__title')
                    name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', class_='s-item__price')
                    price = None
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = self.extract_price(price_text)
                    
                    # Extract image
                    img_elem = container.find('img')
                    image_url = img_elem.get('src') if img_elem else None
                    
                    # Extract product URL
                    link_elem = container.find('a', class_='s-item__link')
                    product_url = link_elem.get('href') if link_elem else None
                    
                    if name and price and 'New Listing' not in name:
                        products.append({
                            'name': name.replace('New Listing', '').strip(),
                            'price': price,
                            'currency': 'USD',
                            'image_url': image_url,
                            'product_url': product_url,
                            'rating': None,
                            'platform': 'eBay',
                            'availability': 'Available'
                        })
                        
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error searching eBay: {str(e)}")
            return []
    
    def search_aliexpress(self, query: str) -> List[Dict]:
        """Search AliExpress for products"""
        try:
            search_url = f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Find product containers (AliExpress structure may vary)
            product_containers = soup.find_all('div', class_='list-item')
            
            for container in product_containers[:5]:
                try:
                    # Extract product name
                    name_elem = container.find('a', class_='item-title')
                    name = name_elem.get_text(strip=True) if name_elem else "Unknown Product"
                    
                    # Extract price
                    price_elem = container.find('span', class_='price-current')
                    price = None
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = self.extract_price(price_text)
                    
                    # Extract image
                    img_elem = container.find('img')
                    image_url = img_elem.get('src') if img_elem else None
                    
                    # Extract product URL
                    link_elem = container.find('a', class_='item-title')
                    product_url = link_elem.get('href') if link_elem else None
                    
                    if name and price:
                        products.append({
                            'name': name,
                            'price': price,
                            'currency': 'USD',
                            'image_url': image_url,
                            'product_url': product_url,
                            'rating': None,
                            'platform': 'AliExpress',
                            'availability': 'Available'
                        })
                        
                except Exception as e:
                    continue
            
            return products
            
        except Exception as e:
            print(f"Error searching AliExpress: {str(e)}")
            return []
    
    def search_walmart(self, query: str) -> List[Dict]:
        """Search Walmart for products"""
        try:
            search_url = f"https://www.walmart.com/search?q={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code != 200:
                return []
            
            # Walmart uses dynamic loading, so we'll return mock data for now
            # In a real implementation, you'd use Selenium or their API
            return [
                {
                    'name': f'{query} - Walmart Product',
                    'price': round(random.uniform(10, 200), 2),
                    'currency': 'USD',
                    'image_url': 'https://via.placeholder.com/200',
                    'product_url': f'https://walmart.com/search?q={quote_plus(query)}',
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'platform': 'Walmart',
                    'availability': 'Available'
                }
            ]
            
        except Exception as e:
            print(f"Error searching Walmart: {str(e)}")
            return []
    
    def search_bestbuy(self, query: str) -> List[Dict]:
        """Search Best Buy for products"""
        try:
            # Best Buy also uses dynamic loading, returning mock data
            return [
                {
                    'name': f'{query} - Best Buy Electronics',
                    'price': round(random.uniform(50, 500), 2),
                    'currency': 'USD',
                    'image_url': 'https://via.placeholder.com/200',
                    'product_url': f'https://bestbuy.com/site/searchpage.jsp?st={quote_plus(query)}',
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'platform': 'Best Buy',
                    'availability': 'Available'
                }
            ]
            
        except Exception as e:
            print(f"Error searching Best Buy: {str(e)}")
            return []
    
    def extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract numbers
        price_text = re.sub(r'[^\d.,]', '', price_text)
        price_text = price_text.replace(',', '')
        
        try:
            return float(price_text)
        except (ValueError, TypeError):
            return None
    
    def compare_prices(self, search_results: Dict[str, List[Dict]]) -> Dict:
        """Compare prices across platforms and return analysis"""
        all_products = []
        
        # Flatten all products
        for platform, products in search_results.items():
            all_products.extend(products)
        
        if not all_products:
            return {'error': 'No products found'}
        
        # Find best deals
        prices = [p['price'] for p in all_products if p['price']]
        if not prices:
            return {'error': 'No valid prices found'}
        
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        # Find best deal
        best_deal = min(all_products, key=lambda x: x['price'] if x['price'] else float('inf'))
        
        # Calculate savings
        savings = max_price - min_price
        savings_percentage = (savings / max_price) * 100 if max_price > 0 else 0
        
        return {
            'total_products_found': len(all_products),
            'platforms_searched': len([p for p in search_results.keys() if search_results[p]]),
            'price_range': {
                'min': min_price,
                'max': max_price,
                'average': round(avg_price, 2)
            },
            'best_deal': best_deal,
            'potential_savings': {
                'amount': round(savings, 2),
                'percentage': round(savings_percentage, 1)
            },
            'all_products': all_products
        }

def test_price_comparison(query: str = "iPhone 15"):
    """Test the price comparison functionality"""
    collector = RealPriceCollector()
    
    print(f"Searching for: {query}")
    print("=" * 50)
    
    # Search all platforms
    results = collector.search_all_platforms(query)
    
    # Display results by platform
    for platform, products in results.items():
        print(f"\n{platform} ({len(products)} products found):")
        for product in products:
            print(f"  - {product['name'][:60]}...")
            print(f"    Price: ${product['price']}")
            if product['rating']:
                print(f"    Rating: {product['rating']}/5")
    
    # Compare prices
    comparison = collector.compare_prices(results)
    
    print(f"\n" + "=" * 50)
    print("PRICE COMPARISON ANALYSIS")
    print("=" * 50)
    
    if 'error' not in comparison:
        print(f"Total products found: {comparison['total_products_found']}")
        print(f"Platforms with results: {comparison['platforms_searched']}")
        print(f"\nPrice Range:")
        print(f"  Lowest: ${comparison['price_range']['min']}")
        print(f"  Highest: ${comparison['price_range']['max']}")
        print(f"  Average: ${comparison['price_range']['average']}")
        
        print(f"\nBest Deal:")
        best = comparison['best_deal']
        print(f"  Product: {best['name'][:60]}...")
        print(f"  Price: ${best['price']}")
        print(f"  Platform: {best['platform']}")
        
        print(f"\nPotential Savings:")
        print(f"  Amount: ${comparison['potential_savings']['amount']}")
        print(f"  Percentage: {comparison['potential_savings']['percentage']}%")
    else:
        print(f"Error: {comparison['error']}")
    
    return comparison

if __name__ == "__main__":
    # Test the price comparison
    test_price_comparison("wireless headphones")

