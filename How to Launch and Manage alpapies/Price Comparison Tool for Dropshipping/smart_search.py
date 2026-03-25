from flask import Blueprint, request, jsonify
from src.services.enhanced_price_collector import EnhancedPriceCollector
from src.services.smart_comparison_engine import smart_engine
from src.services.currency_service import currency_service
from src.services.fallback_currency_service import fallback_currency_service
from src.services.cost_calculator import cost_calculator, ProductInfo, ShippingInfo, ShippingMethod
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)

smart_search_bp = Blueprint('smart_search', __name__)

# Global instances
price_collector = EnhancedPriceCollector()

@smart_search_bp.route('/smart-search', methods=['GET'])
def smart_search():
    """
    Intelligent price search with advanced product matching and recommendations
    """
    try:
        start_time = time.time()
        
        # Get query parameters
        query = request.args.get('q', '').strip()
        user_currency = request.args.get('currency', 'USD').upper()
        user_country = request.args.get('country', 'US').upper()
        max_results = request.args.get('max_results', 5, type=int)
        include_shipping = request.args.get('include_shipping', 'true').lower() == 'true'
        include_taxes = request.args.get('include_taxes', 'true').lower() == 'true'
        
        # User preferences (optional)
        prefer_fast_delivery = request.args.get('prefer_fast_delivery', 'false').lower() == 'true'
        prefer_high_rating = request.args.get('prefer_high_rating', 'false').lower() == 'true'
        max_budget = request.args.get('max_budget', type=float)
        
        # Validate parameters
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters long'}), 400
        
        if max_results > 10:
            max_results = 10
        
        logger.info(f"Smart search for '{query}' in {user_currency} for {user_country}")
        
        # Step 1: Collect prices from all platforms
        search_results = price_collector.search_all_platforms(query, max_results)
        
        # Step 2: Process and enhance results with currency conversion and cost calculation
        enhanced_results = process_and_enhance_results(
            search_results, user_currency, user_country, include_shipping, include_taxes, query
        )
        
        # Step 3: Apply smart comparison and matching
        user_preferences = {
            'prefer_fast_delivery': prefer_fast_delivery,
            'prefer_high_rating': prefer_high_rating,
            'max_budget': max_budget,
            'currency': user_currency
        }
        
        comparison_result = smart_engine.compare_products(enhanced_results, query, user_preferences)
        
        # Step 4: Format response
        end_time = time.time()
        search_duration = round(end_time - start_time, 2)
        
        response = {
            'query': query,
            'user_currency': user_currency,
            'user_country': user_country,
            'search_duration_seconds': search_duration,
            'timestamp': datetime.now().isoformat(),
            
            # Smart comparison results
            'total_products': comparison_result.total_products,
            'matched_groups': format_matched_groups(comparison_result.matched_groups),
            'best_deals': format_best_deals(comparison_result.best_deals),
            'price_insights': comparison_result.price_insights,
            'recommendations': comparison_result.recommendations,
            'search_metadata': comparison_result.search_metadata,
            
            # Raw platform results (for debugging/advanced users)
            'raw_platform_results': enhanced_results if request.args.get('include_raw') == 'true' else None,
            
            # Settings used
            'settings': {
                'include_shipping': include_shipping,
                'include_taxes': include_taxes,
                'max_results_per_platform': max_results,
                'user_preferences': user_preferences
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in smart search: {str(e)}")
        return jsonify({
            'error': f'Smart search failed: {str(e)}',
            'query': request.args.get('q', ''),
            'timestamp': datetime.now().isoformat()
        }), 500

def process_and_enhance_results(search_results, user_currency, user_country, include_shipping, include_taxes, query):
    """Process raw search results with currency conversion and cost calculation"""
    enhanced_results = {}
    
    for platform, products in search_results.items():
        if not products:
            enhanced_results[platform] = []
            continue
        
        enhanced_products = []
        
        for product in products:
            try:
                enhanced_product = enhance_single_product(
                    product, user_currency, user_country, include_shipping, include_taxes, query
                )
                if enhanced_product:
                    enhanced_products.append(enhanced_product)
            except Exception as e:
                logger.warning(f"Error enhancing product from {platform}: {e}")
                # Include original product as fallback
                enhanced_products.append(product)
        
        enhanced_results[platform] = enhanced_products
    
    return enhanced_results

def enhance_single_product(product, user_currency, user_country, include_shipping, include_taxes, query):
    """Enhance a single product with currency conversion and cost calculation"""
    try:
        enhanced_product = product.copy()
        
        # Original price information
        original_price = product['price']
        original_currency = product.get('currency', 'USD')
        
        # Currency conversion
        if user_currency != original_currency:
            # Try primary currency service first
            conversion = currency_service.convert_currency(
                original_price, original_currency, user_currency
            )
            
            # If primary fails, try fallback service
            if not conversion:
                conversion = fallback_currency_service.convert_currency(
                    original_price, original_currency, user_currency
                )
            
            if conversion:
                enhanced_product['converted_price'] = conversion['converted_amount']
                enhanced_product['user_currency'] = user_currency
                enhanced_product['exchange_rate'] = conversion['exchange_rate']
                enhanced_product['conversion_date'] = conversion['conversion_date']
                enhanced_product['conversion_source'] = conversion.get('source', 'unknown')
            else:
                # Final fallback to original price
                enhanced_product['converted_price'] = original_price
                enhanced_product['user_currency'] = original_currency
                enhanced_product['exchange_rate'] = 1.0
                enhanced_product['conversion_source'] = 'no-conversion'
        else:
            enhanced_product['converted_price'] = original_price
            enhanced_product['user_currency'] = user_currency
            enhanced_product['exchange_rate'] = 1.0
            enhanced_product['conversion_source'] = 'same-currency'
        
        # Cost calculation (shipping, taxes, duties)
        if include_shipping or include_taxes:
            cost_breakdown = calculate_enhanced_costs(
                enhanced_product, user_country, include_shipping, include_taxes, query
            )
            enhanced_product['cost_breakdown'] = cost_breakdown
            enhanced_product['total_cost'] = cost_breakdown['total_cost']
        else:
            enhanced_product['total_cost'] = enhanced_product['converted_price']
        
        # Add additional metadata
        enhanced_product['delivery_estimate'] = get_delivery_estimate(
            product.get('platform'), user_country
        )
        enhanced_product['trust_score'] = calculate_trust_score(product)
        
        return enhanced_product
        
    except Exception as e:
        logger.error(f"Error enhancing single product: {e}")
        return product

def calculate_enhanced_costs(product, user_country, include_shipping, include_taxes, query):
    """Calculate enhanced costs with better categorization"""
    try:
        # Create product info for cost calculator
        product_info = ProductInfo(
            price=product['converted_price'],
            currency=product['user_currency'],
            category=categorize_product_enhanced(query, product['name']),
            weight=estimate_weight_enhanced(query, product['name']),
            origin_country=get_origin_country(product['platform'])
        )
        
        # Create shipping info
        shipping_info = ShippingInfo(
            destination_country=user_country,
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Calculate costs
        cost_breakdown = cost_calculator.calculate_total_cost(
            product_info, shipping_info, product['user_currency']
        )
        
        return {
            'base_price': cost_breakdown.base_price,
            'shipping_cost': cost_breakdown.shipping_cost if include_shipping else 0,
            'vat_amount': cost_breakdown.vat_amount if include_taxes else 0,
            'import_duty': cost_breakdown.import_duty if include_taxes else 0,
            'handling_fee': cost_breakdown.handling_fee if include_taxes else 0,
            'insurance_fee': cost_breakdown.insurance_fee if include_shipping else 0,
            'total_cost': (
                cost_breakdown.base_price + 
                (cost_breakdown.shipping_cost if include_shipping else 0) +
                (cost_breakdown.vat_amount if include_taxes else 0) +
                (cost_breakdown.import_duty if include_taxes else 0) +
                (cost_breakdown.handling_fee if include_taxes else 0) +
                (cost_breakdown.insurance_fee if include_shipping else 0)
            ),
            'currency': product['user_currency'],
            'breakdown_details': {
                'category_used': product_info.category,
                'estimated_weight': product_info.weight,
                'origin_country': product_info.origin_country
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating enhanced costs: {e}")
        return {
            'base_price': product['converted_price'],
            'shipping_cost': 0,
            'vat_amount': 0,
            'import_duty': 0,
            'handling_fee': 0,
            'insurance_fee': 0,
            'total_cost': product['converted_price'],
            'currency': product['user_currency']
        }

def categorize_product_enhanced(query, product_name):
    """Enhanced product categorization"""
    combined_text = f"{query} {product_name}".lower()
    
    # Electronics categories
    if any(word in combined_text for word in ['phone', 'iphone', 'android', 'smartphone', 'mobile']):
        return 'electronics'
    elif any(word in combined_text for word in ['laptop', 'computer', 'pc', 'macbook', 'notebook']):
        return 'electronics'
    elif any(word in combined_text for word in ['tablet', 'ipad']):
        return 'electronics'
    elif any(word in combined_text for word in ['headphones', 'earbuds', 'airpods', 'headset']):
        return 'electronics'
    elif any(word in combined_text for word in ['tv', 'television', 'monitor', 'display']):
        return 'electronics'
    elif any(word in combined_text for word in ['camera', 'lens', 'photography']):
        return 'electronics'
    elif any(word in combined_text for word in ['speaker', 'audio', 'sound', 'music']):
        return 'electronics'
    
    # Clothing categories
    elif any(word in combined_text for word in ['shirt', 'tshirt', 't-shirt', 'blouse', 'top']):
        return 'clothing'
    elif any(word in combined_text for word in ['dress', 'gown', 'skirt']):
        return 'clothing'
    elif any(word in combined_text for word in ['pants', 'jeans', 'trousers', 'shorts']):
        return 'clothing'
    elif any(word in combined_text for word in ['shoes', 'sneakers', 'boots', 'sandals']):
        return 'clothing'
    elif any(word in combined_text for word in ['jacket', 'coat', 'hoodie', 'sweater']):
        return 'clothing'
    
    # Books
    elif any(word in combined_text for word in ['book', 'novel', 'textbook', 'manual', 'guide']):
        return 'books'
    
    # Default
    else:
        return 'general'

def estimate_weight_enhanced(query, product_name):
    """Enhanced weight estimation"""
    combined_text = f"{query} {product_name}".lower()
    
    # Heavy electronics
    if any(word in combined_text for word in ['laptop', 'computer', 'pc', 'tv', 'television']):
        return 2.5  # kg
    elif any(word in combined_text for word in ['monitor', 'display']):
        return 3.0  # kg
    elif any(word in combined_text for word in ['tablet', 'ipad']):
        return 0.5  # kg
    elif any(word in combined_text for word in ['phone', 'smartphone']):
        return 0.2  # kg
    elif any(word in combined_text for word in ['headphones', 'headset']):
        return 0.3  # kg
    elif any(word in combined_text for word in ['earbuds', 'airpods']):
        return 0.1  # kg
    elif any(word in combined_text for word in ['speaker']):
        return 1.0  # kg
    elif any(word in combined_text for word in ['camera']):
        return 0.8  # kg
    
    # Clothing
    elif any(word in combined_text for word in ['shoes', 'boots']):
        return 0.8  # kg
    elif any(word in combined_text for word in ['jacket', 'coat']):
        return 0.6  # kg
    elif any(word in combined_text for word in ['shirt', 'dress', 'pants']):
        return 0.3  # kg
    
    # Books
    elif any(word in combined_text for word in ['book', 'textbook']):
        return 0.5  # kg
    
    # Default
    else:
        return 0.5  # kg

def get_origin_country(platform):
    """Get typical origin country for platform"""
    origin_map = {
        'Amazon': 'US',
        'eBay': 'US',
        'Walmart': 'US',
        'Best Buy': 'US',
        'AliExpress': 'CN',
        'Temu': 'CN',
        'Shein': 'CN'
    }
    return origin_map.get(platform, 'US')

def get_delivery_estimate(platform, user_country):
    """Get delivery time estimate"""
    if platform in ['Amazon', 'Walmart', 'Best Buy'] and user_country == 'US':
        return '2-5 business days'
    elif platform in ['Amazon', 'eBay'] and user_country in ['CA', 'GB', 'DE', 'FR']:
        return '5-10 business days'
    elif platform in ['AliExpress', 'Temu']:
        return '10-25 business days'
    elif platform == 'Shein':
        return '8-15 business days'
    else:
        return '7-14 business days'

def calculate_trust_score(product):
    """Calculate trust score for the product/platform"""
    score = 70  # Base score
    
    # Platform reputation
    platform_scores = {
        'Amazon': 95,
        'Best Buy': 90,
        'Walmart': 85,
        'eBay': 75,
        'AliExpress': 65,
        'Temu': 60,
        'Shein': 55
    }
    
    platform_score = platform_scores.get(product['platform'], 70)
    
    # Rating bonus
    if product.get('rating'):
        rating_bonus = (product['rating'] - 3.0) * 5  # Bonus for ratings above 3.0
        score += rating_bonus
    
    # Combine platform and rating scores
    final_score = (platform_score + score) / 2
    
    return min(100, max(0, round(final_score)))

def format_matched_groups(matched_groups):
    """Format matched groups for JSON response"""
    formatted_groups = []
    
    for i, group in enumerate(matched_groups):
        formatted_group = {
            'group_id': i + 1,
            'group_size': len(group),
            'products': []
        }
        
        for match in group:
            product_data = match.product.copy()
            product_data['similarity_score'] = match.similarity_score
            product_data['match_reasons'] = match.match_reasons
            product_data['confidence_level'] = match.confidence_level
            formatted_group['products'].append(product_data)
        
        formatted_groups.append(formatted_group)
    
    return formatted_groups

def format_best_deals(best_deals):
    """Format best deals for JSON response"""
    formatted_deals = []
    
    for i, deal in enumerate(best_deals):
        deal_data = deal.product.copy()
        deal_data['deal_rank'] = i + 1
        deal_data['similarity_score'] = deal.similarity_score
        deal_data['confidence_level'] = deal.confidence_level
        formatted_deals.append(deal_data)
    
    return formatted_deals

@smart_search_bp.route('/search-suggestions', methods=['GET'])
def search_suggestions():
    """Get search suggestions based on partial query"""
    try:
        partial_query = request.args.get('q', '').strip().lower()
        
        if len(partial_query) < 2:
            return jsonify({'suggestions': []})
        
        # Common product suggestions
        suggestions = []
        
        # Electronics suggestions
        if any(word in partial_query for word in ['iphone', 'phone', 'apple']):
            suggestions.extend(['iPhone 15', 'iPhone 15 Pro', 'iPhone 14', 'iPhone 13'])
        elif any(word in partial_query for word in ['samsung', 'galaxy']):
            suggestions.extend(['Samsung Galaxy S24', 'Samsung Galaxy S23', 'Samsung Galaxy Note'])
        elif any(word in partial_query for word in ['laptop', 'macbook']):
            suggestions.extend(['MacBook Pro', 'MacBook Air', 'Dell XPS', 'HP Pavilion'])
        elif any(word in partial_query for word in ['headphones', 'airpods']):
            suggestions.extend(['AirPods Pro', 'Sony WH-1000XM5', 'Bose QuietComfort', 'JBL Tune'])
        
        # General suggestions based on partial match
        common_searches = [
            'wireless headphones', 'bluetooth speaker', 'gaming mouse', 'mechanical keyboard',
            'running shoes', 'winter jacket', 'coffee maker', 'fitness tracker',
            'tablet case', 'phone charger', 'laptop bag', 'wireless earbuds'
        ]
        
        for search in common_searches:
            if partial_query in search.lower():
                suggestions.append(search)
        
        # Remove duplicates and limit
        suggestions = list(dict.fromkeys(suggestions))[:8]
        
        return jsonify({
            'suggestions': suggestions,
            'query': partial_query
        })
        
    except Exception as e:
        logger.error(f"Error getting search suggestions: {e}")
        return jsonify({'suggestions': [], 'error': str(e)})

@smart_search_bp.route('/compare', methods=['POST'])
def compare_specific_products():
    """Compare specific products by their URLs or IDs"""
    try:
        data = request.get_json()
        product_urls = data.get('product_urls', [])
        
        if not product_urls or len(product_urls) < 2:
            return jsonify({'error': 'At least 2 product URLs are required'}), 400
        
        # This would integrate with specific product scrapers
        # For now, return a placeholder response
        return jsonify({
            'message': 'Direct product comparison feature coming soon',
            'product_urls': product_urls,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in product comparison: {e}")
        return jsonify({'error': str(e)}), 500
