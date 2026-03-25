"""
CFO (Chief Financial Officer) Agent
Handles all financial strategy, reporting, and decision-making
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from core.base_agent import BaseAgent
import json
from datetime import datetime

class CFOAgent(BaseAgent):
    """
    CFO Agent - Autonomous financial management and strategy
    """
    
    def __init__(self):
        super().__init__(
            name="CFO",
            role="Chief Financial Officer",
            department="Finance"
        )
        self.financial_data = {
            "revenue": 0,
            "expenses": 0,
            "profit": 0,
            "cash_flow": []
        }
    
    def _execute_actions(self, actions, context):
        """
        Execute financial-specific actions
        """
        results = []
        
        for action in actions:
            if "financial_report" in action.lower():
                results.append(self.generate_financial_report())
            elif "analyze" in action.lower():
                results.append(self.analyze_financial_health())
            elif "forecast" in action.lower():
                results.append(self.create_forecast(context))
            elif "invoice" in action.lower():
                results.append(self.process_invoice(context))
            elif "payment" in action.lower():
                results.append(self.process_payment(context))
            else:
                results.append(f"Executed financial action: {action}")
        
        return results
    
    def generate_financial_report(self):
        """
        Generate comprehensive financial report
        """
        report = {
            "report_date": datetime.now().isoformat(),
            "revenue": self.financial_data["revenue"],
            "expenses": self.financial_data["expenses"],
            "profit": self.financial_data["profit"],
            "profit_margin": (self.financial_data["profit"] / self.financial_data["revenue"] * 100) if self.financial_data["revenue"] > 0 else 0,
            "cash_flow_summary": self.financial_data["cash_flow"][-10:]
        }
        
        return {
            "type": "financial_report",
            "data": report,
            "status": "completed"
        }
    
    def analyze_financial_health(self):
        """
        AI-powered financial health analysis
        """
        analysis_prompt = f"""Analyze this financial data and provide insights:
        
Revenue: R{self.financial_data['revenue']}
Expenses: R{self.financial_data['expenses']}
Profit: R{self.financial_data['profit']}

Provide:
1. Health assessment (Excellent/Good/Fair/Poor)
2. Key concerns
3. Recommendations for improvement
4. Growth opportunities

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CFO analyzing financial health."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return {
                "type": "financial_analysis",
                "data": analysis,
                "status": "completed"
            }
        except Exception as e:
            return {
                "type": "financial_analysis",
                "error": str(e),
                "status": "failed"
            }
    
    def create_forecast(self, context):
        """
        Create financial forecast based on current data and context
        """
        return {
            "type": "forecast",
            "data": {
                "next_month_revenue_projection": self.financial_data["revenue"] * 1.15,
                "confidence": "medium",
                "assumptions": ["15% growth based on current trajectory"]
            },
            "status": "completed"
        }
    
    def process_invoice(self, context):
        """
        Process and generate invoices
        """
        invoice_data = context.get("invoice_data", {})
        
        invoice = {
            "invoice_number": f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "date": datetime.now().isoformat(),
            "amount": invoice_data.get("amount", 0),
            "client": invoice_data.get("client", "Unknown"),
            "status": "generated"
        }
        
        # Update financial data
        self.financial_data["revenue"] += invoice_data.get("amount", 0)
        self.financial_data["profit"] = self.financial_data["revenue"] - self.financial_data["expenses"]
        
        return {
            "type": "invoice",
            "data": invoice,
            "status": "completed"
        }
    
    def process_payment(self, context):
        """
        Process incoming payments
        """
        payment_data = context.get("payment_data", {})
        
        payment = {
            "payment_id": f"PAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "amount": payment_data.get("amount", 0),
            "method": payment_data.get("method", "bank_transfer"),
            "status": "received",
            "timestamp": datetime.now().isoformat()
        }
        
        # Update cash flow
        self.financial_data["cash_flow"].append(payment)
        
        return {
            "type": "payment",
            "data": payment,
            "status": "completed"
        }
    
    def record_expense(self, amount, category, description):
        """
        Record business expense
        """
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        self.financial_data["expenses"] += amount
        self.financial_data["profit"] = self.financial_data["revenue"] - self.financial_data["expenses"]
        
        return expense
