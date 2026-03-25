"""
PayFast Payment Gateway Integration for South Africa
Handles payment processing, invoicing, and transaction tracking
"""

import hashlib
import urllib.parse
from datetime import datetime
import json

class PayFastGateway:
    """
    PayFast payment gateway integration
    Enables receiving payments from South African clients
    """
    
    def __init__(self, merchant_id=None, merchant_key=None, passphrase=None, sandbox=True):
        """
        Initialize PayFast gateway
        
        Args:
            merchant_id: Your PayFast merchant ID
            merchant_key: Your PayFast merchant key
            passphrase: Your PayFast passphrase (set in dashboard)
            sandbox: Use sandbox mode for testing (default: True)
        """
        self.merchant_id = merchant_id or "10000100"  # Sandbox default
        self.merchant_key = merchant_key or "46f0cd694581a"  # Sandbox default
        self.passphrase = passphrase or "jt7NOE43FZPn"  # Sandbox default
        self.sandbox = sandbox
        
        # URLs
        if sandbox:
            self.process_url = "https://sandbox.payfast.co.za/eng/process"
            self.validate_url = "https://sandbox.payfast.co.za/eng/query/validate"
        else:
            self.process_url = "https://www.payfast.co.za/eng/process"
            self.validate_url = "https://www.payfast.co.za/eng/query/validate"
        
        self.transactions = []
    
    def generate_signature(self, data_dict):
        """
        Generate MD5 signature for PayFast
        Required for security verification
        """
        # Remove signature if it exists
        data = {k: v for k, v in data_dict.items() if k != 'signature'}
        
        # Sort by key (PayFast requirement)
        sorted_data = sorted(data.items())
        
        # Create parameter string
        param_string = "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_data])
        
        # Add passphrase
        param_string += f"&passphrase={urllib.parse.quote_plus(self.passphrase)}"
        
        # Generate MD5 hash
        signature = hashlib.md5(param_string.encode()).hexdigest()
        
        return signature
    
    def create_payment_form_data(self, invoice_data):
        """
        Create payment form data for PayFast
        
        Args:
            invoice_data: Dict with invoice details
                - amount: Payment amount (float)
                - item_name: Name of item/service
                - item_description: Description
                - client_email: Client's email
                - client_name: Client's name
                - m_payment_id: Your internal payment ID
        
        Returns:
            Dict with form data including signature
        """
        # Base URL for notifications (in production, use your domain)
        base_url = invoice_data.get('base_url', 'https://yourdomain.com')
        
        # Build form data
        form_data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': f"{base_url}/payment/success",
            'cancel_url': f"{base_url}/payment/cancel",
            'notify_url': f"{base_url}/payment/notify",
            
            # Transaction details
            'm_payment_id': invoice_data.get('m_payment_id', f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"),
            'amount': f"{invoice_data['amount']:.2f}",
            'item_name': invoice_data['item_name'],
            'item_description': invoice_data.get('item_description', ''),
            
            # Client details
            'email_address': invoice_data['client_email'],
            'name_first': invoice_data.get('client_name', '').split()[0] if invoice_data.get('client_name') else 'Client',
            'name_last': ' '.join(invoice_data.get('client_name', '').split()[1:]) if len(invoice_data.get('client_name', '').split()) > 1 else '',
        }
        
        # Generate signature
        form_data['signature'] = self.generate_signature(form_data)
        
        return form_data
    
    def generate_payment_link(self, invoice_data):
        """
        Generate a payment link that clients can click
        
        Returns:
            Full payment URL with all parameters
        """
        form_data = self.create_payment_form_data(invoice_data)
        
        # Build query string
        query_params = urllib.parse.urlencode(form_data)
        payment_url = f"{self.process_url}?{query_params}"
        
        return payment_url
    
    def generate_payment_button_html(self, invoice_data):
        """
        Generate HTML form with Pay Now button
        
        Returns:
            HTML string for payment form
        """
        form_data = self.create_payment_form_data(invoice_data)
        
        html = f'''
        <form action="{self.process_url}" method="POST">
        '''
        
        for key, value in form_data.items():
            html += f'    <input type="hidden" name="{key}" value="{value}">\n'
        
        html += '''
            <button type="submit" style="background: #00A3E0; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
                Pay with PayFast
            </button>
        </form>
        '''
        
        return html
    
    def validate_itn(self, post_data):
        """
        Validate Instant Transaction Notification from PayFast
        Call this when PayFast sends notification to your notify_url
        
        Args:
            post_data: POST data received from PayFast
        
        Returns:
            Dict with validation result and transaction details
        """
        # Verify signature
        received_signature = post_data.get('signature', '')
        data_without_signature = {k: v for k, v in post_data.items() if k != 'signature'}
        calculated_signature = self.generate_signature(data_without_signature)
        
        if received_signature != calculated_signature:
            return {
                'valid': False,
                'error': 'Signature mismatch',
                'transaction': None
            }
        
        # Extract transaction details
        transaction = {
            'pf_payment_id': post_data.get('pf_payment_id'),
            'm_payment_id': post_data.get('m_payment_id'),
            'payment_status': post_data.get('payment_status'),
            'amount_gross': float(post_data.get('amount_gross', 0)),
            'amount_fee': float(post_data.get('amount_fee', 0)),
            'amount_net': float(post_data.get('amount_net', 0)),
            'item_name': post_data.get('item_name'),
            'client_email': post_data.get('email_address'),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store transaction
        self.transactions.append(transaction)
        
        return {
            'valid': True,
            'transaction': transaction
        }
    
    def get_transaction_history(self):
        """
        Get all processed transactions
        """
        return {
            'total_transactions': len(self.transactions),
            'total_revenue': sum(t['amount_net'] for t in self.transactions),
            'successful_payments': len([t for t in self.transactions if t['payment_status'] == 'COMPLETE']),
            'transactions': self.transactions
        }
    
    def create_invoice_with_payment(self, client_info, items, due_date=None):
        """
        Create a complete invoice with PayFast payment link
        
        Args:
            client_info: Dict with client details (name, email, company)
            items: List of items/services with amount
            due_date: Payment due date
        
        Returns:
            Invoice dict with payment link
        """
        # Calculate total
        total_amount = sum(item.get('amount', 0) for item in items)
        
        # Create invoice
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        invoice = {
            'invoice_number': invoice_number,
            'client': client_info,
            'items': items,
            'total_amount': total_amount,
            'currency': 'ZAR',
            'due_date': due_date or datetime.now().isoformat(),
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        # Generate payment link
        payment_data = {
            'm_payment_id': invoice_number,
            'amount': total_amount,
            'item_name': f"Invoice {invoice_number}",
            'item_description': f"{len(items)} item(s)",
            'client_email': client_info['email'],
            'client_name': client_info['name']
        }
        
        invoice['payment_link'] = self.generate_payment_link(payment_data)
        invoice['payment_button_html'] = self.generate_payment_button_html(payment_data)
        
        return invoice
    
    def get_setup_instructions(self):
        """
        Get instructions for setting up PayFast account
        """
        return {
            'title': 'PayFast Setup Instructions for South Africa',
            'steps': [
                {
                    'step': 1,
                    'title': 'Create PayFast Account',
                    'description': 'Visit https://www.payfast.co.za and sign up for a business account',
                    'requirements': ['Valid SA ID or company registration', 'Business bank account', 'Email and phone number']
                },
                {
                    'step': 2,
                    'title': 'Complete FICA Verification',
                    'description': 'Upload required documents for FICA compliance',
                    'documents': ['ID document', 'Proof of address', 'Bank statement']
                },
                {
                    'step': 3,
                    'title': 'Configure Settings',
                    'description': 'Set up your merchant profile and security settings',
                    'actions': ['Set passphrase', 'Configure notify URL', 'Set return URLs']
                },
                {
                    'step': 4,
                    'title': 'Get Credentials',
                    'description': 'Copy your Merchant ID and Merchant Key from dashboard',
                    'location': 'Settings > Integration'
                },
                {
                    'step': 5,
                    'title': 'Test Integration',
                    'description': 'Use sandbox mode to test payments before going live',
                    'sandbox_url': 'https://sandbox.payfast.co.za'
                }
            ],
            'fees': {
                'setup': 'Free',
                'monthly': 'Free',
                'transaction': '2.9% + R2.00 per transaction (standard)',
                'settlement': '1-2 business days'
            },
            'support': {
                'email': 'support@payfast.co.za',
                'phone': '+27 21 813 9810',
                'docs': 'https://developers.payfast.co.za'
            }
        }


class FNBBankingIntegration:
    """
    FNB Business Banking Integration
    For automated reconciliation and direct banking
    """
    
    def __init__(self):
        self.api_key = None
        self.account_number = None
        
    def get_setup_guide(self):
        """
        Guide for setting up FNB business banking integration
        """
        return {
            'title': 'FNB Business Banking Setup Guide',
            'overview': 'FNB offers API and Host-to-Host services for automated banking',
            'steps': [
                {
                    'step': 1,
                    'title': 'Open FNB Business Account',
                    'description': 'Visit FNB branch or apply online',
                    'url': 'https://www.fnb.co.za/business/accounts.html',
                    'requirements': ['Company registration (CIPC)', 'FICA documents', 'Proof of business address']
                },
                {
                    'step': 2,
                    'title': 'Register for FNB Business Online',
                    'description': 'Activate online banking for your business account',
                    'features': ['View balances', 'Make payments', 'Download statements']
                },
                {
                    'step': 3,
                    'title': 'Apply for API Access',
                    'description': 'Contact FNB Integration Channel team',
                    'contact': 'https://www.fnb.co.za/integration-channel/',
                    'note': 'API access typically for medium to large businesses'
                },
                {
                    'step': 4,
                    'title': 'Integrate Payment Gateway',
                    'description': 'Link PayFast to your FNB account for automatic settlements',
                    'benefit': 'Payments from PayFast settle directly to FNB account'
                }
            ],
            'benefits': [
                'Automated reconciliation',
                'Real-time balance checks',
                'Bulk payments',
                'Direct API access'
            ],
            'user_action_required': 'You mentioned you will handle FNB business account setup yourself'
        }
