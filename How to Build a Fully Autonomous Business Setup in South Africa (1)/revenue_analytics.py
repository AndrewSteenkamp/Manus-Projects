"""
Revenue Tracking and Financial Management System
Real-time analytics and forecasting for business performance
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from datetime import datetime, timedelta
import json
from openai import OpenAI

class RevenueAnalytics:
    """
    Comprehensive revenue tracking and business analytics
    """
    
    def __init__(self, cfo, crm, service_delivery):
        self.client = OpenAI()
        self.cfo = cfo
        self.crm = crm
        self.service_delivery = service_delivery
        self.revenue_events = []
        
    def record_revenue_event(self, event_type, amount, source, details=None):
        """
        Record a revenue-generating event
        """
        event = {
            "event_id": f"REV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "type": event_type,  # payment, invoice, refund, etc.
            "amount": amount,
            "source": source,  # client_id or lead_id
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
            "currency": "ZAR"
        }
        
        self.revenue_events.append(event)
        
        # Update CFO financial data
        if event_type == "payment":
            self.cfo.financial_data["revenue"] += amount
            self.cfo.financial_data["profit"] = self.cfo.financial_data["revenue"] - self.cfo.financial_data["expenses"]
        
        return event
    
    def get_revenue_dashboard(self):
        """
        Generate comprehensive revenue dashboard
        """
        # Calculate key metrics
        total_revenue = sum(e["amount"] for e in self.revenue_events if e["type"] == "payment")
        
        # Revenue by time period
        today_revenue = self._calculate_period_revenue(days=1)
        week_revenue = self._calculate_period_revenue(days=7)
        month_revenue = self._calculate_period_revenue(days=30)
        
        # Client metrics
        pipeline_stats = self.crm.get_pipeline_stats()
        delivery_metrics = self.service_delivery.get_delivery_metrics()
        
        # Financial health
        financial_report = self.cfo.generate_financial_report()
        
        dashboard = {
            "overview": {
                "total_revenue": total_revenue,
                "today": today_revenue,
                "this_week": week_revenue,
                "this_month": month_revenue,
                "currency": "ZAR"
            },
            "sales_pipeline": pipeline_stats,
            "service_delivery": delivery_metrics,
            "financial_health": financial_report,
            "growth_rate": self._calculate_growth_rate(),
            "forecast": self._generate_forecast(),
            "generated_at": datetime.now().isoformat()
        }
        
        return dashboard
    
    def _calculate_period_revenue(self, days):
        """Calculate revenue for a specific time period"""
        cutoff = datetime.now() - timedelta(days=days)
        
        period_events = [
            e for e in self.revenue_events
            if e["type"] == "payment" and datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
        
        return sum(e["amount"] for e in period_events)
    
    def _calculate_growth_rate(self):
        """Calculate month-over-month growth rate"""
        current_month = self._calculate_period_revenue(days=30)
        previous_month = self._calculate_period_revenue_offset(days=30, offset_days=30)
        
        if previous_month == 0:
            return "N/A - Insufficient data"
        
        growth = ((current_month - previous_month) / previous_month) * 100
        
        return f"{growth:+.1f}%"
    
    def _calculate_period_revenue_offset(self, days, offset_days):
        """Calculate revenue for a period in the past"""
        end_date = datetime.now() - timedelta(days=offset_days)
        start_date = end_date - timedelta(days=days)
        
        period_events = [
            e for e in self.revenue_events
            if e["type"] == "payment" and start_date <= datetime.fromisoformat(e["timestamp"]) <= end_date
        ]
        
        return sum(e["amount"] for e in period_events)
    
    def _generate_forecast(self):
        """AI-powered revenue forecast"""
        current_revenue = self._calculate_period_revenue(days=30)
        pipeline_value = sum(
            self.crm.leads[lead_id].get("estimated_value", 0)
            for lead_id in self.crm.leads
            if self.crm.leads[lead_id]["status"] in ["proposal_sent", "negotiating"]
        )
        
        prompt = f"""Generate revenue forecast:

Current Month Revenue: R{current_revenue}
Pipeline Value: R{pipeline_value}
Active Leads: {len(self.crm.leads)}
Conversion Rate: {self.crm.get_pipeline_stats().get('conversion_rate', '0%')}

Forecast next 3 months with:
1. Conservative estimate
2. Expected estimate
3. Optimistic estimate
4. Key assumptions
5. Risk factors

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a financial forecasting expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            forecast = json.loads(response.choices[0].message.content)
            forecast["generated_at"] = datetime.now().isoformat()
            
            return forecast
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_client_lifetime_value(self, client_id):
        """Calculate CLV for a client"""
        if client_id not in self.crm.clients:
            return {"error": "Client not found"}
        
        client = self.crm.clients[client_id]
        
        # Calculate actual revenue from this client
        client_revenue = sum(
            e["amount"] for e in self.revenue_events
            if e["source"] == client_id and e["type"] == "payment"
        )
        
        # AI predicts future value
        prompt = f"""Predict client lifetime value:

Current Revenue: R{client_revenue}
Client Since: {client['converted_at']}
Service Type: {client.get('service_type', 'Unknown')}

Estimate:
1. Projected additional revenue
2. Retention probability
3. Upsell opportunities
4. Total CLV

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a CLV prediction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            clv_prediction = json.loads(response.choices[0].message.content)
            clv_prediction["current_revenue"] = client_revenue
            
            return clv_prediction
        except Exception as e:
            return {"error": str(e)}
    
    def generate_financial_insights(self):
        """AI-generated business insights"""
        dashboard = self.get_revenue_dashboard()
        
        prompt = f"""Analyze business performance and provide insights:

Revenue: R{dashboard['overview']['total_revenue']}
This Month: R{dashboard['overview']['this_month']}
Growth Rate: {dashboard['growth_rate']}
Active Leads: {dashboard['sales_pipeline']['total_leads']}
Conversion Rate: {dashboard['sales_pipeline']['conversion_rate']}
Active Projects: {dashboard['service_delivery']['active_projects']}

Provide:
1. Top 3 strengths
2. Top 3 concerns
3. Immediate action items
4. Strategic recommendations
5. Opportunities to explore

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a business strategy consultant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            insights = json.loads(response.choices[0].message.content)
            insights["generated_at"] = datetime.now().isoformat()
            
            return insights
        except Exception as e:
            return {"error": str(e)}
    
    def get_profitability_analysis(self):
        """Analyze profitability by service type, client, etc."""
        # Revenue by source
        revenue_by_client = {}
        for event in self.revenue_events:
            if event["type"] == "payment":
                client_id = event["source"]
                revenue_by_client[client_id] = revenue_by_client.get(client_id, 0) + event["amount"]
        
        # Sort by revenue
        top_clients = sorted(revenue_by_client.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Calculate margins
        total_revenue = self.cfo.financial_data["revenue"]
        total_expenses = self.cfo.financial_data["expenses"]
        profit_margin = (total_revenue - total_expenses) / total_revenue * 100 if total_revenue > 0 else 0
        
        return {
            "profit_margin": f"{profit_margin:.1f}%",
            "total_profit": total_revenue - total_expenses,
            "top_clients": [
                {
                    "client_id": client_id,
                    "revenue": revenue,
                    "percentage": f"{(revenue / total_revenue * 100):.1f}%" if total_revenue > 0 else "0%"
                }
                for client_id, revenue in top_clients
            ],
            "revenue_concentration": "Diversified" if len(top_clients) > 5 else "Concentrated"
        }
    
    def export_financial_report(self, format="json"):
        """Export comprehensive financial report"""
        report = {
            "report_date": datetime.now().isoformat(),
            "company": "Your Autonomous Business",
            "currency": "ZAR",
            "dashboard": self.get_revenue_dashboard(),
            "insights": self.generate_financial_insights(),
            "profitability": self.get_profitability_analysis(),
            "forecast": self._generate_forecast()
        }
        
        if format == "json":
            return report
        elif format == "summary":
            return self._generate_executive_summary(report)
        else:
            return report
    
    def _generate_executive_summary(self, report):
        """Generate executive summary of financial report"""
        prompt = f"""Create an executive summary of this financial report:

{json.dumps(report, indent=2)}

The summary should be:
1. 2-3 paragraphs
2. Highlight key metrics
3. Note important trends
4. Actionable insights

Respond with just the summary text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a CFO writing executive summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
