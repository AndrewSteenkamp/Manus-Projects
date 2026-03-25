"""
Service Search API Routes
Endpoints for searching and comparing services and service providers
"""

from flask import Blueprint, request, jsonify
import time
from datetime import datetime
from ..services.service_provider_collector import ServiceProviderCollector
from ..services.service_comparison_engine import ServiceComparisonEngine
from ..services.fallback_currency_service import FallbackCurrencyService
from ..services.affiliate_manager import AffiliateManager

service_search_bp = Blueprint('service_search', __name__)

# Initialize services
service_collector = ServiceProviderCollector()
comparison_engine = ServiceComparisonEngine()
currency_service = FallbackCurrencyService()
affiliate_manager = AffiliateManager()

@service_search_bp.route('/service-search', methods=['GET'])
def search_services():
    """Search for services across multiple platforms"""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '')
        max_results = min(int(request.args.get('max_results', 20)), 50)
        currency = request.args.get('currency', 'USD')
        location = request.args.get('location', '')
        budget_min = request.args.get('budget_min', type=float)
        budget_max = request.args.get('budget_max', type=float)
        service_type = request.args.get('service_type', '')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        start_time = time.time()
        
        # Search for services
        services = service_collector.search_services(query, category, max_results)
        
        # Filter by budget if specified
        if budget_min or budget_max:
            services = filter_services_by_budget(services, budget_min, budget_max)
        
        # Filter by service type if specified
        if service_type:
            services = [s for s in services if service_type.lower() in s.get('service_type', '').lower()]
        
        # Convert currency if needed
        if currency != 'USD':
            services = convert_service_prices(services, currency)
        
        # User preferences for comparison
        user_preferences = {
            'location': location,
            'currency': currency,
            'budget_min': budget_min,
            'budget_max': budget_max,
            'service_type': service_type
        }
        
        # Compare and rank services
        comparison_result = comparison_engine.compare_services(services, user_preferences)
        
        # Generate affiliate links
        for service in comparison_result['services']:
            service['affiliate_url'] = generate_service_affiliate_link(service)
        
        search_duration = time.time() - start_time
        
        # Prepare response
        response = {
            'query': query,
            'category': category,
            'total_services': comparison_result['total_services'],
            'platforms_searched': comparison_result['platforms_searched'],
            'search_duration_seconds': round(search_duration, 2),
            'currency': currency,
            'user_location': location,
            'services': comparison_result['services'],
            'service_groups': comparison_result['service_groups'],
            'recommendations': comparison_result['recommendations'],
            'insights': comparison_result['insights'],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Service search failed: {str(e)}'}), 500

@service_search_bp.route('/service-categories', methods=['GET'])
def get_service_categories():
    """Get available service categories"""
    try:
        categories = service_collector.get_service_categories()
        platforms = service_collector.get_platform_info()
        
        return jsonify({
            'categories': categories,
            'platforms': platforms,
            'total_categories': len(categories),
            'total_platforms': len(platforms)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get categories: {str(e)}'}), 500

@service_search_bp.route('/service-suggestions', methods=['GET'])
def get_service_suggestions():
    """Get service search suggestions"""
    try:
        query = request.args.get('q', '').strip().lower()
        
        # Popular service suggestions
        suggestions = [
            'web development', 'graphic design', 'digital marketing', 'content writing',
            'logo design', 'seo services', 'social media management', 'video editing',
            'mobile app development', 'wordpress development', 'copywriting', 'translation',
            'data entry', 'virtual assistant', 'bookkeeping', 'customer service',
            'house cleaning', 'handyman services', 'plumbing', 'electrical work',
            'lawn care', 'pest control', 'hvac repair', 'painting services',
            'tutoring', 'fitness training', 'pet sitting', 'event planning',
            'photography', 'music lessons', 'life coaching', 'massage therapy',
            'legal consultation', 'accounting services', 'business consulting',
            'real estate agent', 'insurance agent', 'financial planning'
        ]
        
        # Filter suggestions based on query
        if query:
            filtered_suggestions = [s for s in suggestions if query in s.lower()]
            # Add exact matches first, then partial matches
            exact_matches = [s for s in filtered_suggestions if s.lower().startswith(query)]
            partial_matches = [s for s in filtered_suggestions if not s.lower().startswith(query)]
            suggestions = exact_matches + partial_matches
        
        return jsonify({
            'suggestions': suggestions[:10],  # Limit to 10 suggestions
            'query': query
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get suggestions: {str(e)}'}), 500

@service_search_bp.route('/service-platforms', methods=['GET'])
def get_service_platforms():
    """Get information about supported service platforms"""
    try:
        platforms = service_collector.get_platform_info()
        
        # Add additional platform information
        platform_details = {}
        for platform, info in platforms.items():
            platform_details[platform] = {
                **info,
                'trust_score': comparison_engine.platform_trust_scores.get(platform, 0.75),
                'service_types': get_platform_service_types(platform),
                'typical_pricing': get_platform_pricing_info(platform)
            }
        
        return jsonify({
            'platforms': platform_details,
            'total_platforms': len(platform_details),
            'most_trusted': max(platform_details.items(), 
                              key=lambda x: x[1]['trust_score'])[0]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get platforms: {str(e)}'}), 500

@service_search_bp.route('/service-compare', methods=['POST'])
def compare_specific_services():
    """Compare specific services provided by the user"""
    try:
        data = request.get_json()
        services = data.get('services', [])
        user_preferences = data.get('preferences', {})
        
        if not services:
            return jsonify({'error': 'Services array is required'}), 400
        
        # Compare services
        comparison_result = comparison_engine.compare_services(services, user_preferences)
        
        # Generate affiliate links
        for service in comparison_result['services']:
            service['affiliate_url'] = generate_service_affiliate_link(service)
        
        return jsonify(comparison_result)
        
    except Exception as e:
        return jsonify({'error': f'Service comparison failed: {str(e)}'}), 500

def filter_services_by_budget(services, budget_min=None, budget_max=None):
    """Filter services by budget range"""
    if not budget_min and not budget_max:
        return services
    
    filtered_services = []
    for service in services:
        price = extract_service_price(service)
        if price:
            if budget_min and price < budget_min:
                continue
            if budget_max and price > budget_max:
                continue
        filtered_services.append(service)
    
    return filtered_services

def extract_service_price(service):
    """Extract price from service for filtering"""
    # Try different price fields
    for field in ['starting_price', 'hourly_rate', 'bid_amount']:
        if field in service and service[field]:
            return float(service[field])
    
    # Try to extract from price ranges
    for field in ['price_range', 'quote_range']:
        if field in service and service[field]:
            import re
            numbers = re.findall(r'\d+', str(service[field]))
            if numbers:
                return float(numbers[0])
    
    return None

def convert_service_prices(services, target_currency):
    """Convert service prices to target currency"""
    try:
        exchange_rate = currency_service.get_exchange_rate('USD', target_currency)
        if not exchange_rate:
            return services  # Return original if conversion fails
        
        for service in services:
            # Convert various price fields
            price_fields = ['starting_price', 'hourly_rate', 'bid_amount']
            for field in price_fields:
                if field in service and service[field]:
                    service[field] = round(service[field] * exchange_rate, 2)
            
            # Update currency
            service['currency'] = target_currency
            
            # Convert price ranges
            for field in ['price_range', 'quote_range']:
                if field in service and service[field]:
                    service[field] = convert_price_range_string(service[field], exchange_rate, target_currency)
        
        return services
        
    except Exception as e:
        print(f"Currency conversion error: {e}")
        return services

def convert_price_range_string(price_range, exchange_rate, currency):
    """Convert price range string to new currency"""
    import re
    
    # Extract numbers from price range
    numbers = re.findall(r'\d+', str(price_range))
    if len(numbers) >= 2:
        min_price = round(float(numbers[0]) * exchange_rate, 2)
        max_price = round(float(numbers[1]) * exchange_rate, 2)
        return f"{currency} {min_price} - {max_price}"
    elif len(numbers) == 1:
        price = round(float(numbers[0]) * exchange_rate, 2)
        return f"{currency} {price}"
    
    return price_range

def generate_service_affiliate_link(service):
    """Generate affiliate link for service"""
    try:
        platform = service.get('platform', '')
        service_url = service.get('service_url', '')
        
        if not service_url:
            return None
        
        # Get affiliate program info
        affiliate_programs = affiliate_manager.get_affiliate_programs()
        
        # Map service platforms to affiliate programs
        platform_mapping = {
            'Fiverr': 'Fiverr',
            'Upwork': 'Upwork',
            'Freelancer': 'Freelancer',
            'TaskRabbit': 'TaskRabbit',
            'Thumbtack': 'Thumbtack',
            'Angie': 'Angie'
        }
        
        affiliate_platform = platform_mapping.get(platform)
        if affiliate_platform and affiliate_platform in affiliate_programs:
            # Generate affiliate link (simplified - would need actual affiliate IDs)
            affiliate_id = affiliate_programs[affiliate_platform].get('affiliate_id', '')
            if affiliate_id:
                separator = '&' if '?' in service_url else '?'
                return f"{service_url}{separator}ref={affiliate_id}"
        
        return service_url
        
    except Exception as e:
        print(f"Affiliate link generation error: {e}")
        return service.get('service_url', '')

def get_platform_service_types(platform):
    """Get service types available on platform"""
    platform_types = {
        'Fiverr': ['Digital Services', 'Creative Services', 'Business Services'],
        'Upwork': ['Professional Services', 'Technical Services', 'Creative Services'],
        'Freelancer': ['Development Services', 'Design Services', 'Business Services'],
        'TaskRabbit': ['Local Services', 'Home Services', 'Personal Services'],
        'Thumbtack': ['Professional Services', 'Home Services', 'Personal Services'],
        'Angie': ['Home Services', 'Contractor Services', 'Maintenance Services']
    }
    return platform_types.get(platform, ['General Services'])

def get_platform_pricing_info(platform):
    """Get typical pricing information for platform"""
    pricing_info = {
        'Fiverr': {'min': 5, 'typical_range': '5-200', 'pricing_model': 'Fixed Price'},
        'Upwork': {'min': 15, 'typical_range': '15-150/hour', 'pricing_model': 'Hourly/Fixed'},
        'Freelancer': {'min': 10, 'typical_range': '10-100/hour', 'pricing_model': 'Bid-based'},
        'TaskRabbit': {'min': 25, 'typical_range': '25-100/hour', 'pricing_model': 'Hourly'},
        'Thumbtack': {'min': 50, 'typical_range': '50-500', 'pricing_model': 'Quote-based'},
        'Angie': {'min': 100, 'typical_range': '100-2000', 'pricing_model': 'Quote-based'}
    }
    return pricing_info.get(platform, {'min': 0, 'typical_range': 'Varies', 'pricing_model': 'Various'})
