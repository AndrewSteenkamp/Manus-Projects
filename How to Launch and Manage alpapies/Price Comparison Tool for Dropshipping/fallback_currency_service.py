"""
Fallback Currency Service for PricePulse
Provides currency conversion with hardcoded exchange rates when API fails
"""

from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FallbackCurrencyService:
    """Fallback currency service with static exchange rates"""
    
    def __init__(self):
        # Static exchange rates (USD as base)
        # These should be updated periodically in a real system
        self.exchange_rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73,
            'JPY': 110.0,
            'AUD': 1.35,
            'CAD': 1.25,
            'CHF': 0.88,
            'CNY': 7.2,
            'SEK': 9.5,
            'NZD': 1.45,
            'MXN': 18.5,
            'SGD': 1.32,
            'HKD': 7.8,
            'NOK': 9.8,
            'ZAR': 15.2,
            'TRY': 8.5,
            'BRL': 5.1,
            'INR': 74.5,
            'KRW': 1180.0,
            'RUB': 75.0
        }
        
        self.last_updated = datetime.now().isoformat()
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """
        Convert amount from one currency to another using static rates
        """
        try:
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            
            if from_currency == to_currency:
                return {
                    "original_amount": amount,
                    "converted_amount": amount,
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "exchange_rate": 1.0,
                    "conversion_date": self.last_updated,
                    "source": "fallback-static"
                }
            
            # Get exchange rates
            from_rate = self.exchange_rates.get(from_currency)
            to_rate = self.exchange_rates.get(to_currency)
            
            if not from_rate or not to_rate:
                logger.warning(f"Currency not supported: {from_currency} -> {to_currency}")
                return None
            
            # Convert via USD
            usd_amount = amount / from_rate
            converted_amount = usd_amount * to_rate
            exchange_rate = to_rate / from_rate
            
            return {
                "original_amount": amount,
                "converted_amount": round(converted_amount, 2),
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": round(exchange_rate, 4),
                "conversion_date": self.last_updated,
                "source": "fallback-static"
            }
            
        except Exception as e:
            logger.error(f"Error in fallback currency conversion: {e}")
            return None
    
    def get_supported_currencies(self):
        """Get list of supported currencies"""
        return list(self.exchange_rates.keys())
    
    def get_exchange_rates(self, base_currency: str = "USD"):
        """Get all exchange rates for a base currency"""
        base_currency = base_currency.upper()
        
        if base_currency not in self.exchange_rates:
            return None
        
        base_rate = self.exchange_rates[base_currency]
        rates = {}
        
        for currency, rate in self.exchange_rates.items():
            if currency != base_currency:
                rates[currency] = round(rate / base_rate, 4)
        
        return {
            "base_code": base_currency,
            "rates": rates,
            "last_updated": self.last_updated,
            "source": "fallback-static"
        }

# Global fallback currency service
fallback_currency_service = FallbackCurrencyService()

def test_fallback_currency():
    """Test the fallback currency service"""
    service = FallbackCurrencyService()
    
    # Test conversions
    tests = [
        (100, 'USD', 'EUR'),
        (100, 'EUR', 'USD'),
        (100, 'GBP', 'JPY'),
        (100, 'USD', 'USD'),
    ]
    
    print("Testing Fallback Currency Service")
    print("=" * 40)
    
    for amount, from_curr, to_curr in tests:
        result = service.convert_currency(amount, from_curr, to_curr)
        if result:
            print(f"{amount} {from_curr} = {result['converted_amount']} {to_curr} (rate: {result['exchange_rate']})")
        else:
            print(f"Failed to convert {amount} {from_curr} to {to_curr}")
    
    print(f"\nSupported currencies: {', '.join(service.get_supported_currencies())}")

if __name__ == "__main__":
    test_fallback_currency()
