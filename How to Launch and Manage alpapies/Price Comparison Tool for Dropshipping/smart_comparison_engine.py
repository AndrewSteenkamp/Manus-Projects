"""
Smart Comparison Engine for PricePulse
Advanced algorithms for product matching, ranking, and intelligent price comparison
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
from difflib import SequenceMatcher
import math

logger = logging.getLogger(__name__)

@dataclass
class ProductMatch:
    """Represents a matched product with similarity score"""
    product: Dict
    similarity_score: float
    match_reasons: List[str]
    confidence_level: str  # 'high', 'medium', 'low'

@dataclass
class ComparisonResult:
    """Complete comparison result with rankings and insights"""
    query: str
    total_products: int
    matched_groups: List[List[ProductMatch]]
    best_deals: List[ProductMatch]
    price_insights: Dict
    recommendations: List[str]
    search_metadata: Dict

class SmartComparisonEngine:
    """Advanced price comparison engine with intelligent matching"""
    
    def __init__(self):
        self.brand_keywords = self._load_brand_keywords()
        self.category_keywords = self._load_category_keywords()
        self.quality_indicators = self._load_quality_indicators()
        
    def compare_products(self, search_results: Dict[str, List[Dict]], query: str, 
                        user_preferences: Dict = None) -> ComparisonResult:
        """
        Perform intelligent product comparison with advanced matching
        """
        try:
            # Flatten and normalize all products
            all_products = self._flatten_and_normalize_products(search_results)
            
            if not all_products:
                return self._empty_comparison_result(query)
            
            # Apply intelligent product matching
            matched_groups = self._group_similar_products(all_products, query)
            
            # Rank products within each group
            ranked_groups = self._rank_product_groups(matched_groups, user_preferences or {})
            
            # Find best deals across all groups
            best_deals = self._find_best_deals(ranked_groups)
            
            # Generate price insights
            price_insights = self._generate_price_insights(all_products, ranked_groups)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(ranked_groups, price_insights, query)
            
            # Create search metadata
            search_metadata = self._create_search_metadata(search_results, all_products)
            
            return ComparisonResult(
                query=query,
                total_products=len(all_products),
                matched_groups=ranked_groups,
                best_deals=best_deals,
                price_insights=price_insights,
                recommendations=recommendations,
                search_metadata=search_metadata
            )
            
        except Exception as e:
            logger.error(f"Error in smart comparison: {e}")
            return self._empty_comparison_result(query)
    
    def _flatten_and_normalize_products(self, search_results: Dict[str, List[Dict]]) -> List[Dict]:
        """Flatten and normalize product data from all platforms"""
        all_products = []
        
        for platform, products in search_results.items():
            for product in products:
                normalized_product = self._normalize_product(product)
                if normalized_product:
                    all_products.append(normalized_product)
        
        return all_products
    
    def _normalize_product(self, product: Dict) -> Optional[Dict]:
        """Normalize product data for consistent comparison"""
        try:
            # Extract key information
            name = product.get('name', '').strip()
            if not name:
                return None
            
            # Normalize name for comparison
            normalized_name = self._normalize_product_name(name)
            
            # Extract brand
            brand = self._extract_brand(name)
            
            # Extract model/version
            model = self._extract_model(name)
            
            # Extract key features
            features = self._extract_features(name)
            
            # Calculate total cost (use total_cost if available, otherwise converted_price)
            total_cost = product.get('total_cost') or product.get('converted_price') or product.get('price', 0)
            
            return {
                'original_data': product,
                'normalized_name': normalized_name,
                'display_name': name,
                'brand': brand,
                'model': model,
                'features': features,
                'total_cost': total_cost,
                'currency': product.get('user_currency') or product.get('currency', 'USD'),
                'platform': product.get('platform', 'Unknown'),
                'rating': product.get('rating'),
                'availability': product.get('availability', 'Unknown'),
                'delivery_estimate': product.get('delivery_estimate', 'Unknown'),
                'trust_score': product.get('trust_score', 50),
                'image_url': product.get('image_url'),
                'product_url': product.get('product_url')
            }
            
        except Exception as e:
            logger.warning(f"Error normalizing product: {e}")
            return None
    
    def _normalize_product_name(self, name: str) -> str:
        """Normalize product name for comparison"""
        # Convert to lowercase
        normalized = name.lower()
        
        # Remove common noise words
        noise_words = ['new', 'original', 'genuine', 'authentic', 'official', 'brand', 'hot', 'sale']
        for word in noise_words:
            normalized = re.sub(rf'\b{word}\b', '', normalized)
        
        # Remove special characters but keep spaces and alphanumeric
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        
        # Normalize whitespace
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def _extract_brand(self, name: str) -> Optional[str]:
        """Extract brand from product name"""
        name_lower = name.lower()
        
        for brand in self.brand_keywords:
            if brand.lower() in name_lower:
                return brand
        
        # Try to extract brand from beginning of name
        words = name.split()
        if words:
            first_word = words[0].lower()
            if len(first_word) > 2 and first_word.isalpha():
                return words[0]
        
        return None
    
    def _extract_model(self, name: str) -> Optional[str]:
        """Extract model/version from product name"""
        # Look for common model patterns
        patterns = [
            r'\b(\w+\s?\d+\w*)\b',  # iPhone 15, Galaxy S23, etc.
            r'\b(v\d+\.?\d*)\b',    # v2.0, v3, etc.
            r'\b(gen\s?\d+)\b',     # gen 3, gen2, etc.
            r'\b(\d+\w+)\b'         # 15pro, 128gb, etc.
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, name, re.IGNORECASE)
            if matches:
                return matches[0]
        
        return None
    
    def _extract_features(self, name: str) -> List[str]:
        """Extract key features from product name"""
        features = []
        name_lower = name.lower()
        
        # Storage capacity
        storage_match = re.search(r'(\d+)\s*(gb|tb)', name_lower)
        if storage_match:
            features.append(f"{storage_match.group(1)}{storage_match.group(2).upper()}")
        
        # Color
        colors = ['black', 'white', 'red', 'blue', 'green', 'gold', 'silver', 'pink', 'purple']
        for color in colors:
            if color in name_lower:
                features.append(color.title())
        
        # Wireless/Bluetooth
        if any(word in name_lower for word in ['wireless', 'bluetooth', 'bt']):
            features.append('Wireless')
        
        # Size indicators
        size_match = re.search(r'(\d+\.?\d*)\s*(inch|"|mm)', name_lower)
        if size_match:
            features.append(f"{size_match.group(1)}{size_match.group(2)}")
        
        return features
    
    def _group_similar_products(self, products: List[Dict], query: str) -> List[List[ProductMatch]]:
        """Group similar products together using intelligent matching"""
        groups = []
        used_products = set()
        
        for i, product in enumerate(products):
            if i in used_products:
                continue
            
            # Start a new group with this product
            group = [ProductMatch(
                product=product,
                similarity_score=1.0,
                match_reasons=['Original product'],
                confidence_level='high'
            )]
            used_products.add(i)
            
            # Find similar products
            for j, other_product in enumerate(products):
                if j in used_products or i == j:
                    continue
                
                similarity_score, match_reasons = self._calculate_similarity(product, other_product, query)
                
                if similarity_score >= 0.6:  # Threshold for grouping
                    confidence_level = self._determine_confidence_level(similarity_score)
                    group.append(ProductMatch(
                        product=other_product,
                        similarity_score=similarity_score,
                        match_reasons=match_reasons,
                        confidence_level=confidence_level
                    ))
                    used_products.add(j)
            
            groups.append(group)
        
        # Sort groups by size (larger groups first)
        groups.sort(key=len, reverse=True)
        
        return groups
    
    def _calculate_similarity(self, product1: Dict, product2: Dict, query: str) -> Tuple[float, List[str]]:
        """Calculate similarity score between two products"""
        scores = []
        reasons = []
        
        # Name similarity
        name_sim = SequenceMatcher(None, product1['normalized_name'], product2['normalized_name']).ratio()
        scores.append(name_sim * 0.4)  # 40% weight
        if name_sim > 0.7:
            reasons.append(f"Similar names ({name_sim:.2f})")
        
        # Brand similarity
        if product1['brand'] and product2['brand']:
            if product1['brand'].lower() == product2['brand'].lower():
                scores.append(0.3)  # 30% weight
                reasons.append("Same brand")
            else:
                scores.append(0.0)
        else:
            scores.append(0.1)  # Neutral if brand unknown
        
        # Model similarity
        if product1['model'] and product2['model']:
            model_sim = SequenceMatcher(None, product1['model'].lower(), product2['model'].lower()).ratio()
            scores.append(model_sim * 0.2)  # 20% weight
            if model_sim > 0.8:
                reasons.append(f"Similar models ({model_sim:.2f})")
        else:
            scores.append(0.05)
        
        # Feature overlap
        features1 = set(f.lower() for f in product1['features'])
        features2 = set(f.lower() for f in product2['features'])
        if features1 and features2:
            feature_overlap = len(features1.intersection(features2)) / len(features1.union(features2))
            scores.append(feature_overlap * 0.1)  # 10% weight
            if feature_overlap > 0.5:
                reasons.append(f"Shared features ({feature_overlap:.2f})")
        else:
            scores.append(0.05)
        
        total_score = sum(scores)
        return total_score, reasons
    
    def _determine_confidence_level(self, similarity_score: float) -> str:
        """Determine confidence level based on similarity score"""
        if similarity_score >= 0.8:
            return 'high'
        elif similarity_score >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _rank_product_groups(self, groups: List[List[ProductMatch]], preferences: Dict) -> List[List[ProductMatch]]:
        """Rank products within each group based on multiple factors"""
        for group in groups:
            for match in group:
                match.product['ranking_score'] = self._calculate_ranking_score(match.product, preferences)
            
            # Sort by ranking score (higher is better)
            group.sort(key=lambda x: x.product['ranking_score'], reverse=True)
        
        return groups
    
    def _calculate_ranking_score(self, product: Dict, preferences: Dict) -> float:
        """Calculate ranking score for a product"""
        score = 0.0
        
        # Price factor (lower price is better, but not the only factor)
        total_cost = product['total_cost']
        if total_cost > 0:
            # Normalize price score (inverse relationship)
            price_score = 1.0 / (1.0 + total_cost / 100)  # Adjust denominator as needed
            score += price_score * 0.3  # 30% weight
        
        # Trust score factor
        trust_score = product.get('trust_score', 50) / 100.0
        score += trust_score * 0.25  # 25% weight
        
        # Rating factor
        rating = product.get('rating')
        if rating:
            rating_score = rating / 5.0
            score += rating_score * 0.2  # 20% weight
        
        # Availability factor
        if product.get('availability') == 'Available':
            score += 0.1  # 10% weight
        
        # Delivery speed factor
        delivery = product.get('delivery_estimate', '')
        if 'day' in delivery.lower():
            try:
                days = int(re.search(r'(\d+)', delivery).group(1))
                delivery_score = max(0, 1.0 - days / 30)  # Faster delivery is better
                score += delivery_score * 0.15  # 15% weight
            except:
                pass
        
        return score
    
    def _find_best_deals(self, groups: List[List[ProductMatch]]) -> List[ProductMatch]:
        """Find the best deals across all groups"""
        all_matches = []
        for group in groups:
            all_matches.extend(group)
        
        # Sort by total cost (ascending)
        all_matches.sort(key=lambda x: x.product['total_cost'])
        
        # Return top 5 best deals
        return all_matches[:5]
    
    def _generate_price_insights(self, all_products: List[Dict], groups: List[List[ProductMatch]]) -> Dict:
        """Generate insights about pricing patterns"""
        if not all_products:
            return {}
        
        costs = [p['total_cost'] for p in all_products if p['total_cost'] > 0]
        if not costs:
            return {}
        
        # Basic statistics
        min_price = min(costs)
        max_price = max(costs)
        avg_price = sum(costs) / len(costs)
        median_price = sorted(costs)[len(costs) // 2]
        
        # Platform analysis
        platform_stats = {}
        for product in all_products:
            platform = product['platform']
            if platform not in platform_stats:
                platform_stats[platform] = {'prices': [], 'count': 0}
            platform_stats[platform]['prices'].append(product['total_cost'])
            platform_stats[platform]['count'] += 1
        
        # Calculate platform averages
        for platform, stats in platform_stats.items():
            if stats['prices']:
                stats['avg_price'] = sum(stats['prices']) / len(stats['prices'])
                stats['min_price'] = min(stats['prices'])
                stats['max_price'] = max(stats['prices'])
        
        # Find cheapest and most expensive platforms
        cheapest_platform = min(platform_stats.items(), key=lambda x: x[1].get('avg_price', float('inf')))
        most_expensive_platform = max(platform_stats.items(), key=lambda x: x[1].get('avg_price', 0))
        
        return {
            'price_range': {
                'min': round(min_price, 2),
                'max': round(max_price, 2),
                'average': round(avg_price, 2),
                'median': round(median_price, 2)
            },
            'savings_potential': {
                'max_savings': round(max_price - min_price, 2),
                'percentage_savings': round((max_price - min_price) / max_price * 100, 1) if max_price > 0 else 0
            },
            'platform_analysis': platform_stats,
            'cheapest_platform': cheapest_platform[0] if cheapest_platform else None,
            'most_expensive_platform': most_expensive_platform[0] if most_expensive_platform else None,
            'total_products_analyzed': len(all_products),
            'unique_groups': len(groups)
        }
    
    def _generate_recommendations(self, groups: List[List[ProductMatch]], insights: Dict, query: str) -> List[str]:
        """Generate intelligent recommendations for the user"""
        recommendations = []
        
        if not groups:
            return ["No products found for your search. Try different keywords."]
        
        # Best value recommendation
        if groups and groups[0]:
            best_product = groups[0][0].product
            recommendations.append(
                f"Best overall value: {best_product['display_name'][:50]}... "
                f"from {best_product['platform']} at {best_product['currency']}{best_product['total_cost']:.2f}"
            )
        
        # Savings recommendation
        savings_potential = insights.get('savings_potential', {})
        if savings_potential.get('max_savings', 0) > 10:
            recommendations.append(
                f"You could save up to {insights['price_range']['max'] - insights['price_range']['min']:.2f} "
                f"({savings_potential['percentage_savings']:.1f}%) by choosing the cheapest option"
            )
        
        # Platform recommendation
        cheapest_platform = insights.get('cheapest_platform')
        if cheapest_platform:
            recommendations.append(f"{cheapest_platform} generally offers the best prices for this search")
        
        # Quality vs price recommendation
        high_rated_products = []
        for group in groups:
            for match in group:
                rating = match.product.get('rating')
                if rating and rating >= 4.5:
                    high_rated_products.append(match.product)
        
        if high_rated_products:
            best_rated = min(high_rated_products, key=lambda x: x['total_cost'])
            recommendations.append(
                f"Best rated option: {best_rated['display_name'][:50]}... "
                f"({best_rated['rating']}/5 stars) for {best_rated['currency']}{best_rated['total_cost']:.2f}"
            )
        
        # Delivery recommendation
        fast_delivery_products = []
        for group in groups:
            for match in group:
                delivery = match.product.get('delivery_estimate', '')
                if 'day' in delivery.lower():
                    try:
                        days = int(re.search(r'(\d+)', delivery).group(1))
                        if days <= 5:
                            fast_delivery_products.append(match.product)
                    except:
                        pass
        
        if fast_delivery_products:
            fastest_cheap = min(fast_delivery_products, key=lambda x: x['total_cost'])
            recommendations.append(
                f"Fastest delivery: {fastest_cheap['display_name'][:50]}... "
                f"arrives in {fastest_cheap['delivery_estimate']} for {fastest_cheap['currency']}{fastest_cheap['total_cost']:.2f}"
            )
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _create_search_metadata(self, search_results: Dict, all_products: List[Dict]) -> Dict:
        """Create metadata about the search"""
        return {
            'platforms_searched': len(search_results),
            'platforms_with_results': len([p for p in search_results.values() if p]),
            'total_products_found': len(all_products),
            'search_timestamp': datetime.now().isoformat(),
            'currencies_found': list(set(p['currency'] for p in all_products)),
            'brands_found': list(set(p['brand'] for p in all_products if p['brand'])),
            'platforms_with_products': list(set(p['platform'] for p in all_products))
        }
    
    def _empty_comparison_result(self, query: str) -> ComparisonResult:
        """Return empty comparison result"""
        return ComparisonResult(
            query=query,
            total_products=0,
            matched_groups=[],
            best_deals=[],
            price_insights={},
            recommendations=["No products found for your search. Try different keywords."],
            search_metadata={'search_timestamp': datetime.now().isoformat()}
        )
    
    def _load_brand_keywords(self) -> List[str]:
        """Load common brand keywords"""
        return [
            'Apple', 'Samsung', 'Google', 'Microsoft', 'Sony', 'LG', 'Huawei', 'Xiaomi',
            'OnePlus', 'Nokia', 'Motorola', 'Oppo', 'Vivo', 'Realme', 'Honor',
            'Nike', 'Adidas', 'Puma', 'Under Armour', 'Reebok', 'New Balance',
            'Canon', 'Nikon', 'Fujifilm', 'Olympus', 'Panasonic', 'GoPro',
            'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Alienware',
            'Intel', 'AMD', 'Nvidia', 'Corsair', 'Logitech', 'Razer',
            'Bose', 'JBL', 'Sennheiser', 'Audio-Technica', 'Beats', 'AirPods'
        ]
    
    def _load_category_keywords(self) -> Dict[str, List[str]]:
        """Load category-specific keywords"""
        return {
            'electronics': ['phone', 'laptop', 'tablet', 'headphones', 'speaker', 'camera', 'tv'],
            'clothing': ['shirt', 'dress', 'pants', 'shoes', 'jacket', 'sweater', 'jeans'],
            'home': ['furniture', 'decor', 'kitchen', 'bedroom', 'bathroom', 'garden'],
            'sports': ['fitness', 'gym', 'running', 'cycling', 'swimming', 'outdoor'],
            'books': ['book', 'novel', 'textbook', 'manual', 'guide', 'reference']
        }
    
    def _load_quality_indicators(self) -> List[str]:
        """Load quality indicator keywords"""
        return [
            'premium', 'professional', 'pro', 'plus', 'max', 'ultra', 'deluxe',
            'certified', 'original', 'authentic', 'genuine', 'official'
        ]

# Global smart comparison engine instance
smart_engine = SmartComparisonEngine()

def test_smart_comparison():
    """Test the smart comparison engine"""
    # Mock search results for testing
    mock_results = {
        'Amazon': [
            {'name': 'Apple iPhone 15 Pro 128GB Black', 'price': 999, 'currency': 'USD', 'platform': 'Amazon', 'rating': 4.5},
            {'name': 'Samsung Galaxy S23 Ultra 256GB', 'price': 1199, 'currency': 'USD', 'platform': 'Amazon', 'rating': 4.3}
        ],
        'eBay': [
            {'name': 'iPhone 15 Pro 128GB Space Black', 'price': 949, 'currency': 'USD', 'platform': 'eBay', 'rating': 4.2},
            {'name': 'Apple AirPods Pro 2nd Gen', 'price': 199, 'currency': 'USD', 'platform': 'eBay', 'rating': 4.6}
        ]
    }
    
    engine = SmartComparisonEngine()
    result = engine.compare_products(mock_results, "iPhone 15 Pro")
    
    print("Smart Comparison Test Results")
    print("=" * 40)
    print(f"Query: {result.query}")
    print(f"Total products: {result.total_products}")
    print(f"Matched groups: {len(result.matched_groups)}")
    print(f"Best deals: {len(result.best_deals)}")
    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")
    
    return result

if __name__ == "__main__":
    test_smart_comparison()
