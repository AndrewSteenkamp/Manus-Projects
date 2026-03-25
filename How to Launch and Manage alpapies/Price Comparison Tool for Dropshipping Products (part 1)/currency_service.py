"""
Currency Service for PricePulse
Handles real-time currency conversion and exchange rate management
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging
from flask import current_app

logger = logging.getLogger(__name__)

class CurrencyService:
    """Service for handling currency conversion and exchange rates"""
    
    def __init__(self):
        self.base_url = "https://v6.exchangerate-api.com/v6"
        self.api_key = None  # Will be set from environment or config
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self.fallback_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies"
        
    def set_api_key(self, api_key: str):
        """Set the ExchangeRate-API key"""
        self.api_key = api_key
    
    def get_exchange_rates(self, base_currency: str = "USD") -> Optional[Dict]:
        """
        Get exchange rates for a base currency
        Returns cached data if available and fresh, otherwise fetches new data
        """
        cache_key = f"rates_{base_currency}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_duration:
                logger.info(f"Using cached exchange rates for {base_currency}")
                return cached_data
        
        # Fetch fresh data
        rates = self._fetch_exchange_rates(base_currency)
        if rates:
            self.cache[cache_key] = (rates, datetime.now())
            logger.info(f"Fetched and cached new exchange rates for {base_currency}")
        
        return rates
    
    def _fetch_exchange_rates(self, base_currency: str) -> Optional[Dict]:
        """Fetch exchange rates from primary API with fallback"""
        
        # Try primary API (ExchangeRate-API) if API key is available
        if self.api_key:
            try:
                url = f"{self.base_url}/{self.api_key}/latest/{base_currency}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get("result") == "success":
                    return {
                        "base_code": data["base_code"],
                        "rates": data["conversion_rates"],
                        "last_updated": data.get("time_last_update_utc"),
                        "source": "exchangerate-api"
                    }
            except Exception as e:
                logger.warning(f"Primary API failed: {e}, trying fallback")
        
        # Fallback to free API
        try:
            url = f"{self.fallback_url}/{base_currency.lower()}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Convert to uppercase keys for consistency
            rates = {k.upper(): v for k, v in data.get(base_currency.lower(), {}).items()}
            
            return {
                "base_code": base_currency.upper(),
                "rates": rates,
                "last_updated": datetime.now().isoformat(),
                "source": "fallback-api"
            }
        except Exception as e:
            logger.error(f"Fallback API also failed: {e}")
            return None
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[Dict]:
        """
        Convert amount from one currency to another
        Returns conversion details including rate and converted amount
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if from_currency == to_currency:
            return {
                "original_amount": amount,
                "converted_amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "exchange_rate": 1.0,
                "conversion_date": datetime.now().isoformat()
            }
        
        # Get exchange rates
        rates_data = self.get_exchange_rates(from_currency)
        if not rates_data:
            logger.error(f"Could not get exchange rates for {from_currency}")
            return None
        
        rates = rates_data["rates"]
        if to_currency not in rates:
            logger.error(f"Currency {to_currency} not found in rates")
            return None
        
        exchange_rate = rates[to_currency]
        converted_amount = amount * exchange_rate
        
        return {
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": exchange_rate,
            "conversion_date": rates_data.get("last_updated", datetime.now().isoformat()),
            "source": rates_data.get("source", "unknown")
        }
    
    def get_supported_currencies(self) -> List[str]:
        """Get list of supported currency codes"""
        rates_data = self.get_exchange_rates("USD")
        if rates_data and "rates" in rates_data:
            return list(rates_data["rates"].keys())
        
        # Fallback list of major currencies
        return [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
            "MXN", "SGD", "HKD", "NOK", "ZAR", "TRY", "BRL", "INR", "KRW", "RUB"
        ]
    
    def get_currency_info(self, currency_code: str) -> Dict:
        """Get information about a specific currency"""
        currency_info = {
            "USD": {"name": "US Dollar", "symbol": "$", "country": "United States"},
            "EUR": {"name": "Euro", "symbol": "€", "country": "European Union"},
            "GBP": {"name": "British Pound", "symbol": "£", "country": "United Kingdom"},
            "JPY": {"name": "Japanese Yen", "symbol": "¥", "country": "Japan"},
            "AUD": {"name": "Australian Dollar", "symbol": "A$", "country": "Australia"},
            "CAD": {"name": "Canadian Dollar", "symbol": "C$", "country": "Canada"},
            "CHF": {"name": "Swiss Franc", "symbol": "CHF", "country": "Switzerland"},
            "CNY": {"name": "Chinese Yuan", "symbol": "¥", "country": "China"},
            "ZAR": {"name": "South African Rand", "symbol": "R", "country": "South Africa"},
            "INR": {"name": "Indian Rupee", "symbol": "₹", "country": "India"},
            "BRL": {"name": "Brazilian Real", "symbol": "R$", "country": "Brazil"},
            "KRW": {"name": "South Korean Won", "symbol": "₩", "country": "South Korea"},
            "RUB": {"name": "Russian Ruble", "symbol": "₽", "country": "Russia"},
            "SGD": {"name": "Singapore Dollar", "symbol": "S$", "country": "Singapore"},
            "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "country": "Hong Kong"},
            "NOK": {"name": "Norwegian Krone", "symbol": "kr", "country": "Norway"},
            "SEK": {"name": "Swedish Krona", "symbol": "kr", "country": "Sweden"},
            "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "country": "New Zealand"},
            "MXN": {"name": "Mexican Peso", "symbol": "$", "country": "Mexico"},
            "TRY": {"name": "Turkish Lira", "symbol": "₺", "country": "Turkey"}
        }
        
        currency_code = currency_code.upper()
        return currency_info.get(currency_code, {
            "name": currency_code,
            "symbol": currency_code,
            "country": "Unknown"
        })
    
    def clear_cache(self):
        """Clear the exchange rate cache"""
        self.cache.clear()
        logger.info("Exchange rate cache cleared")
    
    def get_cache_status(self) -> Dict:
        """Get information about the current cache status"""
        cache_info = {}
        for key, (data, timestamp) in self.cache.items():
            age = datetime.now() - timestamp
            cache_info[key] = {
                "age_minutes": int(age.total_seconds() / 60),
                "expires_in_minutes": int((self.cache_duration - age).total_seconds() / 60),
                "is_expired": age > self.cache_duration,
                "base_currency": data.get("base_code"),
                "source": data.get("source")
            }
        return cache_info

# Global currency service instance
currency_service = CurrencyService()

