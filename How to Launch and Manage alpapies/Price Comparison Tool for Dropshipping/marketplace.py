"""
Marketplace API Routes for PricePulse
Handles multi-marketplace search and integration endpoints
"""

from flask import Blueprint, request, jsonify
from src.services.marketplace_integrations import (
    marketplace_aggregator, SearchQuery, MarketplaceType
)
from src.services.currency_service import currency_service
from src.services.cost_calculator import cost_calculator, ProductInfo, ShippingInfo, ShippingMethod
import logging

logger = logging.getLogger(__name__)

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/api/marketplace')

@marketplace_bp.route('/search', methods=['POST'])
def search_products():
    """Search for products across multiple marketplaces"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'keyword' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Field "keyword" is required'
            }), 400
        
        # Create search query
        query = SearchQuery(
            keyword=data['keyword'],
            category=data.get('category', ''),
            min_price=data.get('min_price', 0.0),
            max_price=data.get('max_price', 0.0),
            location=data.get('location', ''),
            condition=data.get('condition', ''),
            sort_by=data.get('sort_by', 'relevance')
        )
        
        # Get specified marketplaces or search all
        marketplace_names = data.get('marketplaces', [])
        marketplaces = []
        
        if marketplace_names:
            for name in marketplace_names:
                try:
                    marketplace_type = MarketplaceType(name.lower())
                    marketplaces.append(marketplace_type)
                except ValueError:
                    logger.warning(f"Unknown marketplace: {name}")
        else:
            marketplaces = None  # Search all marketplaces
        
        # Perform search
        results = marketplace_aggregator.search_all_marketplaces(query, marketplaces)
        
        # Convert results to JSON-serializable format
        formatted_results = {}
        total_products = 0
        
        for marketplace, listings in results.items():
            formatted_listings = []
            for listing in listings:
                formatted_listings.append({
                    'title': listing.title,
                    'price': listing.price,
                    'currency': listing.currency,
                    'marketplace': listing.marketplace.value,
                    'url': listing.url,
                    'image_url': listing.image_url,
                    'seller': listing.seller,
                    'rating': listing.rating,
                    'reviews_count': listing.reviews_count,
                    'shipping_cost': listing.shipping_cost,
                    'availability': listing.availability,
                    'location': listing.location,
                    'condition': listing.condition,
                    'marketplace_id': listing.marketplace_id
                })
            
            formatted_results[marketplace] = formatted_listings
            total_products += len(formatted_listings)
        
        return jsonify({
            'success': True,
            'query': {
                'keyword': query.keyword,
                'category': query.category,
                'location': query.location
            },
            'results': formatted_results,
            'total_products': total_products,
            'marketplaces_searched': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching marketplaces: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to search marketplaces'
        }), 500

@marketplace_bp.route('/best-deals', methods=['POST'])
def get_best_deals():
    """Get the best deals across all marketplaces"""
    try:
        data = request.get_json()
        
        if 'keyword' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Field "keyword" is required'
            }), 400
        
        # Create search query
        query = SearchQuery(
            keyword=data['keyword'],
            category=data.get('category', ''),
            min_price=data.get('min_price', 0.0),
            max_price=data.get('max_price', 0.0),
            location=data.get('location', ''),
            condition=data.get('condition', ''),
            sort_by='price_low'  # Always sort by price for best deals
        )
        
        limit = data.get('limit', 10)
        user_location = data.get('user_location', 'US')
        user_currency = data.get('user_currency', 'USD')
        
        # Get best deals
        best_deals = marketplace_aggregator.get_best_deals(query, limit)
        
        # Calculate total costs including shipping, taxes, etc.
        enhanced_deals = []
        
        for deal in best_deals:
            try:
                # Create product info for cost calculation
                product = ProductInfo(
                    price=deal.price,
                    currency=deal.currency,
                    category=query.category or 'general',
                    weight=0.5,  # Default weight
                    origin_country=deal.location or 'US',
                    vendor=deal.seller
                )
                
                # Create shipping info
                shipping = ShippingInfo(
                    destination_country=user_location,
                    shipping_method=ShippingMethod.STANDARD
                )
                
                # Calculate total cost
                cost_breakdown = cost_calculator.calculate_total_cost(product, shipping, user_currency)
                
                # Convert to user currency if needed
                display_price = deal.price
                total_cost = cost_breakdown.total_cost
                
                if deal.currency != user_currency:
                    conversion = currency_service.convert_currency(deal.price, deal.currency, user_currency)
                    if conversion:
                        display_price = conversion['converted_amount']
                
                enhanced_deal = {
                    'title': deal.title,
                    'original_price': deal.price,
                    'original_currency': deal.currency,
                    'display_price': display_price,
                    'total_cost': total_cost,
                    'currency': user_currency,
                    'marketplace': deal.marketplace.value,
                    'url': deal.url,
                    'image_url': deal.image_url,
                    'seller': deal.seller,
                    'rating': deal.rating,
                    'reviews_count': deal.reviews_count,
                    'shipping_cost': deal.shipping_cost,
                    'availability': deal.availability,
                    'location': deal.location,
                    'condition': deal.condition,
                    'cost_breakdown': {
                        'base_price': cost_breakdown.base_price,
                        'shipping': cost_breakdown.shipping_cost,
                        'taxes': cost_breakdown.vat_amount + cost_breakdown.import_duty,
                        'fees': cost_breakdown.handling_fee + cost_breakdown.insurance_fee,
                        'total': cost_breakdown.total_cost
                    },
                    'savings_estimate': max(0, display_price * 0.2)  # Estimated savings vs local retail
                }
                
                enhanced_deals.append(enhanced_deal)
                
            except Exception as e:
                logger.error(f"Error calculating costs for deal: {e}")
                # Add basic deal without cost calculation
                enhanced_deals.append({
                    'title': deal.title,
                    'original_price': deal.price,
                    'original_currency': deal.currency,
                    'display_price': deal.price,
                    'total_cost': deal.price,
                    'currency': deal.currency,
                    'marketplace': deal.marketplace.value,
                    'url': deal.url,
                    'image_url': deal.image_url,
                    'seller': deal.seller,
                    'rating': deal.rating,
                    'reviews_count': deal.reviews_count,
                    'availability': deal.availability,
                    'location': deal.location,
                    'condition': deal.condition
                })
        
        return jsonify({
            'success': True,
            'query': {
                'keyword': query.keyword,
                'user_location': user_location,
                'user_currency': user_currency
            },
            'best_deals': enhanced_deals,
            'total_deals': len(enhanced_deals)
        })
        
    except Exception as e:
        logger.error(f"Error getting best deals: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to get best deals'
        }), 500

@marketplace_bp.route('/supported', methods=['GET'])
def get_supported_marketplaces():
    """Get list of supported marketplaces"""
    try:
        marketplaces = marketplace_aggregator.get_supported_marketplaces()
        
        return jsonify({
            'success': True,
            'marketplaces': marketplaces,
            'total_count': len(marketplaces)
        })
        
    except Exception as e:
        logger.error(f"Error getting supported marketplaces: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to get marketplace list'
        }), 500

@marketplace_bp.route('/suggest-site', methods=['POST'])
def suggest_new_site():
    """Allow users to suggest new sites for integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'url', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'message': f'Field "{field}" is required'
                }), 400
        
        # Prepare site info
        site_info = {
            'name': data['name'],
            'url': data['url'],
            'description': data['description'],
            'search_pattern': data.get('search_pattern', ''),
            'category': data.get('category', 'general'),
            'suggested_by': data.get('user_id', 'anonymous'),
            'status': 'pending_review'
        }
        
        # Add to suggested sites
        success = marketplace_aggregator.add_user_suggested_site(site_info)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Site suggestion submitted successfully',
                'site_info': {
                    'name': site_info['name'],
                    'url': site_info['url'],
                    'status': 'pending_review'
                }
            })
        else:
            return jsonify({
                'error': 'Invalid site information',
                'message': 'Unable to process site suggestion'
            }), 400
        
    except Exception as e:
        logger.error(f"Error processing site suggestion: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to process site suggestion'
        }), 500

@marketplace_bp.route('/compare', methods=['POST'])
def compare_products():
    """Compare specific products across marketplaces"""
    try:
        data = request.get_json()
        
        if 'products' not in data or not data['products']:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Field "products" with product IDs is required'
            }), 400
        
        product_ids = data['products']
        user_location = data.get('user_location', 'US')
        user_currency = data.get('user_currency', 'USD')
        
        # For demo purposes, generate comparison data
        # In production, this would fetch actual product details
        comparison_results = []
        
        for i, product_id in enumerate(product_ids):
            # Mock product data
            base_price = 50 + (i * 10)
            
            product_comparison = {
                'product_id': product_id,
                'title': f"Product {product_id}",
                'marketplace_prices': [
                    {
                        'marketplace': 'amazon',
                        'price': base_price * 1.1,
                        'currency': 'USD',
                        'availability': 'in_stock',
                        'shipping_cost': 5.99,
                        'total_cost': (base_price * 1.1) + 5.99
                    },
                    {
                        'marketplace': 'temu',
                        'price': base_price * 0.7,
                        'currency': 'USD',
                        'availability': 'in_stock',
                        'shipping_cost': 8.99,
                        'total_cost': (base_price * 0.7) + 8.99
                    },
                    {
                        'marketplace': 'ebay',
                        'price': base_price * 0.9,
                        'currency': 'USD',
                        'availability': 'limited_stock',
                        'shipping_cost': 7.50,
                        'total_cost': (base_price * 0.9) + 7.50
                    }
                ],
                'best_deal': {
                    'marketplace': 'temu',
                    'total_cost': (base_price * 0.7) + 8.99,
                    'savings': base_price * 0.4
                }
            }
            
            comparison_results.append(product_comparison)
        
        return jsonify({
            'success': True,
            'comparison': comparison_results,
            'user_location': user_location,
            'user_currency': user_currency,
            'total_products': len(comparison_results)
        })
        
    except Exception as e:
        logger.error(f"Error comparing products: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to compare products'
        }), 500

@marketplace_bp.route('/trending', methods=['GET'])
def get_trending_products():
    """Get trending products across marketplaces"""
    try:
        category = request.args.get('category', '')
        limit = int(request.args.get('limit', 20))
        
        # For demo purposes, generate trending products
        trending_products = []
        
        categories = ['electronics', 'clothing', 'home', 'beauty', 'sports'] if not category else [category]
        
        for cat in categories:
            for i in range(limit // len(categories)):
                product = {
                    'title': f"Trending {cat.title()} Product {i+1}",
                    'category': cat,
                    'price_range': {
                        'min': 10 + (i * 5),
                        'max': 50 + (i * 10),
                        'currency': 'USD'
                    },
                    'marketplaces': ['amazon', 'temu', 'shein', 'ebay'],
                    'popularity_score': 95 - (i * 2),
                    'image_url': f"https://via.placeholder.com/300x300?text={cat}+Product",
                    'search_volume': 10000 - (i * 500)
                }
                trending_products.append(product)
        
        return jsonify({
            'success': True,
            'trending_products': trending_products[:limit],
            'category': category or 'all',
            'total_count': len(trending_products)
        })
        
    except Exception as e:
        logger.error(f"Error getting trending products: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to get trending products'
        }), 500

