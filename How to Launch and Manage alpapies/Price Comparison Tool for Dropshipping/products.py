from flask import Blueprint, request, jsonify
from sqlalchemy import or_, and_, desc, asc
from src.models.product import (
    db, Product, Category, Vendor, ProductVendor, 
    PriceHistory, PriceAlert, ClickTracking
)
from datetime import datetime, timedelta
import uuid

products_bp = Blueprint('products', __name__)

@products_bp.route('/search', methods=['GET'])
def search_products():
    """Search for products across all vendors"""
    try:
        # Get query parameters
        query = request.args.get('q', '').strip()
        category_id = request.args.get('category', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        brands = request.args.get('brands', '').split(',') if request.args.get('brands') else []
        sort_by = request.args.get('sort', 'relevance')  # relevance, price_asc, price_desc, rating, popularity
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Validate parameters
        if not query and not category_id:
            return jsonify({'error': 'Search query or category is required'}), 400
        
        if limit > 100:
            limit = 100  # Prevent excessive results
        
        # Build base query
        products_query = Product.query
        
        # Apply filters
        if query:
            products_query = products_query.filter(
                or_(
                    Product.name.ilike(f'%{query}%'),
                    Product.description.ilike(f'%{query}%'),
                    Product.brand.ilike(f'%{query}%')
                )
            )
        
        if category_id:
            products_query = products_query.filter(Product.category_id == category_id)
        
        if brands:
            brands = [b.strip() for b in brands if b.strip()]
            if brands:
                products_query = products_query.filter(Product.brand.in_(brands))
        
        # Get products with active vendor relationships
        products_query = products_query.join(ProductVendor).filter(
            ProductVendor.is_active == True,
            ProductVendor.current_price.isnot(None)
        )
        
        # Apply price filters
        if min_price is not None:
            products_query = products_query.filter(ProductVendor.current_price >= min_price)
        
        if max_price is not None:
            products_query = products_query.filter(ProductVendor.current_price <= max_price)
        
        # Apply sorting
        if sort_by == 'price_asc':
            products_query = products_query.order_by(asc(ProductVendor.current_price))
        elif sort_by == 'price_desc':
            products_query = products_query.order_by(desc(ProductVendor.current_price))
        elif sort_by == 'rating':
            # For now, order by product name (can be enhanced with actual ratings)
            products_query = products_query.order_by(desc(Product.name))
        elif sort_by == 'popularity':
            # Order by most recent updates (proxy for popularity)
            products_query = products_query.order_by(desc(Product.updated_at))
        else:  # relevance (default)
            products_query = products_query.order_by(desc(Product.updated_at))
        
        # Get distinct products (avoid duplicates from joins)
        products_query = products_query.distinct(Product.id)
        
        # Pagination
        total_results = products_query.count()
        products = products_query.offset((page - 1) * limit).limit(limit).all()
        
        # Format results
        results = []
        for product in products:
            product_data = product.to_dict(include_vendors=True)
            
            # Calculate savings
            if product_data['vendors']:
                prices = [v['current_price'] for v in product_data['vendors'] if v['current_price']]
                if prices:
                    min_price_val = min(prices)
                    max_price_val = max(prices)
                    savings = max_price_val - min_price_val if len(prices) > 1 else 0
                    product_data['savings'] = round(savings, 2)
                else:
                    product_data['savings'] = 0
            else:
                product_data['savings'] = 0
            
            results.append(product_data)
        
        return jsonify({
            'products': results,
            'total_results': total_results,
            'page': page,
            'limit': limit,
            'total_pages': (total_results + limit - 1) // limit,
            'query': query,
            'filters': {
                'category_id': category_id,
                'min_price': min_price,
                'max_price': max_price,
                'brands': brands,
                'sort_by': sort_by
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """Get detailed information about a specific product"""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Get price history for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        price_history = db.session.query(PriceHistory).join(ProductVendor).filter(
            ProductVendor.product_id == product_id,
            PriceHistory.recorded_at >= thirty_days_ago
        ).order_by(PriceHistory.recorded_at.asc()).all()
        
        # Format product data
        product_data = product.to_dict(include_vendors=True)
        
        # Add price history
        product_data['price_history'] = [ph.to_dict() for ph in price_history]
        
        # Add category information
        if product.category:
            product_data['category'] = product.category.to_dict()
        
        # Calculate additional metrics
        if product_data['vendors']:
            prices = [v['current_price'] for v in product_data['vendors'] if v['current_price']]
            if prices:
                product_data['price_stats'] = {
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'avg_price': round(sum(prices) / len(prices), 2),
                    'vendor_count': len(prices)
                }
        
        return jsonify(product_data)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get product details: {str(e)}'}), 500

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.all()
        return jsonify({
            'categories': [cat.to_dict() for cat in categories]
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get categories: {str(e)}'}), 500

@products_bp.route('/vendors', methods=['GET'])
def get_vendors():
    """Get all active vendors"""
    try:
        vendors = Vendor.query.filter(Vendor.is_active == True).all()
        return jsonify({
            'vendors': [vendor.to_dict() for vendor in vendors]
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get vendors: {str(e)}'}), 500

@products_bp.route('/alerts', methods=['POST'])
def create_price_alert():
    """Create a price alert for a product"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'product_id', 'target_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate product exists
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check if alert already exists
        existing_alert = PriceAlert.query.filter(
            PriceAlert.email == data['email'],
            PriceAlert.product_id == data['product_id'],
            PriceAlert.is_active == True
        ).first()
        
        if existing_alert:
            # Update existing alert
            existing_alert.target_price = data['target_price']
            existing_alert.created_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'message': 'Price alert updated successfully',
                'alert': existing_alert.to_dict()
            })
        else:
            # Create new alert
            alert = PriceAlert(
                email=data['email'],
                product_id=data['product_id'],
                target_price=data['target_price']
            )
            db.session.add(alert)
            db.session.commit()
            
            return jsonify({
                'message': 'Price alert created successfully',
                'alert': alert.to_dict()
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create price alert: {str(e)}'}), 500

@products_bp.route('/alerts/<email>', methods=['GET'])
def get_user_alerts(email):
    """Get all active price alerts for a user"""
    try:
        alerts = PriceAlert.query.filter(
            PriceAlert.email == email,
            PriceAlert.is_active == True
        ).all()
        
        # Include product information
        alerts_data = []
        for alert in alerts:
            alert_data = alert.to_dict()
            alert_data['product'] = alert.product.to_dict(include_vendors=False)
            alert_data['current_best_price'] = alert.product.get_best_price()
            alerts_data.append(alert_data)
        
        return jsonify({
            'alerts': alerts_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get alerts: {str(e)}'}), 500

@products_bp.route('/alerts/<int:alert_id>', methods=['DELETE'])
def delete_price_alert(alert_id):
    """Delete a price alert"""
    try:
        alert = PriceAlert.query.get_or_404(alert_id)
        alert.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Price alert deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete price alert: {str(e)}'}), 500

@products_bp.route('/track/click', methods=['POST'])
def track_click():
    """Track user clicks on affiliate links"""
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
        
        # Create click tracking record
        click = ClickTracking(
            session_id=session_id,
            product_vendor_id=data['product_vendor_id'],
            user_ip=user_ip,
            user_agent=user_agent,
            referrer_url=referrer
        )
        
        db.session.add(click)
        db.session.commit()
        
        # Get the affiliate URL to redirect to
        product_vendor = ProductVendor.query.get(data['product_vendor_id'])
        if not product_vendor:
            return jsonify({'error': 'Product vendor not found'}), 404
        
        return jsonify({
            'message': 'Click tracked successfully',
            'session_id': session_id,
            'redirect_url': product_vendor.affiliate_url or product_vendor.product_url,
            'click_id': click.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to track click: {str(e)}'}), 500

@products_bp.route('/trending', methods=['GET'])
def get_trending_products():
    """Get trending products based on recent activity"""
    try:
        limit = request.args.get('limit', 10, type=int)
        category_id = request.args.get('category', type=int)
        
        # Get products with recent price updates (proxy for trending)
        query = Product.query.join(ProductVendor).filter(
            ProductVendor.is_active == True,
            ProductVendor.current_price.isnot(None)
        )
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        # Order by most recent updates
        products = query.order_by(desc(ProductVendor.last_updated)).limit(limit).all()
        
        return jsonify({
            'trending_products': [product.to_dict(include_vendors=True) for product in products]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get trending products: {str(e)}'}), 500

@products_bp.route('/deals', methods=['GET'])
def get_best_deals():
    """Get products with the best discounts"""
    try:
        limit = request.args.get('limit', 10, type=int)
        min_discount = request.args.get('min_discount', 10, type=float)
        
        # Get products with significant discounts
        products = Product.query.join(ProductVendor).filter(
            ProductVendor.is_active == True,
            ProductVendor.current_price.isnot(None),
            ProductVendor.discount_percentage >= min_discount
        ).order_by(desc(ProductVendor.discount_percentage)).limit(limit).all()
        
        return jsonify({
            'best_deals': [product.to_dict(include_vendors=True) for product in products]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get best deals: {str(e)}'}), 500

@products_bp.route('/price-history/<int:product_id>', methods=['GET'])
def get_price_history(product_id):
    """Get price history for a specific product"""
    try:
        days = request.args.get('days', 30, type=int)
        vendor_id = request.args.get('vendor_id', type=int)
        
        # Validate product exists
        product = Product.query.get_or_404(product_id)
        
        # Build query
        start_date = datetime.utcnow() - timedelta(days=days)
        query = db.session.query(PriceHistory).join(ProductVendor).filter(
            ProductVendor.product_id == product_id,
            PriceHistory.recorded_at >= start_date
        )
        
        if vendor_id:
            query = query.filter(ProductVendor.vendor_id == vendor_id)
        
        price_history = query.order_by(PriceHistory.recorded_at.asc()).all()
        
        # Group by vendor for better visualization
        history_by_vendor = {}
        for ph in price_history:
            vendor_name = ph.product_vendor.vendor.name
            if vendor_name not in history_by_vendor:
                history_by_vendor[vendor_name] = []
            history_by_vendor[vendor_name].append(ph.to_dict())
        
        return jsonify({
            'product_id': product_id,
            'product_name': product.name,
            'days': days,
            'price_history': history_by_vendor
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get price history: {str(e)}'}), 500

