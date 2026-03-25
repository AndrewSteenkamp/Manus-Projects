"""
Stripe Payment Integration Module
Handles subscription billing, payments, and customer management
"""

import stripe
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class StripePaymentProcessor:
    def __init__(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
        
    def create_customer(self, email: str, name: str = None) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={'source': 'socrates_ai'}
            )
            return {
                'success': True,
                'customer_id': customer.id,
                'customer': customer
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_subscription(self, customer_id: str, price_id: str, trial_days: int = 14) -> Dict[str, Any]:
        """Create a subscription with trial period"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                trial_period_days=trial_days,
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent']
            )
            
            return {
                'success': True,
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription"""
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return {
                'success': True,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_subscription_status(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription status and details"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'success': True,
                'status': subscription.status,
                'current_period_end': subscription.current_period_end,
                'trial_end': subscription.trial_end,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_pricing_plans(self):
        """Create pricing plans for Socrates AI"""
        plans = [
            {
                'name': 'Basic Plan',
                'price': 2900,  # $29.00 in cents
                'interval': 'month',
                'features': ['Daily market analysis', 'Basic ECM insights', 'Email support']
            },
            {
                'name': 'Professional Plan', 
                'price': 7900,  # $79.00 in cents
                'interval': 'month',
                'features': ['All Basic features', 'Real-time alerts', 'Advanced analytics', 'Priority support']
            },
            {
                'name': 'Enterprise Plan',
                'price': 19900,  # $199.00 in cents
                'interval': 'month',
                'features': ['All Professional features', 'Custom analysis', 'API access', 'Dedicated support']
            }
        ]
        
        created_plans = []
        for plan in plans:
            try:
                product = stripe.Product.create(
                    name=plan['name'],
                    description=f"Socrates AI {plan['name']} - {', '.join(plan['features'])}"
                )
                
                price = stripe.Price.create(
                    product=product.id,
                    unit_amount=plan['price'],
                    currency='usd',
                    recurring={'interval': plan['interval']}
                )
                
                created_plans.append({
                    'product_id': product.id,
                    'price_id': price.id,
                    'plan': plan
                })
            except stripe.error.StripeError as e:
                print(f"Error creating plan {plan['name']}: {e}")
        
        return created_plans

# South African Payment Integration (PayFast)
class PayFastProcessor:
    def __init__(self):
        self.merchant_id = os.getenv('PAYFAST_MERCHANT_ID')
        self.merchant_key = os.getenv('PAYFAST_MERCHANT_KEY')
        self.passphrase = os.getenv('PAYFAST_PASSPHRASE')
        self.sandbox = os.getenv('PAYFAST_SANDBOX', 'true').lower() == 'true'
        
    def create_payment_url(self, amount: float, item_name: str, customer_email: str) -> str:
        """Create PayFast payment URL for South African customers"""
        import hashlib
        import urllib.parse
        
        # PayFast payment data
        data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': 'https://your-domain.com/payment/success',
            'cancel_url': 'https://your-domain.com/payment/cancel',
            'notify_url': 'https://your-domain.com/payment/notify',
            'amount': f'{amount:.2f}',
            'item_name': item_name,
            'email_address': customer_email,
            'payment_method': 'cc'
        }
        
        # Create signature
        signature_string = '&'.join([f'{k}={urllib.parse.quote_plus(str(v))}' for k, v in sorted(data.items())])
        if self.passphrase:
            signature_string += f'&passphrase={urllib.parse.quote_plus(self.passphrase)}'
        
        signature = hashlib.md5(signature_string.encode()).hexdigest()
        data['signature'] = signature
        
        # Build payment URL
        base_url = 'https://sandbox.payfast.co.za/eng/process' if self.sandbox else 'https://www.payfast.co.za/eng/process'
        query_string = urllib.parse.urlencode(data)
        
        return f'{base_url}?{query_string}'

# Unified Payment Manager
class PaymentManager:
    def __init__(self):
        self.stripe = StripePaymentProcessor()
        self.payfast = PayFastProcessor()
    
    def process_payment(self, customer_data: Dict[str, Any], plan: str, country: str = 'US') -> Dict[str, Any]:
        """Process payment based on customer location"""
        if country.upper() == 'ZA':  # South Africa
            amount = self.get_plan_price_zar(plan)
            payment_url = self.payfast.create_payment_url(
                amount=amount,
                item_name=f'Socrates AI {plan} Plan',
                customer_email=customer_data['email']
            )
            return {
                'success': True,
                'payment_method': 'payfast',
                'payment_url': payment_url
            }
        else:  # International (Stripe)
            customer = self.stripe.create_customer(
                email=customer_data['email'],
                name=customer_data.get('name')
            )
            if customer['success']:
                price_id = self.get_stripe_price_id(plan)
                subscription = self.stripe.create_subscription(
                    customer_id=customer['customer_id'],
                    price_id=price_id
                )
                return {
                    'success': True,
                    'payment_method': 'stripe',
                    'subscription_id': subscription.get('subscription_id'),
                    'client_secret': subscription.get('client_secret')
                }
            return customer
    
    def get_plan_price_zar(self, plan: str) -> float:
        """Get plan price in South African Rand"""
        prices = {
            'basic': 499.00,      # ~$29 USD
            'professional': 1299.00,  # ~$79 USD  
            'enterprise': 3299.00     # ~$199 USD
        }
        return prices.get(plan.lower(), 499.00)
    
    def get_stripe_price_id(self, plan: str) -> str:
        """Get Stripe price ID for plan"""
        # These would be set after creating the plans
        price_ids = {
            'basic': 'price_basic_monthly',
            'professional': 'price_pro_monthly',
            'enterprise': 'price_enterprise_monthly'
        }
        return price_ids.get(plan.lower(), price_ids['basic'])

