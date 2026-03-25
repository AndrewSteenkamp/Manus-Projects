from src.models.user import db
from datetime import datetime
import json

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for hierarchical categories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100), index=True)
    model = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    image_url = db.Column(db.String(500))
    specifications = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product_vendors = db.relationship('ProductVendor', backref='product', lazy=True, cascade='all, delete-orphan')
    price_alerts = db.relationship('PriceAlert', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def get_specifications(self):
        """Parse specifications JSON string"""
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_specifications(self, specs_dict):
        """Set specifications from dictionary"""
        self.specifications = json.dumps(specs_dict) if specs_dict else None
    
    def get_best_price(self):
        """Get the lowest current price from all vendors"""
        if not self.product_vendors:
            return None
        
        active_vendors = [pv for pv in self.product_vendors if pv.is_active and pv.current_price]
        if not active_vendors:
            return None
            
        return min(pv.current_price for pv in active_vendors)
    
    def get_price_range(self):
        """Get price range (min, max) from all vendors"""
        if not self.product_vendors:
            return None, None
        
        active_vendors = [pv for pv in self.product_vendors if pv.is_active and pv.current_price]
        if not active_vendors:
            return None, None
        
        prices = [pv.current_price for pv in active_vendors]
        return min(prices), max(prices)
    
    def to_dict(self, include_vendors=True):
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'brand': self.brand,
            'model': self.model,
            'category_id': self.category_id,
            'image_url': self.image_url,
            'specifications': self.get_specifications(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_vendors:
            result['vendors'] = [pv.to_dict() for pv in self.product_vendors if pv.is_active]
            result['best_price'] = self.get_best_price()
            min_price, max_price = self.get_price_range()
            result['price_range'] = {'min': min_price, 'max': max_price}
        
        return result

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo_url = db.Column(db.String(500))
    affiliate_program_id = db.Column(db.Integer, db.ForeignKey('affiliate_programs.id'))
    base_commission_rate = db.Column(db.Numeric(5, 2))
    cookie_duration_days = db.Column(db.Integer, default=30)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product_vendors = db.relationship('ProductVendor', backref='vendor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'logo_url': self.logo_url,
            'affiliate_program_id': self.affiliate_program_id,
            'base_commission_rate': float(self.base_commission_rate) if self.base_commission_rate else None,
            'cookie_duration_days': self.cookie_duration_days,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProductVendor(db.Model):
    __tablename__ = 'product_vendors'
    
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    vendor_product_id = db.Column(db.String(100))
    product_url = db.Column(db.String(1000))
    affiliate_url = db.Column(db.String(1000))
    current_price = db.Column(db.Numeric(10, 2))
    original_price = db.Column(db.Numeric(10, 2))
    discount_percentage = db.Column(db.Numeric(5, 2))
    availability_status = db.Column(db.Enum('in_stock', 'out_of_stock', 'limited_stock', 'unknown', name='availability_status'))
    shipping_cost = db.Column(db.Numeric(8, 2))
    shipping_time = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    price_history = db.relationship('PriceHistory', backref='product_vendor', lazy=True, cascade='all, delete-orphan')
    click_tracking = db.relationship('ClickTracking', backref='product_vendor', lazy=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_product_vendor', 'product_id', 'vendor_id'),
        db.Index('idx_price', 'current_price'),
        db.Index('idx_last_updated', 'last_updated'),
    )
    
    def calculate_discount(self):
        """Calculate discount percentage if not already set"""
        if self.current_price and self.original_price and self.original_price > 0:
            discount = ((self.original_price - self.current_price) / self.original_price) * 100
            return round(discount, 2)
        return 0
    
    def get_total_price(self):
        """Get total price including shipping"""
        total = self.current_price or 0
        if self.shipping_cost:
            total += self.shipping_cost
        return total
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.name if self.vendor else None,
            'vendor_logo': self.vendor.logo_url if self.vendor else None,
            'vendor_product_id': self.vendor_product_id,
            'product_url': self.product_url,
            'affiliate_url': self.affiliate_url,
            'current_price': float(self.current_price) if self.current_price else None,
            'original_price': float(self.original_price) if self.original_price else None,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else self.calculate_discount(),
            'availability_status': self.availability_status,
            'shipping_cost': float(self.shipping_cost) if self.shipping_cost else None,
            'shipping_time': self.shipping_time,
            'total_price': float(self.get_total_price()),
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'is_active': self.is_active
        }

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    
    id = db.Column(db.BigInteger, primary_key=True)
    product_vendor_id = db.Column(db.BigInteger, db.ForeignKey('product_vendors.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2))
    discount_percentage = db.Column(db.Numeric(5, 2))
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_product_vendor_date', 'product_vendor_id', 'recorded_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_vendor_id': self.product_vendor_id,
            'price': float(self.price),
            'original_price': float(self.original_price) if self.original_price else None,
            'discount_percentage': float(self.discount_percentage) if self.discount_percentage else None,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }

class AffiliateProgram(db.Model):
    __tablename__ = 'affiliate_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    network = db.Column(db.String(100))
    commission_structure = db.Column(db.Text)  # JSON string
    tracking_domain = db.Column(db.String(200))
    api_endpoint = db.Column(db.String(500))
    api_key_encrypted = db.Column(db.String(500))
    terms_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    vendors = db.relationship('Vendor', backref='affiliate_program', lazy=True)
    
    def get_commission_structure(self):
        """Parse commission structure JSON string"""
        if self.commission_structure:
            try:
                return json.loads(self.commission_structure)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_commission_structure(self, structure_dict):
        """Set commission structure from dictionary"""
        self.commission_structure = json.dumps(structure_dict) if structure_dict else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'network': self.network,
            'commission_structure': self.get_commission_structure(),
            'tracking_domain': self.tracking_domain,
            'api_endpoint': self.api_endpoint,
            'terms_url': self.terms_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PriceAlert(db.Model):
    __tablename__ = 'price_alerts'
    
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'), nullable=False)
    target_price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_checked = db.Column(db.DateTime)
    alert_sent_at = db.Column(db.DateTime)
    
    # Indexes
    __table_args__ = (
        db.Index('idx_product_active', 'product_id', 'is_active'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'product_id': self.product_id,
            'target_price': float(self.target_price),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_checked': self.last_checked.isoformat() if self.last_checked else None,
            'alert_sent_at': self.alert_sent_at.isoformat() if self.alert_sent_at else None
        }

class ClickTracking(db.Model):
    __tablename__ = 'click_tracking'
    
    id = db.Column(db.BigInteger, primary_key=True)
    session_id = db.Column(db.String(100))
    product_vendor_id = db.Column(db.BigInteger, db.ForeignKey('product_vendors.id'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_ip = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer_url = db.Column(db.String(1000))
    conversion_tracked = db.Column(db.Boolean, default=False)
    commission_earned = db.Column(db.Numeric(8, 2))
    
    # Indexes
    __table_args__ = (
        db.Index('idx_session_product', 'session_id', 'product_vendor_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'product_vendor_id': self.product_vendor_id,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None,
            'user_ip': self.user_ip,
            'user_agent': self.user_agent,
            'referrer_url': self.referrer_url,
            'conversion_tracked': self.conversion_tracked,
            'commission_earned': float(self.commission_earned) if self.commission_earned else None
        }

