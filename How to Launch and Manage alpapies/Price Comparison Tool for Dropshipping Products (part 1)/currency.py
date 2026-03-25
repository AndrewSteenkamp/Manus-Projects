"""
Currency API Routes for PricePulse
Handles currency conversion and exchange rate endpoints
"""

from flask import Blueprint, request, jsonify
from src.services.currency_service import currency_service
from src.services.cost_calculator import cost_calculator, ProductInfo, ShippingInfo, ShippingMethod
import logging

logger = logging.getLogger(__name__)

currency_bp = Blueprint('currency', __name__, url_prefix='/api/currency')

@currency_bp.route('/rates', methods=['GET'])
def get_exchange_rates():
    """Get current exchange rates for a base currency"""
    try:
        base_currency = request.args.get('base', 'USD').upper()
        
        rates_data = currency_service.get_exchange_rates(base_currency)
        if not rates_data:
            return jsonify({
                'error': 'Unable to fetch exchange rates',
                'message': 'Please try again later'
            }), 503
        
        return jsonify({
            'success': True,
            'base_currency': rates_data['base_code'],
            'rates': rates_data['rates'],
            'last_updated': rates_data['last_updated'],
            'source': rates_data['source']
        })
        
    except Exception as e:
        logger.error(f"Error getting exchange rates: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to process request'
        }), 500

@currency_bp.route('/convert', methods=['POST'])
def convert_currency():
    """Convert amount between currencies"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['amount', 'from_currency', 'to_currency']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'message': f'Field "{field}" is required'
                }), 400
        
        amount = float(data['amount'])
        from_currency = data['from_currency'].upper()
        to_currency = data['to_currency'].upper()
        
        if amount <= 0:
            return jsonify({
                'error': 'Invalid amount',
                'message': 'Amount must be greater than 0'
            }), 400
        
        conversion = currency_service.convert_currency(amount, from_currency, to_currency)
        if not conversion:
            return jsonify({
                'error': 'Conversion failed',
                'message': 'Unable to convert between specified currencies'
            }), 400
        
        return jsonify({
            'success': True,
            'conversion': conversion
        })
        
    except ValueError:
        return jsonify({
            'error': 'Invalid amount',
            'message': 'Amount must be a valid number'
        }), 400
    except Exception as e:
        logger.error(f"Error converting currency: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to process conversion'
        }), 500

@currency_bp.route('/supported', methods=['GET'])
def get_supported_currencies():
    """Get list of supported currencies"""
    try:
        currencies = currency_service.get_supported_currencies()
        
        # Get detailed info for each currency
        currency_details = []
        for code in currencies:
            info = currency_service.get_currency_info(code)
            currency_details.append({
                'code': code,
                'name': info['name'],
                'symbol': info['symbol'],
                'country': info['country']
            })
        
        return jsonify({
            'success': True,
            'currencies': currency_details,
            'total_count': len(currency_details)
        })
        
    except Exception as e:
        logger.error(f"Error getting supported currencies: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to fetch currency list'
        }), 500

@currency_bp.route('/calculate-total-cost', methods=['POST'])
def calculate_total_cost():
    """Calculate total landed cost including all fees and taxes"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['price', 'currency', 'category', 'destination_country']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'message': f'Field "{field}" is required'
                }), 400
        
        # Create product info
        product = ProductInfo(
            price=float(data['price']),
            currency=data['currency'].upper(),
            category=data['category'],
            weight=data.get('weight', 0.5),  # Default 0.5kg
            origin_country=data.get('origin_country', 'US'),
            vendor=data.get('vendor', '')
        )
        
        # Create shipping info
        shipping_method_str = data.get('shipping_method', 'standard')
        try:
            shipping_method = ShippingMethod(shipping_method_str)
        except ValueError:
            shipping_method = ShippingMethod.STANDARD
        
        shipping = ShippingInfo(
            destination_country=data['destination_country'].upper(),
            destination_region=data.get('destination_region', ''),
            shipping_method=shipping_method,
            is_remote_area=data.get('is_remote_area', False)
        )
        
        target_currency = data.get('target_currency', 'USD').upper()
        
        # Calculate costs
        breakdown = cost_calculator.calculate_total_cost(product, shipping, target_currency)
        
        # Convert to target currency if needed
        if breakdown.base_currency != target_currency:
            conversion = currency_service.convert_currency(
                breakdown.total_cost, 
                breakdown.base_currency, 
                target_currency
            )
            if conversion:
                breakdown.total_cost = conversion['converted_amount']
                breakdown.exchange_rate = conversion['exchange_rate']
                breakdown.target_currency = target_currency
                
                # Convert all components
                for component, amount in breakdown.cost_components.items():
                    converted = currency_service.convert_currency(amount, breakdown.base_currency, target_currency)
                    if converted:
                        breakdown.cost_components[component] = converted['converted_amount']
        
        return jsonify({
            'success': True,
            'cost_breakdown': {
                'base_price': breakdown.base_price,
                'shipping_cost': breakdown.shipping_cost,
                'vat_amount': breakdown.vat_amount,
                'import_duty': breakdown.import_duty,
                'handling_fee': breakdown.handling_fee,
                'insurance_fee': breakdown.insurance_fee,
                'total_cost': breakdown.total_cost,
                'currency': breakdown.target_currency,
                'exchange_rate': breakdown.exchange_rate,
                'cost_components': breakdown.cost_components
            }
        })
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid input',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error calculating total cost: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to calculate total cost'
        }), 500

@currency_bp.route('/cost-estimate', methods=['POST'])
def get_cost_estimate():
    """Get a quick cost estimate summary"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['price', 'currency', 'destination_country']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'message': f'Field "{field}" is required'
                }), 400
        
        # Create simplified product and shipping info
        product = ProductInfo(
            price=float(data['price']),
            currency=data['currency'].upper(),
            category=data.get('category', 'general'),
            weight=data.get('weight', 0.5),
            origin_country=data.get('origin_country', 'US')
        )
        
        shipping = ShippingInfo(
            destination_country=data['destination_country'].upper(),
            shipping_method=ShippingMethod.STANDARD
        )
        
        # Get estimate
        estimate = cost_calculator.get_cost_estimate_summary(product, shipping)
        
        return jsonify({
            'success': True,
            'estimate': estimate
        })
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid input',
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error getting cost estimate: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to get cost estimate'
        }), 500

@currency_bp.route('/cache/status', methods=['GET'])
def get_cache_status():
    """Get currency cache status (for debugging)"""
    try:
        cache_status = currency_service.get_cache_status()
        return jsonify({
            'success': True,
            'cache_status': cache_status
        })
    except Exception as e:
        logger.error(f"Error getting cache status: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to get cache status'
        }), 500

@currency_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear currency cache (for debugging)"""
    try:
        currency_service.clear_cache()
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Unable to clear cache'
        }), 500

