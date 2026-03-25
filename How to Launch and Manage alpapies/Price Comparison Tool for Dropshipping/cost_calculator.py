"""
Cost Calculator Service for PricePulse
Calculates total landed cost including shipping, VAT, import duties, and other hidden costs
"""

import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ShippingMethod(Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    OVERNIGHT = "overnight"
    FREE = "free"

@dataclass
class ProductInfo:
    """Product information for cost calculation"""
    price: float
    currency: str
    category: str
    weight: float = 0.0  # in kg
    dimensions: Dict[str, float] = None  # length, width, height in cm
    origin_country: str = "US"
    vendor: str = ""

@dataclass
class ShippingInfo:
    """Shipping information"""
    destination_country: str
    destination_region: str = ""
    shipping_method: ShippingMethod = ShippingMethod.STANDARD
    is_remote_area: bool = False

@dataclass
class CostBreakdown:
    """Complete cost breakdown"""
    base_price: float
    base_currency: str
    shipping_cost: float
    vat_amount: float
    import_duty: float
    handling_fee: float
    insurance_fee: float
    total_cost: float
    target_currency: str
    exchange_rate: float = 1.0
    cost_components: Dict[str, float] = None

class CostCalculator:
    """Service for calculating total landed costs including all hidden fees"""
    
    def __init__(self):
        self.vat_rates = self._load_vat_rates()
        self.import_duty_rates = self._load_import_duty_rates()
        self.shipping_rates = self._load_shipping_rates()
        self.country_info = self._load_country_info()
    
    def calculate_total_cost(self, product: ProductInfo, shipping: ShippingInfo, 
                           target_currency: str = "USD") -> CostBreakdown:
        """
        Calculate the total landed cost for a product including all fees
        """
        try:
            # Base calculations
            base_price = product.price
            
            # Calculate shipping cost
            shipping_cost = self._calculate_shipping_cost(product, shipping)
            
            # Calculate subtotal before taxes
            subtotal = base_price + shipping_cost
            
            # Calculate VAT/Sales Tax
            vat_amount = self._calculate_vat(subtotal, shipping.destination_country, product.category)
            
            # Calculate import duty
            import_duty = self._calculate_import_duty(base_price, product, shipping.destination_country)
            
            # Calculate handling and processing fees
            handling_fee = self._calculate_handling_fee(subtotal, shipping.destination_country)
            
            # Calculate insurance fee
            insurance_fee = self._calculate_insurance_fee(base_price, shipping.shipping_method)
            
            # Calculate total
            total_cost = subtotal + vat_amount + import_duty + handling_fee + insurance_fee
            
            # Prepare cost components
            cost_components = {
                "base_price": base_price,
                "shipping": shipping_cost,
                "vat_tax": vat_amount,
                "import_duty": import_duty,
                "handling_fee": handling_fee,
                "insurance": insurance_fee
            }
            
            return CostBreakdown(
                base_price=base_price,
                base_currency=product.currency,
                shipping_cost=shipping_cost,
                vat_amount=vat_amount,
                import_duty=import_duty,
                handling_fee=handling_fee,
                insurance_fee=insurance_fee,
                total_cost=total_cost,
                target_currency=target_currency,
                cost_components=cost_components
            )
            
        except Exception as e:
            logger.error(f"Error calculating total cost: {e}")
            # Return basic breakdown with just base price
            return CostBreakdown(
                base_price=base_price,
                base_currency=product.currency,
                shipping_cost=0,
                vat_amount=0,
                import_duty=0,
                handling_fee=0,
                insurance_fee=0,
                total_cost=base_price,
                target_currency=target_currency,
                cost_components={"base_price": base_price}
            )
    
    def _calculate_shipping_cost(self, product: ProductInfo, shipping: ShippingInfo) -> float:
        """Calculate shipping cost based on product and destination"""
        
        # Get base shipping rate
        country_rates = self.shipping_rates.get(shipping.destination_country, {})
        base_rate = country_rates.get(shipping.shipping_method.value, 0)
        
        # Weight-based calculation
        weight_factor = max(1.0, product.weight / 0.5)  # Base rate for 0.5kg
        shipping_cost = base_rate * weight_factor
        
        # Remote area surcharge
        if shipping.is_remote_area:
            shipping_cost *= 1.5
        
        # Express shipping multiplier
        if shipping.shipping_method == ShippingMethod.EXPRESS:
            shipping_cost *= 2.0
        elif shipping.shipping_method == ShippingMethod.OVERNIGHT:
            shipping_cost *= 3.0
        elif shipping.shipping_method == ShippingMethod.FREE:
            shipping_cost = 0
        
        return round(shipping_cost, 2)
    
    def _calculate_vat(self, amount: float, country: str, category: str) -> float:
        """Calculate VAT/Sales Tax"""
        vat_rate = self.vat_rates.get(country, {}).get(category, 0)
        if vat_rate == 0:
            vat_rate = self.vat_rates.get(country, {}).get("standard", 0)
        
        return round(amount * vat_rate, 2)
    
    def _calculate_import_duty(self, amount: float, product: ProductInfo, destination_country: str) -> float:
        """Calculate import duty based on product category and destination"""
        
        # No duty for domestic purchases
        if product.origin_country == destination_country:
            return 0
        
        # Get duty rate
        country_duties = self.import_duty_rates.get(destination_country, {})
        duty_rate = country_duties.get(product.category, 0)
        if duty_rate == 0:
            duty_rate = country_duties.get("general", 0)
        
        # Many countries have duty-free thresholds
        threshold = country_duties.get("threshold", 0)
        if amount <= threshold:
            return 0
        
        return round(amount * duty_rate, 2)
    
    def _calculate_handling_fee(self, amount: float, country: str) -> float:
        """Calculate handling and processing fees"""
        country_info = self.country_info.get(country, {})
        
        # Fixed handling fee
        fixed_fee = country_info.get("handling_fee", 0)
        
        # Percentage-based fee
        percentage_fee = amount * country_info.get("processing_fee_rate", 0)
        
        return round(fixed_fee + percentage_fee, 2)
    
    def _calculate_insurance_fee(self, amount: float, shipping_method: ShippingMethod) -> float:
        """Calculate insurance fee based on product value and shipping method"""
        
        # Insurance rates by shipping method
        insurance_rates = {
            ShippingMethod.STANDARD: 0.005,  # 0.5%
            ShippingMethod.EXPRESS: 0.008,   # 0.8%
            ShippingMethod.OVERNIGHT: 0.01,  # 1.0%
            ShippingMethod.FREE: 0.003       # 0.3%
        }
        
        rate = insurance_rates.get(shipping_method, 0.005)
        return round(amount * rate, 2)
    
    def _load_vat_rates(self) -> Dict:
        """Load VAT rates by country and category"""
        return {
            "US": {"standard": 0.0875, "electronics": 0.0875, "clothing": 0.08, "books": 0.0},
            "GB": {"standard": 0.20, "electronics": 0.20, "clothing": 0.20, "books": 0.0},
            "DE": {"standard": 0.19, "electronics": 0.19, "clothing": 0.19, "books": 0.07},
            "FR": {"standard": 0.20, "electronics": 0.20, "clothing": 0.20, "books": 0.055},
            "CA": {"standard": 0.13, "electronics": 0.13, "clothing": 0.13, "books": 0.05},
            "AU": {"standard": 0.10, "electronics": 0.10, "clothing": 0.10, "books": 0.10},
            "ZA": {"standard": 0.15, "electronics": 0.15, "clothing": 0.15, "books": 0.0},
            "JP": {"standard": 0.10, "electronics": 0.10, "clothing": 0.10, "books": 0.10},
            "CN": {"standard": 0.13, "electronics": 0.13, "clothing": 0.13, "books": 0.09},
            "IN": {"standard": 0.18, "electronics": 0.18, "clothing": 0.12, "books": 0.05},
            "BR": {"standard": 0.17, "electronics": 0.17, "clothing": 0.17, "books": 0.0},
            "MX": {"standard": 0.16, "electronics": 0.16, "clothing": 0.16, "books": 0.0}
        }
    
    def _load_import_duty_rates(self) -> Dict:
        """Load import duty rates by country and category"""
        return {
            "US": {"threshold": 800, "electronics": 0.0, "clothing": 0.12, "general": 0.05},
            "GB": {"threshold": 135, "electronics": 0.0, "clothing": 0.12, "general": 0.025},
            "DE": {"threshold": 150, "electronics": 0.0, "clothing": 0.12, "general": 0.04},
            "FR": {"threshold": 150, "electronics": 0.0, "clothing": 0.12, "general": 0.04},
            "CA": {"threshold": 200, "electronics": 0.0, "clothing": 0.18, "general": 0.065},
            "AU": {"threshold": 1000, "electronics": 0.0, "clothing": 0.10, "general": 0.05},
            "ZA": {"threshold": 500, "electronics": 0.15, "clothing": 0.45, "general": 0.20},
            "JP": {"threshold": 100, "electronics": 0.0, "clothing": 0.12, "general": 0.03},
            "CN": {"threshold": 50, "electronics": 0.13, "clothing": 0.16, "general": 0.10},
            "IN": {"threshold": 100, "electronics": 0.20, "clothing": 0.25, "general": 0.15},
            "BR": {"threshold": 50, "electronics": 0.60, "clothing": 0.35, "general": 0.20},
            "MX": {"threshold": 50, "electronics": 0.15, "clothing": 0.25, "general": 0.10}
        }
    
    def _load_shipping_rates(self) -> Dict:
        """Load base shipping rates by country (in USD)"""
        return {
            "US": {"standard": 5.99, "express": 12.99, "overnight": 25.99, "free": 0},
            "CA": {"standard": 8.99, "express": 18.99, "overnight": 35.99, "free": 0},
            "GB": {"standard": 12.99, "express": 24.99, "overnight": 45.99, "free": 0},
            "DE": {"standard": 11.99, "express": 22.99, "overnight": 42.99, "free": 0},
            "FR": {"standard": 12.99, "express": 24.99, "overnight": 45.99, "free": 0},
            "AU": {"standard": 15.99, "express": 29.99, "overnight": 55.99, "free": 0},
            "ZA": {"standard": 18.99, "express": 35.99, "overnight": 65.99, "free": 0},
            "JP": {"standard": 14.99, "express": 27.99, "overnight": 52.99, "free": 0},
            "CN": {"standard": 16.99, "express": 31.99, "overnight": 58.99, "free": 0},
            "IN": {"standard": 19.99, "express": 37.99, "overnight": 69.99, "free": 0},
            "BR": {"standard": 22.99, "express": 42.99, "overnight": 79.99, "free": 0},
            "MX": {"standard": 13.99, "express": 25.99, "overnight": 48.99, "free": 0}
        }
    
    def _load_country_info(self) -> Dict:
        """Load country-specific information"""
        return {
            "US": {"handling_fee": 2.50, "processing_fee_rate": 0.005},
            "CA": {"handling_fee": 3.50, "processing_fee_rate": 0.008},
            "GB": {"handling_fee": 4.00, "processing_fee_rate": 0.01},
            "DE": {"handling_fee": 3.50, "processing_fee_rate": 0.008},
            "FR": {"handling_fee": 4.00, "processing_fee_rate": 0.01},
            "AU": {"handling_fee": 5.00, "processing_fee_rate": 0.012},
            "ZA": {"handling_fee": 6.00, "processing_fee_rate": 0.015},
            "JP": {"handling_fee": 4.50, "processing_fee_rate": 0.01},
            "CN": {"handling_fee": 3.00, "processing_fee_rate": 0.006},
            "IN": {"handling_fee": 2.00, "processing_fee_rate": 0.004},
            "BR": {"handling_fee": 8.00, "processing_fee_rate": 0.02},
            "MX": {"handling_fee": 3.00, "processing_fee_rate": 0.008}
        }
    
    def get_cost_estimate_summary(self, product: ProductInfo, shipping: ShippingInfo) -> Dict:
        """Get a quick cost estimate summary"""
        breakdown = self.calculate_total_cost(product, shipping)
        
        return {
            "base_price": breakdown.base_price,
            "estimated_shipping": breakdown.shipping_cost,
            "estimated_taxes": breakdown.vat_amount + breakdown.import_duty,
            "estimated_fees": breakdown.handling_fee + breakdown.insurance_fee,
            "estimated_total": breakdown.total_cost,
            "currency": breakdown.base_currency,
            "savings_vs_local": 0,  # To be calculated by comparing with local prices
            "delivery_estimate": self._get_delivery_estimate(shipping.shipping_method)
        }
    
    def _get_delivery_estimate(self, shipping_method: ShippingMethod) -> str:
        """Get delivery time estimate"""
        estimates = {
            ShippingMethod.STANDARD: "7-14 business days",
            ShippingMethod.EXPRESS: "3-5 business days",
            ShippingMethod.OVERNIGHT: "1-2 business days",
            ShippingMethod.FREE: "10-21 business days"
        }
        return estimates.get(shipping_method, "7-14 business days")

# Global cost calculator instance
cost_calculator = CostCalculator()

