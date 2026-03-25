"""
Yoco Payment Integration for Siener AI
Handles subscription payments and user management
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YocoPayments:
    def __init__(self):
        self.secret_key = os.getenv('YOCO_SECRET_KEY', 'sk_test_your_secret_key_here')
        self.public_key = os.getenv('YOCO_PUBLIC_KEY', 'pk_test_your_public_key_here')
        self.base_url = 'https://online.yoco.com/v1'
        
        # Subscription plans (in cents - Yoco uses cents)
        self.plans = {
            'basic': {
                'name': 'Basic Plan',
                'price': 49900,  # R499.00 in cents
                'currency': 'ZAR',
                'features': [
                    'Daily market analysis',
                    'Basic AI predictions', 
                    'JSE stock coverage',
                    'Email alerts',
                    'Mobile access'
                ]
            },
            'professional': {
                'name': 'Professional Plan',
                'price': 99900,  # R999.00 in cents
                'currency': 'ZAR',
                'features': [
                    'Everything in Basic',
                    'Advanced ECM analysis',
                    'Global market coverage',
                    'Real-time alerts',
                    'Portfolio tracking',
                    'Priority support'
                ]
            },
            'enterprise': {
                'name': 'Enterprise Plan',
                'price': 249900,  # R2499.00 in cents
                'currency': 'ZAR',
                'features': [
                    'Everything in Professional',
                    'Custom indicators',
                    'API access',
                    'White-label options',
                    'Dedicated support',
                    'Custom integrations'
                ]
            }
        }
    
    def create_charge(self, amount_cents, currency, token, metadata=None):
        """
        Create a charge using Yoco API
        
        Args:
            amount_cents (int): Amount in cents (e.g., 49900 for R499.00)
            currency (str): Currency code (ZAR)
            token (str): Payment token from Yoco.js
            metadata (dict): Additional data to store with payment
        
        Returns:
            dict: Yoco API response
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.secret_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'amount': amount_cents,
                'currency': currency,
                'token': token
            }
            
            if metadata:
                payload['metadata'] = metadata
            
            response = requests.post(
                f'{self.base_url}/charges',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            return {
                'success': response.status_code == 201,
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'error': None if response.status_code == 201 else response.text
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'status_code': 0,
                'data': {},
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'data': {},
                'error': f'Unexpected error: {str(e)}'
            }
    
    def process_subscription_payment(self, plan_type, payment_token, user_email, user_name=None):
        """
        Process a subscription payment for a specific plan
        
        Args:
            plan_type (str): 'basic', 'professional', or 'enterprise'
            payment_token (str): Yoco payment token
            user_email (str): Customer email
            user_name (str): Customer name (optional)
        
        Returns:
            dict: Payment result with subscription details
        """
        try:
            if plan_type not in self.plans:
                return {
                    'success': False,
                    'error': f'Invalid plan type: {plan_type}',
                    'subscription': None
                }
            
            plan = self.plans[plan_type]
            
            # Metadata for the payment
            metadata = {
                'plan_type': plan_type,
                'plan_name': plan['name'],
                'user_email': user_email,
                'user_name': user_name or 'Unknown',
                'subscription_start': datetime.now().isoformat(),
                'subscription_end': (datetime.now() + timedelta(days=30)).isoformat(),
                'service': 'Siener AI'
            }
            
            # Process the payment
            result = self.create_charge(
                amount_cents=plan['price'],
                currency=plan['currency'],
                token=payment_token,
                metadata=metadata
            )
            
            if result['success']:
                # Create subscription record
                subscription = {
                    'id': result['data'].get('id'),
                    'user_email': user_email,
                    'user_name': user_name,
                    'plan_type': plan_type,
                    'plan_name': plan['name'],
                    'amount_paid': plan['price'] / 100,  # Convert back to rands
                    'currency': plan['currency'],
                    'status': 'active',
                    'start_date': datetime.now().isoformat(),
                    'end_date': (datetime.now() + timedelta(days=30)).isoformat(),
                    'payment_id': result['data'].get('id'),
                    'created_at': datetime.now().isoformat()
                }
                
                return {
                    'success': True,
                    'payment': result['data'],
                    'subscription': subscription,
                    'message': f'Successfully subscribed to {plan["name"]} for R{plan["price"]/100:.2f}'
                }
            else:
                return {
                    'success': False,
                    'error': result['error'],
                    'subscription': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Subscription processing error: {str(e)}',
                'subscription': None
            }
    
    def get_plan_details(self, plan_type):
        """Get details for a specific plan"""
        return self.plans.get(plan_type)
    
    def get_all_plans(self):
        """Get all available plans"""
        return self.plans
    
    def validate_payment_token(self, token):
        """
        Validate a Yoco payment token (basic validation)
        In production, you might want more sophisticated validation
        """
        if not token:
            return False
        
        # Basic token format validation
        # Yoco tokens typically start with 'tok_' for test or live tokens
        return isinstance(token, str) and len(token) > 10
    
    def format_amount_for_display(self, amount_cents):
        """Convert cents to Rand display format"""
        return f"R{amount_cents / 100:.2f}"

# Simple in-memory subscription storage (replace with database in production)
class SubscriptionManager:
    def __init__(self):
        self.subscriptions = {}
        self.users = {}
    
    def create_subscription(self, subscription_data):
        """Store a new subscription"""
        user_email = subscription_data['user_email']
        self.subscriptions[user_email] = subscription_data
        
        # Also store user info
        self.users[user_email] = {
            'email': user_email,
            'name': subscription_data.get('user_name', 'Unknown'),
            'plan_type': subscription_data['plan_type'],
            'status': 'active',
            'created_at': subscription_data['created_at']
        }
        
        return subscription_data
    
    def get_subscription(self, user_email):
        """Get subscription for a user"""
        return self.subscriptions.get(user_email)
    
    def is_subscription_active(self, user_email):
        """Check if user has active subscription"""
        subscription = self.get_subscription(user_email)
        if not subscription:
            return False
        
        # Check if subscription is still valid
        end_date = datetime.fromisoformat(subscription['end_date'])
        return datetime.now() < end_date and subscription['status'] == 'active'
    
    def get_user_plan(self, user_email):
        """Get user's current plan type"""
        subscription = self.get_subscription(user_email)
        return subscription['plan_type'] if subscription else None
    
    def cancel_subscription(self, user_email):
        """Cancel a user's subscription"""
        if user_email in self.subscriptions:
            self.subscriptions[user_email]['status'] = 'cancelled'
            return True
        return False
    
    def get_all_active_subscriptions(self):
        """Get all active subscriptions"""
        active = {}
        for email, sub in self.subscriptions.items():
            if self.is_subscription_active(email):
                active[email] = sub
        return active

# Global instances
yoco_payments = YocoPayments()
subscription_manager = SubscriptionManager()

def test_yoco_integration():
    """Test function to verify Yoco integration"""
    print("Testing Yoco Payment Integration...")
    
    # Test plan retrieval
    plans = yoco_payments.get_all_plans()
    print(f"Available plans: {list(plans.keys())}")
    
    # Test plan details
    basic_plan = yoco_payments.get_plan_details('basic')
    print(f"Basic plan: {basic_plan['name']} - {yoco_payments.format_amount_for_display(basic_plan['price'])}")
    
    # Test token validation
    valid_token = yoco_payments.validate_payment_token('tok_test_1234567890')
    invalid_token = yoco_payments.validate_payment_token('invalid')
    print(f"Token validation - Valid: {valid_token}, Invalid: {invalid_token}")
    
    print("Yoco integration test completed!")

if __name__ == "__main__":
    test_yoco_integration()
