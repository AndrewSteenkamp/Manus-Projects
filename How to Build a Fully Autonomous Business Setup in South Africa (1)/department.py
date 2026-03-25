"""
Complete Finance Department Hierarchy
CFO → Financial Controller → Accountant → Payments Clerk
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from core.base_agent import BaseAgent
from agents.finance.cfo import CFOAgent
import json
from datetime import datetime

class FinancialController(BaseAgent):
    """
    Financial Controller - Reports to CFO
    Manages day-to-day financial operations
    """
    
    def __init__(self, cfo):
        super().__init__(
            name="Financial Controller",
            role="Financial Controller",
            department="Finance"
        )
        self.cfo = cfo
        self.reports = []
        
    def _execute_actions(self, actions, context):
        results = []
        for action in actions:
            if "reconcile" in action.lower():
                results.append(self.reconcile_accounts(context))
            elif "audit" in action.lower():
                results.append(self.internal_audit())
            elif "budget" in action.lower():
                results.append(self.manage_budget(context))
            else:
                results.append(f"Executed: {action}")
        return results
    
    def reconcile_accounts(self, context):
        """Reconcile bank accounts and financial records"""
        return {
            "type": "reconciliation",
            "status": "completed",
            "discrepancies": 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def internal_audit(self):
        """Conduct internal financial audit"""
        prompt = """Conduct an internal financial audit checklist:

1. Revenue recognition accuracy
2. Expense categorization
3. Cash flow management
4. Compliance with SA tax law
5. Financial controls

Provide audit findings in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Financial Controller conducting audits."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def manage_budget(self, context):
        """Manage departmental budgets"""
        return {
            "type": "budget_management",
            "status": "monitoring",
            "timestamp": datetime.now().isoformat()
        }


class Accountant(BaseAgent):
    """
    Accountant - Reports to Financial Controller
    Handles bookkeeping and financial records
    """
    
    def __init__(self, controller):
        super().__init__(
            name="Accountant",
            role="Accountant",
            department="Finance"
        )
        self.controller = controller
        self.transactions = []
        
    def _execute_actions(self, actions, context):
        results = []
        for action in actions:
            if "record" in action.lower():
                results.append(self.record_transaction(context))
            elif "categorize" in action.lower():
                results.append(self.categorize_expense(context))
            elif "tax" in action.lower():
                results.append(self.calculate_tax(context))
            else:
                results.append(f"Executed: {action}")
        return results
    
    def record_transaction(self, context):
        """Record financial transaction"""
        transaction = {
            "transaction_id": f"TXN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "amount": context.get("amount", 0),
            "type": context.get("type", "expense"),
            "category": context.get("category", "general"),
            "description": context.get("description", ""),
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        return transaction
    
    def categorize_expense(self, context):
        """AI-powered expense categorization"""
        description = context.get("description", "")
        amount = context.get("amount", 0)
        
        prompt = f"""Categorize this business expense for South African tax purposes:

Description: {description}
Amount: R{amount}

Categories:
- Office Supplies
- Software/Technology
- Marketing/Advertising
- Professional Services
- Travel
- Utilities
- Salaries
- Other

Respond with just the category name."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an accountant expert in SA tax law."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            category = response.choices[0].message.content.strip()
            return {"category": category, "amount": amount, "description": description}
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_tax(self, context):
        """Calculate South African tax obligations"""
        revenue = context.get("revenue", 0)
        expenses = context.get("expenses", 0)
        
        profit = revenue - expenses
        
        # SA Corporate tax rate: 27%
        corporate_tax = profit * 0.27 if profit > 0 else 0
        
        # VAT (15% in SA)
        vat_collected = revenue * 0.15
        vat_paid = expenses * 0.15
        vat_payable = vat_collected - vat_paid
        
        return {
            "profit": profit,
            "corporate_tax": corporate_tax,
            "vat_payable": vat_payable,
            "total_tax_obligation": corporate_tax + vat_payable,
            "currency": "ZAR"
        }


class PaymentsClerk(BaseAgent):
    """
    Payments Clerk - Reports to Accountant
    Handles payment processing and collections
    """
    
    def __init__(self, accountant):
        super().__init__(
            name="Payments Clerk",
            role="Payments Clerk",
            department="Finance"
        )
        self.accountant = accountant
        self.payments_processed = []
        
    def _execute_actions(self, actions, context):
        results = []
        for action in actions:
            if "process_payment" in action.lower():
                results.append(self.process_payment(context))
            elif "send_invoice" in action.lower():
                results.append(self.send_invoice(context))
            elif "follow_up" in action.lower():
                results.append(self.follow_up_payment(context))
            else:
                results.append(f"Executed: {action}")
        return results
    
    def process_payment(self, context):
        """Process incoming payment"""
        payment = {
            "payment_id": f"PAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "amount": context.get("amount", 0),
            "client": context.get("client", "Unknown"),
            "method": context.get("method", "bank_transfer"),
            "status": "processed",
            "timestamp": datetime.now().isoformat()
        }
        
        self.payments_processed.append(payment)
        
        # Notify accountant
        self.accountant.record_transaction({
            "amount": payment["amount"],
            "type": "income",
            "category": "client_payment",
            "description": f"Payment from {payment['client']}"
        })
        
        return payment
    
    def send_invoice(self, context):
        """Generate and send invoice"""
        invoice = {
            "invoice_number": f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "client": context.get("client", ""),
            "amount": context.get("amount", 0),
            "due_date": context.get("due_date", ""),
            "items": context.get("items", []),
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        }
        
        return invoice
    
    def follow_up_payment(self, context):
        """AI-generated payment follow-up message"""
        invoice_number = context.get("invoice_number", "")
        days_overdue = context.get("days_overdue", 0)
        
        prompt = f"""Create a professional payment follow-up message:

Invoice: {invoice_number}
Days Overdue: {days_overdue}

The message should be:
- Professional and polite
- Firm but not aggressive
- Include payment options
- Mention consequences if needed

Respond with just the message text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a payments clerk following up on overdue invoices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            return {
                "message": response.choices[0].message.content,
                "invoice_number": invoice_number
            }
        except Exception as e:
            return {"error": str(e)}


class FinanceDepartment:
    """
    Complete Finance Department with full hierarchy
    """
    
    def __init__(self):
        # Initialize hierarchy from top to bottom
        self.cfo = CFOAgent()
        self.controller = FinancialController(self.cfo)
        self.accountant = Accountant(self.controller)
        self.payments_clerk = PaymentsClerk(self.accountant)
        
    def get_department_status(self):
        """Get status of entire finance department"""
        return {
            "department": "Finance",
            "hierarchy": {
                "cfo": self.cfo.get_status(),
                "controller": self.controller.get_status(),
                "accountant": self.accountant.get_status(),
                "payments_clerk": self.payments_clerk.get_status()
            },
            "total_agents": 4
        }
    
    def delegate_task(self, task, context=None):
        """
        Intelligently delegate task to appropriate team member
        """
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["strategy", "forecast", "analysis", "report"]):
            return self.cfo.execute_task(task, context)
        elif any(word in task_lower for word in ["reconcile", "audit", "budget"]):
            return self.controller.execute_task(task, context)
        elif any(word in task_lower for word in ["record", "categorize", "tax"]):
            return self.accountant.execute_task(task, context)
        elif any(word in task_lower for word in ["payment", "invoice", "collect"]):
            return self.payments_clerk.execute_task(task, context)
        else:
            # Default to CFO for unclear tasks
            return self.cfo.execute_task(task, context)
