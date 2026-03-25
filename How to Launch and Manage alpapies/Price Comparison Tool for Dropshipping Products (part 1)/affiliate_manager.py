import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import requests
import json

from src.models.product import (
    db, Vendor, ProductVendor, AffiliateProgram, ClickTracking
)

class AffiliateManager:
    """Manages affiliate link generation and tracking for different platforms"""
    
    def __init__(self):
        self.affiliate_configs = {
            'Amazon': {
                'base_url': 'https://amazon.com',
                'associate_tag': 'pricecompare-20',  # Replace with actual associate tag
                'link_format': 'https://amazon.com/dp/{product_id}?tag={associate_tag}&linkCode=ogi&th=1&psc=1',
                'commission_rate': 4.0
            },
            'Temu': {
                'base_url': 'https://temu.com',
                'affiliate_id': 'your_temu_affiliate_id',  # Replace with actual ID
                'link_format': 'https://temu.com/ul?_bg_fs=1&_p_jump=0&_x_sessn_id=&goods_id={product_id}&sku_id=&adg_ctx=a-{affiliate_id}',
                'commission_rate': 15.0
            },
            'Shein': {
                'base_url': 'https://shein.com',
                'affiliate_id': 'your_shein_affiliate_id',  # Replace with actual ID
                'link_format': 'https://shein.com/product-{product_id}.html?ref={affiliate_id}',
                'commission_rate': 12.0
            }
        }
    
    def generate_affiliate_link(self, vendor_name: str, product_url: str, product_vendor_id: int) -> str:
        """Generate affiliate link for a specific vendor and product"""
        try:
            config = self.affiliate_configs.get(vendor_name)
            if not config:
                return product_url  # Return original URL if no affiliate config
            
            # Extract product ID from URL (simplified - would need platform-specific logic)
            product_id = self._extract_product_id(product_url, vendor_name)
            if not product_id:
                return product_url
            
            # Generate tracking parameters
            tracking_params = self._generate_tracking_params(product_vendor_id)
            
            # Build affiliate link based on platform
            if vendor_name == 'Amazon':
                affiliate_link = config['link_format'].format(
                    product_id=product_id,
                    associate_tag=config['associate_tag']
                )
            elif vendor_name == 'Temu':
                affiliate_link = config['link_format'].format(
                    product_id=product_id,
                    affiliate_id=config['affiliate_id']
                )
            elif vendor_name == 'Shein':
                affiliate_link = config['link_format'].format(
                    product_id=product_id,
                    affiliate_id=config['affiliate_id']
                )
            else:
                return product_url
            
            # Add tracking parameters
            if tracking_params:
                separator = '&' if '?' in affiliate_link else '?'
                affiliate_link += separator + tracking_params
            
            return affiliate_link
            
        except Exception as e:
            print(f"Error generating affiliate link for {vendor_name}: {str(e)}")
            return product_url
    
    def _extract_product_id(self, product_url: str, vendor_name: str) -> Optional[str]:
        """Extract product ID from product URL"""
        try:
            if vendor_name == 'Amazon':
                # Amazon ASIN extraction
                if '/dp/' in product_url:
                    return product_url.split('/dp/')[1].split('/')[0].split('?')[0]
                elif '/gp/product/' in product_url:
                    return product_url.split('/gp/product/')[1].split('/')[0].split('?')[0]
            
            elif vendor_name == 'Temu':
                # Temu product ID extraction
                if 'goods_id=' in product_url:
                    return product_url.split('goods_id=')[1].split('&')[0]
                elif '/product-' in product_url:
                    return product_url.split('/product-')[1].split('.')[0]
            
            elif vendor_name == 'Shein':
                # Shein product ID extraction
                if '/product-' in product_url:
                    return product_url.split('/product-')[1].split('.')[0]
                elif 'goods_id=' in product_url:
                    return product_url.split('goods_id=')[1].split('&')[0]
            
            return None
            
        except Exception as e:
            print(f"Error extracting product ID from {product_url}: {str(e)}")
            return None
    
    def _generate_tracking_params(self, product_vendor_id: int) -> str:
        """Generate tracking parameters for affiliate links"""
        try:
            # Create tracking ID
            tracking_id = f"pc_{product_vendor_id}_{int(datetime.utcnow().timestamp())}"
            
            # Add UTM parameters for tracking
            params = {
                'utm_source': 'pricecompare',
                'utm_medium': 'affiliate',
                'utm_campaign': 'price_comparison',
                'utm_content': str(product_vendor_id),
                'pc_track': tracking_id
            }
            
            return urllib.parse.urlencode(params)
            
        except Exception as e:
            print(f"Error generating tracking params: {str(e)}")
            return ""
    
    def track_click(self, product_vendor_id: int, session_id: str, user_ip: str, user_agent: str, referrer: str) -> Dict:
        """Track affiliate link clicks"""
        try:
            # Create click tracking record
            click = ClickTracking(
                session_id=session_id,
                product_vendor_id=product_vendor_id,
                user_ip=user_ip,
                user_agent=user_agent,
                referrer_url=referrer,
                clicked_at=datetime.utcnow()
            )
            
            db.session.add(click)
            db.session.commit()
            
            # Get the product vendor info
            product_vendor = ProductVendor.query.get(product_vendor_id)
            if not product_vendor:
                return {'error': 'Product vendor not found'}
            
            # Generate or get affiliate link
            affiliate_link = product_vendor.affiliate_url
            if not affiliate_link:
                affiliate_link = self.generate_affiliate_link(
                    product_vendor.vendor.name,
                    product_vendor.product_url,
                    product_vendor_id
                )
                # Update the database with the generated link
                product_vendor.affiliate_url = affiliate_link
                db.session.commit()
            
            return {
                'success': True,
                'click_id': click.id,
                'redirect_url': affiliate_link,
                'tracking_id': f"pc_{product_vendor_id}_{click.id}"
            }
            
        except Exception as e:
            db.session.rollback()
            print(f"Error tracking click: {str(e)}")
            return {'error': str(e)}
    
    def get_click_analytics(self, days: int = 30) -> Dict:
        """Get click analytics for the specified period"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get total clicks
            total_clicks = ClickTracking.query.filter(
                ClickTracking.clicked_at >= start_date
            ).count()
            
            # Get clicks by vendor
            clicks_by_vendor = db.session.query(
                Vendor.name,
                db.func.count(ClickTracking.id).label('clicks')
            ).join(ProductVendor).join(ClickTracking).filter(
                ClickTracking.clicked_at >= start_date
            ).group_by(Vendor.name).all()
            
            # Get daily clicks
            daily_clicks = db.session.query(
                db.func.date(ClickTracking.clicked_at).label('date'),
                db.func.count(ClickTracking.id).label('clicks')
            ).filter(
                ClickTracking.clicked_at >= start_date
            ).group_by(db.func.date(ClickTracking.clicked_at)).all()
            
            # Calculate estimated earnings (simplified)
            estimated_earnings = 0
            for vendor_name, clicks in clicks_by_vendor:
                config = self.affiliate_configs.get(vendor_name, {})
                commission_rate = config.get('commission_rate', 0)
                # Assume average order value of $50 and 2% conversion rate
                estimated_earnings += clicks * 0.02 * 50 * (commission_rate / 100)
            
            return {
                'total_clicks': total_clicks,
                'clicks_by_vendor': [{'vendor': name, 'clicks': clicks} for name, clicks in clicks_by_vendor],
                'daily_clicks': [{'date': str(date), 'clicks': clicks} for date, clicks in daily_clicks],
                'estimated_earnings': round(estimated_earnings, 2),
                'period_days': days
            }
            
        except Exception as e:
            print(f"Error getting click analytics: {str(e)}")
            return {'error': str(e)}
    
    def update_affiliate_programs(self):
        """Update affiliate program information in the database"""
        try:
            for vendor_name, config in self.affiliate_configs.items():
                # Get or create vendor
                vendor = Vendor.query.filter_by(name=vendor_name).first()
                if not vendor:
                    continue
                
                # Get or create affiliate program
                affiliate_program = AffiliateProgram.query.filter_by(name=f"{vendor_name} Affiliate Program").first()
                if not affiliate_program:
                    affiliate_program = AffiliateProgram(
                        name=f"{vendor_name} Affiliate Program",
                        network="Direct",
                        tracking_domain=config['base_url']
                    )
                    db.session.add(affiliate_program)
                    db.session.flush()
                
                # Update commission structure
                commission_structure = {
                    'base_rate': config['commission_rate'],
                    'currency': 'USD',
                    'type': 'percentage'
                }
                affiliate_program.set_commission_structure(commission_structure)
                
                # Link vendor to affiliate program
                vendor.affiliate_program_id = affiliate_program.id
                vendor.base_commission_rate = config['commission_rate']
            
            db.session.commit()
            print("Affiliate programs updated successfully")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error updating affiliate programs: {str(e)}")
    
    def generate_deep_link(self, vendor_name: str, search_query: str) -> str:
        """Generate deep links for search queries on specific platforms"""
        try:
            config = self.affiliate_configs.get(vendor_name)
            if not config:
                return f"https://{vendor_name.lower()}.com"
            
            encoded_query = urllib.parse.quote_plus(search_query)
            
            if vendor_name == 'Amazon':
                return f"https://amazon.com/s?k={encoded_query}&tag={config['associate_tag']}&linkCode=ur2"
            elif vendor_name == 'Temu':
                return f"https://temu.com/search_result.html?search_key={encoded_query}&refer_page_el_sn=200001&refer_page_name=home&refer_page_id=10005_1644490829988_hc7ywdkj5k"
            elif vendor_name == 'Shein':
                return f"https://shein.com/search/{encoded_query}?ref={config['affiliate_id']}"
            
            return config['base_url']
            
        except Exception as e:
            print(f"Error generating deep link for {vendor_name}: {str(e)}")
            return f"https://{vendor_name.lower()}.com"

# Utility functions
def initialize_affiliate_manager():
    """Initialize affiliate manager and update programs"""
    manager = AffiliateManager()
    manager.update_affiliate_programs()
    return manager

def get_affiliate_link(product_vendor_id: int) -> str:
    """Get or generate affiliate link for a product vendor"""
    try:
        product_vendor = ProductVendor.query.get(product_vendor_id)
        if not product_vendor:
            return ""
        
        if product_vendor.affiliate_url:
            return product_vendor.affiliate_url
        
        manager = AffiliateManager()
        affiliate_link = manager.generate_affiliate_link(
            product_vendor.vendor.name,
            product_vendor.product_url,
            product_vendor_id
        )
        
        # Save the generated link
        product_vendor.affiliate_url = affiliate_link
        db.session.commit()
        
        return affiliate_link
        
    except Exception as e:
        print(f"Error getting affiliate link: {str(e)}")
        return ""

def track_affiliate_click(product_vendor_id: int, session_id: str, user_ip: str, user_agent: str, referrer: str) -> Dict:
    """Track affiliate click and return redirect URL"""
    manager = AffiliateManager()
    return manager.track_click(product_vendor_id, session_id, user_ip, user_agent, referrer)

