from flask import Blueprint, request, jsonify
from src.services.affiliate_manager import (
    AffiliateManager, track_affiliate_click, get_affiliate_link
)
from src.models.product import db, ProductVendor, ClickTracking, Vendor
from datetime import datetime, timedelta
import uuid

affiliate_bp = Blueprint('affiliate', __name__)

@affiliate_bp.route('/click', methods=['POST'])
def track_click():
    """Track affiliate link clicks and return redirect URL"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'product_vendor_id' not in data:
            return jsonify({'error': 'Missing product_vendor_id'}), 400
        
        # Get or create session ID
        session_id = data.get('session_id') or str(uuid.uuid4())
        
        # Get user information
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        referrer = request.headers.get('Referer', '')
        
        # Track the click
        result = track_affiliate_click(
            data['product_vendor_id'],
            session_id,
            user_ip,
            user_agent,
            referrer
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'redirect_url': result['redirect_url'],
            'click_id': result['click_id'],
            'tracking_id': result['tracking_id']
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to track click: {str(e)}'}), 500

@affiliate_bp.route('/link/<int:product_vendor_id>', methods=['GET'])
def get_product_affiliate_link(product_vendor_id):
    """Get affiliate link for a specific product vendor"""
    try:
        affiliate_link = get_affiliate_link(product_vendor_id)
        
        if not affiliate_link:
            return jsonify({'error': 'Product vendor not found'}), 404
        
        return jsonify({
            'product_vendor_id': product_vendor_id,
            'affiliate_link': affiliate_link
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get affiliate link: {str(e)}'}), 500

@affiliate_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get affiliate click analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        
        manager = AffiliateManager()
        analytics = manager.get_click_analytics(days)
        
        if 'error' in analytics:
            return jsonify(analytics), 500
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500

@affiliate_bp.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get summary analytics for dashboard"""
    try:
        # Get analytics for different periods
        manager = AffiliateManager()
        
        today = manager.get_click_analytics(1)
        week = manager.get_click_analytics(7)
        month = manager.get_click_analytics(30)
        
        # Get top performing products
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        top_products = db.session.query(
            ProductVendor.id,
            ProductVendor.product_id,
            db.func.count(ClickTracking.id).label('clicks')
        ).join(ClickTracking).filter(
            ClickTracking.clicked_at >= thirty_days_ago
        ).group_by(ProductVendor.id).order_by(
            db.func.count(ClickTracking.id).desc()
        ).limit(10).all()
        
        # Get conversion rates (simplified)
        total_clicks = ClickTracking.query.filter(
            ClickTracking.clicked_at >= thirty_days_ago
        ).count()
        
        conversions = ClickTracking.query.filter(
            ClickTracking.clicked_at >= thirty_days_ago,
            ClickTracking.conversion_tracked == True
        ).count()
        
        conversion_rate = (conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        return jsonify({
            'today': today,
            'week': week,
            'month': month,
            'top_products': [
                {
                    'product_vendor_id': pv_id,
                    'product_id': p_id,
                    'clicks': clicks
                } for pv_id, p_id, clicks in top_products
            ],
            'conversion_rate': round(conversion_rate, 2),
            'total_clicks_30d': total_clicks
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get analytics summary: {str(e)}'}), 500

@affiliate_bp.route('/deep-link', methods=['POST'])
def generate_deep_link():
    """Generate deep link for search on specific platform"""
    try:
        data = request.get_json()
        
        if 'vendor_name' not in data or 'search_query' not in data:
            return jsonify({'error': 'Missing vendor_name or search_query'}), 400
        
        manager = AffiliateManager()
        deep_link = manager.generate_deep_link(
            data['vendor_name'],
            data['search_query']
        )
        
        return jsonify({
            'vendor_name': data['vendor_name'],
            'search_query': data['search_query'],
            'deep_link': deep_link
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate deep link: {str(e)}'}), 500

@affiliate_bp.route('/programs', methods=['GET'])
def get_affiliate_programs():
    """Get all affiliate programs and their details"""
    try:
        manager = AffiliateManager()
        
        programs = []
        for vendor_name, config in manager.affiliate_configs.items():
            vendor = Vendor.query.filter_by(name=vendor_name).first()
            
            program_info = {
                'vendor_name': vendor_name,
                'base_url': config['base_url'],
                'commission_rate': config['commission_rate'],
                'status': 'active' if vendor and vendor.is_active else 'inactive'
            }
            
            if vendor:
                program_info.update({
                    'vendor_id': vendor.id,
                    'cookie_duration_days': vendor.cookie_duration_days,
                    'affiliate_program_id': vendor.affiliate_program_id
                })
            
            programs.append(program_info)
        
        return jsonify({
            'affiliate_programs': programs
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get affiliate programs: {str(e)}'}), 500

@affiliate_bp.route('/programs/update', methods=['POST'])
def update_affiliate_programs():
    """Update affiliate programs in database"""
    try:
        manager = AffiliateManager()
        manager.update_affiliate_programs()
        
        return jsonify({
            'message': 'Affiliate programs updated successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to update affiliate programs: {str(e)}'}), 500

@affiliate_bp.route('/earnings/estimate', methods=['GET'])
def estimate_earnings():
    """Estimate potential earnings based on clicks and conversion rates"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get click data
        start_date = datetime.utcnow() - timedelta(days=days)
        
        earnings_by_vendor = db.session.query(
            Vendor.name,
            Vendor.base_commission_rate,
            db.func.count(ClickTracking.id).label('clicks')
        ).join(ProductVendor).join(ClickTracking).filter(
            ClickTracking.clicked_at >= start_date
        ).group_by(Vendor.name, Vendor.base_commission_rate).all()
        
        total_estimated_earnings = 0
        vendor_earnings = []
        
        for vendor_name, commission_rate, clicks in earnings_by_vendor:
            # Assumptions: 2% conversion rate, $50 average order value
            conversion_rate = 0.02
            avg_order_value = 50
            commission_decimal = (commission_rate or 0) / 100
            
            estimated_earnings = clicks * conversion_rate * avg_order_value * commission_decimal
            total_estimated_earnings += estimated_earnings
            
            vendor_earnings.append({
                'vendor_name': vendor_name,
                'clicks': clicks,
                'commission_rate': commission_rate,
                'estimated_earnings': round(estimated_earnings, 2)
            })
        
        return jsonify({
            'period_days': days,
            'total_estimated_earnings': round(total_estimated_earnings, 2),
            'vendor_breakdown': vendor_earnings,
            'assumptions': {
                'conversion_rate': '2%',
                'avg_order_value': '$50',
                'note': 'These are estimates based on industry averages'
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to estimate earnings: {str(e)}'}), 500

@affiliate_bp.route('/redirect/<int:product_vendor_id>', methods=['GET'])
def redirect_to_affiliate_link(product_vendor_id):
    """Redirect to affiliate link with tracking"""
    try:
        # Get session ID from query params or generate new one
        session_id = request.args.get('session_id') or str(uuid.uuid4())
        
        # Get user information
        user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        referrer = request.headers.get('Referer', '')
        
        # Track the click
        result = track_affiliate_click(
            product_vendor_id,
            session_id,
            user_ip,
            user_agent,
            referrer
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Return redirect response
        from flask import redirect
        return redirect(result['redirect_url'], code=302)
        
    except Exception as e:
        return jsonify({'error': f'Failed to redirect: {str(e)}'}), 500

