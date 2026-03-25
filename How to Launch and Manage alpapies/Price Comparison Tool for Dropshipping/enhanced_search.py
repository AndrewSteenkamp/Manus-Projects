from flask import Blueprint, request, jsonify
from src.services.enhanced_price_collector import EnhancedPriceCollector
from src.services.currency_service import currency_service
from src.services.fallback_currency_service import fallback_currency_service
from src.services.cost_calculator import cost_calculator, ProductInfo, ShippingInfo, ShippingMethod
from datetime import datetime
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

logger = logging.getLogger(__name__)

enhanced_search_bp = Blueprint('enhanced_search', __name__)

# Global instances
price_collector = EnhancedPriceCollector()
executor = ThreadPoolExecutor(max_workers=4)

@enhanced_search_bp.route('/live-search', methods=['GET'])
def live_search():
    """
    Live price search across multiple platforms with currency conversion and cost calculation
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
        
        # Validate parameters
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters long'}), 400
        
        if max_results > 10:
            max_results = 10  # Limit to prevent abuse
        
        logger.info(f"Live search for '{query}' in {user_currency} for {user_country}")
        
        # Search all platforms
        search_results = price_collector.search_all_platforms(query, max_results)
        
        # Process and enhance results
        enhanced_results = process_search_results(
            search_results, 
            user_currency, 
            user_country, 
            include_shipping, 
            include_taxes,
            query
        )
        
        # Calculate performance metrics
        end_time = time.time()
        search_duration = round(end_time - start_time, 2)
        
        return jsonify({
            'query': query,
            'user_currency': user_currency,
            'user_country': user_country,
            'search_duration_seconds': search_duration,
            'timestamp': datetime.now().isoformat(),
            'results': enhanced_results,
            'summary': generate_search_summary(enhanced_results),
            'settings': {
                'include_shipping': include_shipping,
                'include_taxes': include_taxes,
                'max_results_per_platform': max_results
            }
        })
        
    except Exception as e:
        logger.error(f"Error in live search: {str(e)}")
        return jsonify({
            'error': f'Search failed: {str(e)}',
            'query': request.args.get('q', ''),
            'timestamp': datetime.now().isoformat()
        }), 500

def process_search_results(search_results, user_currency, user_country, include_shipping, include_taxes, query):
    """Process raw search results with currency conversion and cost calculation"""
    enhanced_results = {}
    
    for platform, products in search_results.items():
        if not products:
            enhanced_results[platform] = {
                'products': [],
                'platform_stats': {
                    'product_count': 0,
                    'avg_price': 0,
                    'min_price': None,
                    'max_price': None
                }
            }
            continue
        
        enhanced_products = []
        
        for product in products:
            try:
                enhanced_product = enhance_product_data(
                    product, user_currency, user_country, include_shipping, include_taxes, query
                )
                if enhanced_product:
                    enhanced_products.append(enhanced_product)
            except Exception as e:
                logger.warning(f"Error enhancing product from {platform}: {e}")
                # Include original product data as fallback
                enhanced_products.append(product)
        
        # Calculate platform statistics
        platform_stats = calculate_platform_stats(enhanced_products, user_currency)
        
        enhanced_results[platform] = {
            'products': enhanced_products,
            'platform_stats': platform_stats
        }
    
    return enhanced_results

def enhance_product_data(product, user_currency, user_country, include_shipping, include_taxes, query):
    """Enhance individual product with currency conversion and cost calculation"""
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
                # Final fallback to original price if both services fail
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
            cost_breakdown = calculate_total_costs(
                enhanced_product, user_country, include_shipping, include_taxes, query
            )
            enhanced_product['cost_breakdown'] = cost_breakdown
            enhanced_product['total_cost'] = cost_breakdown['total_cost']
        else:
            enhanced_product['total_cost'] = enhanced_product['converted_price']
        
        # Add savings calculation (compared to highest price)
        enhanced_product['savings_vs_highest'] = 0  # Will be calculated later
        
        # Add delivery estimate
        enhanced_product['delivery_estimate'] = get_delivery_estimate(
            product.get('platform'), user_country
        )
        
        # Add trust score (basic implementation)
        enhanced_product['trust_score'] = calculate_trust_score(product)
        
        return enhanced_product
        
    except Exception as e:
        logger.error(f"Error enhancing product data: {e}")
        return product

def calculate_total_costs(product, user_country, include_shipping, include_taxes, query):
    """Calculate total costs including shipping and taxes"""
    try:
        # Create product info for cost calculator
        product_info = ProductInfo(
            price=product['converted_price'],
            currency=product['user_currency'],
            category=categorize_product(query),
            weight=estimate_weight(query),
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
            'currency': product['user_currency']
        }
        
    except Exception as e:
        logger.error(f"Error calculating total costs: {e}")
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

def categorize_product(query):
    """Categorize product based on search query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['phone', 'iphone', 'android', 'smartphone']):
        return 'electronics'
    elif any(word in query_lower for word in ['laptop', 'computer', 'tablet', 'ipad']):
        return 'electronics'
    elif any(word in query_lower for word in ['headphones', 'earbuds', 'speaker', 'audio']):
        return 'electronics'
    elif any(word in query_lower for word in ['shirt', 'dress', 'pants', 'shoes', 'clothing']):
        return 'clothing'
    elif any(word in query_lower for word in ['book', 'novel', 'textbook']):
        return 'books'
    else:
        return 'general'

def estimate_weight(query):
    """Estimate product weight based on query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['laptop', 'computer']):
        return 2.0  # kg
    elif any(word in query_lower for word in ['phone', 'smartphone']):
        return 0.2  # kg
    elif any(word in query_lower for word in ['headphones']):
        return 0.3  # kg
    elif any(word in query_lower for word in ['book']):
        return 0.5  # kg
    elif any(word in query_lower for word in ['clothing', 'shirt', 'dress']):
        return 0.3  # kg
    else:
        return 0.5  # kg default

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
    """Calculate a basic trust score for the product/platform"""
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

def calculate_platform_stats(products, currency):
    """Calculate statistics for a platform"""
    if not products:
        return {
            'product_count': 0,
            'avg_price': 0,
            'min_price': None,
            'max_price': None,
            'avg_total_cost': 0,
            'min_total_cost': None,
            'max_total_cost': None
        }
    
    prices = [p['converted_price'] for p in products if p.get('converted_price')]
    total_costs = [p.get('total_cost', p['converted_price']) for p in products]
    
    return {
        'product_count': len(products),
        'avg_price': round(sum(prices) / len(prices), 2) if prices else 0,
        'min_price': min(prices) if prices else None,
        'max_price': max(prices) if prices else None,
        'avg_total_cost': round(sum(total_costs) / len(total_costs), 2) if total_costs else 0,
        'min_total_cost': min(total_costs) if total_costs else None,
        'max_total_cost': max(total_costs) if total_costs else None,
        'currency': currency
    }

def generate_search_summary(enhanced_results):
    """Generate a summary of search results"""
    total_products = 0
    all_total_costs = []
    platforms_with_results = 0
    best_deals = []
    
    for platform, data in enhanced_results.items():
        products = data['products']
        if products:
            platforms_with_results += 1
            total_products += len(products)
            
            # Collect all total costs
            for product in products:
                total_cost = product.get('total_cost', product.get('converted_price', 0))
                if total_cost:
                    all_total_costs.append({
                        'cost': total_cost,
                        'product': product,
                        'platform': platform
                    })
    
    if not all_total_costs:
        return {
            'total_products': 0,
            'platforms_with_results': 0,
            'price_range': None,
            'best_deal': None,
            'potential_savings': None
        }
    
    # Sort by total cost
    all_total_costs.sort(key=lambda x: x['cost'])
    
    # Calculate price range
    min_cost = all_total_costs[0]['cost']
    max_cost = all_total_costs[-1]['cost']
    avg_cost = sum(item['cost'] for item in all_total_costs) / len(all_total_costs)
    
    # Best deal
    best_deal = all_total_costs[0]
    
    # Potential savings
    savings_amount = max_cost - min_cost
    savings_percentage = (savings_amount / max_cost) * 100 if max_cost > 0 else 0
    
    return {
        'total_products': total_products,
        'platforms_with_results': platforms_with_results,
        'price_range': {
            'min': round(min_cost, 2),
            'max': round(max_cost, 2),
            'average': round(avg_cost, 2)
        },
        'best_deal': {
            'platform': best_deal['platform'],
            'product_name': best_deal['product']['name'][:50] + '...',
            'total_cost': round(best_deal['cost'], 2),
            'currency': best_deal['product'].get('user_currency', 'USD')
        },
        'potential_savings': {
            'amount': round(savings_amount, 2),
            'percentage': round(savings_percentage, 1)
        }
    }

@enhanced_search_bp.route('/platforms', methods=['GET'])
def get_supported_platforms():
    """Get list of supported platforms and their capabilities"""
    return jsonify({
        'platforms': [
            {
                'name': 'Amazon',
                'country': 'US',
                'currency': 'USD',
                'shipping_worldwide': True,
                'typical_delivery': '2-5 days (US), 5-10 days (International)',
                'trust_score': 95
            },
            {
                'name': 'eBay',
                'country': 'US',
                'currency': 'USD',
                'shipping_worldwide': True,
                'typical_delivery': '3-7 days (US), 7-14 days (International)',
                'trust_score': 75
            },
            {
                'name': 'AliExpress',
                'country': 'CN',
                'currency': 'USD',
                'shipping_worldwide': True,
                'typical_delivery': '15-30 days',
                'trust_score': 65
            },
            {
                'name': 'Walmart',
                'country': 'US',
                'currency': 'USD',
                'shipping_worldwide': False,
                'typical_delivery': '2-5 days (US only)',
                'trust_score': 85
            },
            {
                'name': 'Best Buy',
                'country': 'US',
                'currency': 'USD',
                'shipping_worldwide': False,
                'typical_delivery': '2-5 days (US only)',
                'trust_score': 90
            },
            {
                'name': 'Temu',
                'country': 'CN',
                'currency': 'USD',
                'shipping_worldwide': True,
                'typical_delivery': '7-15 days',
                'trust_score': 60
            },
            {
                'name': 'Shein',
                'country': 'CN',
                'currency': 'USD',
                'shipping_worldwide': True,
                'typical_delivery': '8-15 days',
                'trust_score': 55,
                'specialty': 'Fashion & Clothing'
            }
        ],
        'total_platforms': 7,
        'supported_currencies': currency_service.get_supported_currencies()[:20],  # Top 20
        'supported_countries': ['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'ZA', 'JP', 'CN', 'IN', 'BR', 'MX']
    })

@enhanced_search_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the enhanced search service"""
    try:
        # Test currency service
        currency_test = currency_service.convert_currency(100, 'USD', 'EUR')
        
        # Test price collector cache
        cache_status = len(price_collector.cache)
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'currency_service': 'operational' if currency_test else 'degraded',
                'price_collector': 'operational',
                'cost_calculator': 'operational'
            },
            'cache_entries': cache_status,
            'version': '1.0.0'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
