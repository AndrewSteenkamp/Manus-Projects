#!/usr/bin/env python3
"""
CFO Agent - Chief Financial Officer
Financial management, analysis, and strategic financial planning for the autonomous UGC advertising agency
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys
import os

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))
from ai_helper import AIHelper

class CFOAgent:
    """
    The CFO Agent manages all financial aspects of the autonomous advertising agency.
    
    Responsibilities:
    - Financial planning and budgeting
    - Revenue and expense tracking
    - Profitability analysis
    - Cash flow management
    - Financial reporting and dashboards
    - Investment analysis and ROI calculations
    - Risk assessment and financial controls
    - Pricing strategy optimization
    - Tax planning and compliance
    - Financial forecasting and modeling
    
    The CFO Agent ensures the financial health and growth of the organization
    through data-driven financial management and strategic planning.
    """
    
    def __init__(self, ai_provider: str = None):
        """
        Initialize the CFO Agent with AI capabilities.
        
        Args:
            ai_provider (str): Preferred AI provider for financial analysis
        """
        self.ai_helper = AIHelper(provider=ai_provider)
        self.agent_id = "CFO-001"
        self.name = "Marcus Chen"
        self.role = "Chief Financial Officer"
        
        # Financial configuration
        self.approval_threshold = 10000  # Maximum expense approval without CEO consent
        self.target_profit_margin = 85   # Target profit margin percentage
        self.cash_reserve_target = 0.3   # Target cash reserve as percentage of monthly revenue
        
        # Financial tracking
        self.financial_data = {
            "monthly_revenue": 0,
            "monthly_expenses": 0,
            "profit_margin": 0,
            "cash_flow": 0,
            "client_acquisition_cost": 0,
            "customer_lifetime_value": 0,
            "accounts_receivable": 0,
            "accounts_payable": 0
        }
        
        # Budget categories
        self.budget_categories = {
            "marketing": {"allocated": 20000, "spent": 0, "remaining": 20000},
            "technology": {"allocated": 15000, "spent": 0, "remaining": 15000},
            "operations": {"allocated": 10000, "spent": 0, "remaining": 10000},
            "personnel": {"allocated": 25000, "spent": 0, "remaining": 25000},
            "research_development": {"allocated": 8000, "spent": 0, "remaining": 8000}
        }
        
        # Financial history for trend analysis
        self.financial_history = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"CFO-{self.agent_id}")
        
        print(f"💰 CFO Agent '{self.name}' initialized")
        print(f"   Role: {self.role}")
        print(f"   AI Provider: {self.ai_helper.provider}")
        print(f"   Approval Authority: ${self.approval_threshold:,}")
        print(f"   Target Profit Margin: {self.target_profit_margin}%")
    
    def analyze_financial_performance(self) -> Dict[str, Any]:
        """
        Analyze current financial performance and provide insights.
        
        Returns:
            Dict: Financial analysis with insights and recommendations
        """
        self.logger.info("Analyzing financial performance")
        
        # Calculate key financial metrics
        revenue = self.financial_data["monthly_revenue"]
        expenses = self.financial_data["monthly_expenses"]
        profit = revenue - expenses
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        context_prompt = f"""
        As CFO, analyze the current financial performance of our UGC advertising agency:
        
        FINANCIAL METRICS:
        - Monthly Revenue: ${revenue:,}
        - Monthly Expenses: ${expenses:,}
        - Net Profit: ${profit:,}
        - Profit Margin: {profit_margin:.1f}%
        - Target Profit Margin: {self.target_profit_margin}%
        - Cash Flow: ${self.financial_data['cash_flow']:,}
        - Client Acquisition Cost: ${self.financial_data['client_acquisition_cost']:,}
        - Customer Lifetime Value: ${self.financial_data['customer_lifetime_value']:,}
        
        BUDGET UTILIZATION:
        {json.dumps(self.budget_categories, indent=2)}
        
        Provide analysis including:
        1. Performance assessment (EXCELLENT/GOOD/FAIR/POOR)
        2. Key strengths and concerns
        3. Profit margin analysis
        4. Cash flow assessment
        5. Budget efficiency evaluation
        6. Recommendations for improvement
        7. Risk factors to monitor
        8. Growth opportunities
        
        Respond in JSON format.
        """
        
        system_message = """You are Marcus Chen, a seasoned CFO with 12 years experience in digital agencies and SaaS companies. 
        You focus on sustainable profitability, efficient capital allocation, and data-driven financial decisions. 
        You balance growth investments with financial discipline."""
        
        try:
            response = self.ai_helper.generate_response(context_prompt, system_message)
            analysis = self._parse_financial_analysis(response)
            
            # Record analysis in history
            analysis_record = {
                "timestamp": datetime.now().isoformat(),
                "metrics": self.financial_data.copy(),
                "analysis": analysis,
                "agent_id": self.agent_id
            }
            self.financial_history.append(analysis_record)
            
            self.logger.info(f"Financial analysis complete: {analysis.get('performance_assessment', 'Unknown')}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing financial performance: {str(e)}")
            return self._create_fallback_analysis()
    
    def approve_expense(self, expense_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Approve or reject expense requests based on budget and financial policies.
        
        Args:
            expense_request (Dict): Expense request details
            
        Returns:
            Dict: Approval decision with reasoning and conditions
        """
        amount = expense_request.get('amount', 0)
        category = expense_request.get('category', 'operations')
        purpose = expense_request.get('purpose', 'Unknown')
        
        self.logger.info(f"Expense approval request: ${amount:,} for {purpose} ({category})")
        
        # Check if category exists in budget
        if category not in self.budget_categories:
            return {
                "approved": False,
                "reasoning": f"Invalid budget category: {category}",
                "conditions": ["Use valid budget category"],
                "available_categories": list(self.budget_categories.keys())
            }
        
        # Check budget availability
        budget_info = self.budget_categories[category]
        remaining_budget = budget_info["remaining"]
        
        if amount > remaining_budget:
            return {
                "approved": False,
                "reasoning": f"Insufficient budget in {category}: ${remaining_budget:,} remaining, ${amount:,} requested",
                "conditions": ["Request budget reallocation", "Reduce expense amount", "Wait for next budget cycle"],
                "budget_status": budget_info
            }
        
        # Auto-approve small expenses
        if amount <= 500:
            self._update_budget(category, amount)
            return {
                "approved": True,
                "reasoning": "Auto-approved: Small expense within policy limits",
                "approval_level": "automatic",
                "new_budget_remaining": self.budget_categories[category]["remaining"]
            }
        
        # CFO approval for medium expenses
        if amount <= self.approval_threshold:
            context_prompt = f"""
            As CFO, evaluate this expense request:
            
            EXPENSE DETAILS:
            - Amount: ${amount:,}
            - Category: {category}
            - Purpose: {purpose}
            - Requestor: {expense_request.get('requestor', 'Unknown')}
            - Urgency: {expense_request.get('urgency', 'Normal')}
            - Expected ROI: {expense_request.get('expected_roi', 'Not specified')}
            - Justification: {expense_request.get('justification', 'Not provided')}
            
            BUDGET STATUS:
            - Category Budget Allocated: ${budget_info['allocated']:,}
            - Category Budget Spent: ${budget_info['spent']:,}
            - Category Budget Remaining: ${budget_info['remaining']:,}
            - Utilization Rate: {(budget_info['spent'] / budget_info['allocated'] * 100):.1f}%
            
            FINANCIAL CONTEXT:
            - Monthly Revenue: ${self.financial_data['monthly_revenue']:,}
            - Profit Margin: {((self.financial_data['monthly_revenue'] - self.financial_data['monthly_expenses']) / self.financial_data['monthly_revenue'] * 100) if self.financial_data['monthly_revenue'] > 0 else 0:.1f}%
            - Target Profit Margin: {self.target_profit_margin}%
            
            Evaluate based on:
            1. Budget availability
            2. Business necessity
            3. ROI potential
            4. Strategic alignment
            5. Financial impact
            
            Provide decision with:
            - Approved (true/false)
            - Reasoning
            - Conditions (if any)
            - Alternative suggestions (if rejected)
            
            Respond in JSON format.
            """
            
            try:
                response = self.ai_helper.generate_response(context_prompt)
                approval = self._parse_approval_response(response)
                
                if approval.get("approved"):
                    self._update_budget(category, amount)
                    approval["new_budget_remaining"] = self.budget_categories[category]["remaining"]
                
                self.logger.info(f"Expense decision: {'Approved' if approval.get('approved') else 'Rejected'}")
                return approval
                
            except Exception as e:
                self.logger.error(f"Error processing expense approval: {str(e)}")
                return {
                    "approved": False,
                    "reasoning": "Error in approval process, defaulting to rejection for financial safety",
                    "conditions": ["Resubmit with complete details"]
                }
        
        else:
            return {
                "approved": False,
                "reasoning": f"Amount ${amount:,} exceeds CFO authority limit of ${self.approval_threshold:,}",
                "conditions": ["Requires CEO approval"],
                "approval_level": "ceo_required"
            }
    
    def optimize_pricing_strategy(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and optimize pricing strategy based on market data and financial goals.
        
        Args:
            market_data (Dict): Market research and competitor pricing data
            
        Returns:
            Dict: Pricing recommendations and strategy
        """
        self.logger.info("Optimizing pricing strategy")
        
        context_prompt = f"""
        As CFO, optimize our pricing strategy for UGC video packages:
        
        CURRENT FINANCIAL PERFORMANCE:
        - Monthly Revenue: ${self.financial_data['monthly_revenue']:,}
        - Profit Margin: {((self.financial_data['monthly_revenue'] - self.financial_data['monthly_expenses']) / self.financial_data['monthly_revenue'] * 100) if self.financial_data['monthly_revenue'] > 0 else 0:.1f}%
        - Target Profit Margin: {self.target_profit_margin}%
        - Client Acquisition Cost: ${self.financial_data['client_acquisition_cost']:,}
        - Customer Lifetime Value: ${self.financial_data['customer_lifetime_value']:,}
        
        MARKET DATA:
        {json.dumps(market_data, indent=2)}
        
        CURRENT SERVICE COSTS:
        - AI Generation Cost: $0.15 per video (using Anthropic)
        - Operational Overhead: 10% of revenue
        - Sales & Marketing: 15% of revenue
        
        Recommend pricing strategy including:
        1. Optimal price points for each package tier
        2. Value-based pricing justification
        3. Competitive positioning
        4. Profit margin analysis per tier
        5. Volume discount structure
        6. Upselling opportunities
        7. Price elasticity considerations
        8. Implementation timeline
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            pricing_strategy = self._parse_pricing_response(response)
            
            self.logger.info("Pricing strategy optimization complete")
            return pricing_strategy
            
        except Exception as e:
            self.logger.error(f"Error optimizing pricing strategy: {str(e)}")
            return self._create_fallback_pricing()
    
    def forecast_revenue(self, forecast_period: int = 12) -> Dict[str, Any]:
        """
        Generate revenue forecast based on current trends and growth projections.
        
        Args:
            forecast_period (int): Number of months to forecast
            
        Returns:
            Dict: Revenue forecast with confidence intervals and assumptions
        """
        self.logger.info(f"Generating {forecast_period}-month revenue forecast")
        
        # Calculate historical growth rate
        if len(self.financial_history) >= 2:
            recent_revenue = [record["metrics"]["monthly_revenue"] for record in self.financial_history[-6:]]
            growth_rate = self._calculate_growth_rate(recent_revenue)
        else:
            growth_rate = 0.25  # Default 25% monthly growth
        
        context_prompt = f"""
        As CFO, create a revenue forecast for the next {forecast_period} months:
        
        CURRENT FINANCIAL STATUS:
        - Current Monthly Revenue: ${self.financial_data['monthly_revenue']:,}
        - Historical Growth Rate: {growth_rate * 100:.1f}% per month
        - Client Acquisition Cost: ${self.financial_data['client_acquisition_cost']:,}
        - Customer Lifetime Value: ${self.financial_data['customer_lifetime_value']:,}
        - Current Client Count: {self.financial_data.get('client_count', 50)}
        
        MARKET FACTORS:
        - UGC market growing at 30% annually
        - Increasing demand for authentic content
        - AI technology reducing production costs
        - Competition increasing but market expanding
        
        Create forecast including:
        1. Monthly revenue projections
        2. Confidence intervals (optimistic/realistic/conservative)
        3. Key assumptions and drivers
        4. Risk factors that could impact forecast
        5. Milestone targets and growth phases
        6. Investment requirements for growth
        7. Break-even analysis for new initiatives
        
        Respond in JSON format with monthly breakdown.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            forecast = self._parse_forecast_response(response)
            
            self.logger.info(f"Revenue forecast generated for {forecast_period} months")
            return forecast
            
        except Exception as e:
            self.logger.error(f"Error generating revenue forecast: {str(e)}")
            return self._create_fallback_forecast(forecast_period)
    
    def generate_financial_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive financial report for executive review.
        
        Returns:
            Dict: Complete financial report with all key metrics and analysis
        """
        self.logger.info("Generating comprehensive financial report")
        
        # Calculate key ratios and metrics
        revenue = self.financial_data["monthly_revenue"]
        expenses = self.financial_data["monthly_expenses"]
        profit = revenue - expenses
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        # Budget utilization analysis
        total_budget = sum(cat["allocated"] for cat in self.budget_categories.values())
        total_spent = sum(cat["spent"] for cat in self.budget_categories.values())
        budget_utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
        
        report = {
            "report_date": datetime.now().isoformat(),
            "reporting_period": "Current Month",
            "executive_summary": {
                "revenue": revenue,
                "expenses": expenses,
                "net_profit": profit,
                "profit_margin": profit_margin,
                "performance_status": "STRONG" if profit_margin >= self.target_profit_margin else "NEEDS_IMPROVEMENT"
            },
            "revenue_analysis": {
                "monthly_revenue": revenue,
                "revenue_growth": self._calculate_revenue_growth(),
                "revenue_per_client": revenue / max(1, self.financial_data.get('client_count', 1)),
                "recurring_revenue_percentage": 85  # Estimated
            },
            "expense_analysis": {
                "total_expenses": expenses,
                "expense_categories": self.budget_categories,
                "budget_utilization": budget_utilization,
                "cost_per_acquisition": self.financial_data["client_acquisition_cost"]
            },
            "profitability_metrics": {
                "gross_profit_margin": profit_margin,
                "target_profit_margin": self.target_profit_margin,
                "profit_variance": profit_margin - self.target_profit_margin,
                "customer_lifetime_value": self.financial_data["customer_lifetime_value"],
                "ltv_to_cac_ratio": self.financial_data["customer_lifetime_value"] / max(1, self.financial_data["client_acquisition_cost"])
            },
            "cash_flow_analysis": {
                "operating_cash_flow": self.financial_data["cash_flow"],
                "accounts_receivable": self.financial_data["accounts_receivable"],
                "accounts_payable": self.financial_data["accounts_payable"],
                "cash_conversion_cycle": 30  # Estimated days
            },
            "key_recommendations": self._generate_financial_recommendations(),
            "risk_assessment": self._assess_financial_risks(),
            "next_review_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        self.logger.info("Financial report generated successfully")
        return report
    
    def update_financial_data(self, new_data: Dict[str, Any]) -> None:
        """
        Update financial data with new metrics.
        
        Args:
            new_data (Dict): Updated financial metrics
        """
        for key, value in new_data.items():
            if key in self.financial_data:
                old_value = self.financial_data[key]
                self.financial_data[key] = value
                
                if old_value > 0:
                    change = ((value - old_value) / old_value * 100)
                    self.logger.info(f"Financial metric updated - {key}: ${value:,} ({change:+.1f}%)")
                else:
                    self.logger.info(f"Financial metric updated - {key}: ${value:,}")
    
    def _update_budget(self, category: str, amount: float) -> None:
        """Update budget allocation after expense approval."""
        if category in self.budget_categories:
            self.budget_categories[category]["spent"] += amount
            self.budget_categories[category]["remaining"] -= amount
    
    def _calculate_growth_rate(self, revenue_history: List[float]) -> float:
        """Calculate average monthly growth rate from revenue history."""
        if len(revenue_history) < 2:
            return 0.0
        
        growth_rates = []
        for i in range(1, len(revenue_history)):
            if revenue_history[i-1] > 0:
                growth_rate = (revenue_history[i] - revenue_history[i-1]) / revenue_history[i-1]
                growth_rates.append(growth_rate)
        
        return sum(growth_rates) / len(growth_rates) if growth_rates else 0.0
    
    def _calculate_revenue_growth(self) -> float:
        """Calculate revenue growth from historical data."""
        if len(self.financial_history) >= 2:
            current = self.financial_history[-1]["metrics"]["monthly_revenue"]
            previous = self.financial_history[-2]["metrics"]["monthly_revenue"]
            return ((current - previous) / previous * 100) if previous > 0 else 0
        return 0.0
    
    def _generate_financial_recommendations(self) -> List[str]:
        """Generate financial recommendations based on current performance."""
        recommendations = []
        
        profit_margin = ((self.financial_data["monthly_revenue"] - self.financial_data["monthly_expenses"]) / 
                        self.financial_data["monthly_revenue"] * 100) if self.financial_data["monthly_revenue"] > 0 else 0
        
        if profit_margin < self.target_profit_margin:
            recommendations.append("Focus on cost optimization to improve profit margins")
        
        if self.financial_data["client_acquisition_cost"] > 0:
            ltv_cac_ratio = self.financial_data["customer_lifetime_value"] / self.financial_data["client_acquisition_cost"]
            if ltv_cac_ratio < 3:
                recommendations.append("Improve customer lifetime value or reduce acquisition costs")
        
        # Budget utilization recommendations
        for category, budget in self.budget_categories.items():
            utilization = (budget["spent"] / budget["allocated"] * 100) if budget["allocated"] > 0 else 0
            if utilization < 50:
                recommendations.append(f"Consider reallocating underutilized {category} budget")
            elif utilization > 90:
                recommendations.append(f"Monitor {category} budget closely - approaching limit")
        
        return recommendations
    
    def _assess_financial_risks(self) -> List[str]:
        """Assess current financial risks."""
        risks = []
        
        # Cash flow risks
        if self.financial_data["cash_flow"] < 0:
            risks.append("Negative cash flow - monitor liquidity closely")
        
        # Profit margin risks
        profit_margin = ((self.financial_data["monthly_revenue"] - self.financial_data["monthly_expenses"]) / 
                        self.financial_data["monthly_revenue"] * 100) if self.financial_data["monthly_revenue"] > 0 else 0
        
        if profit_margin < 50:
            risks.append("Low profit margins - vulnerable to cost increases")
        
        # Client concentration risk
        if self.financial_data.get("client_count", 0) < 20:
            risks.append("Low client diversification - high customer concentration risk")
        
        return risks
    
    def _parse_financial_analysis(self, response: str) -> Dict[str, Any]:
        """Parse AI response for financial analysis."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_analysis()
    
    def _parse_approval_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for expense approvals."""
        try:
            return json.loads(response)
        except:
            return {
                "approved": False,
                "reasoning": "Unable to parse AI response, defaulting to rejection for financial safety",
                "conditions": ["Resubmit with complete details"]
            }
    
    def _parse_pricing_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for pricing strategy."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_pricing()
    
    def _parse_forecast_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for revenue forecast."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_forecast(12)
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create fallback financial analysis."""
        return {
            "performance_assessment": "FAIR",
            "key_strengths": ["Automated operations", "Low operational costs"],
            "concerns": ["AI analysis unavailable"],
            "recommendations": ["Implement manual financial review", "Ensure AI system reliability"],
            "risk_factors": ["Technology dependency"]
        }
    
    def _create_fallback_pricing(self) -> Dict[str, Any]:
        """Create fallback pricing strategy."""
        return {
            "pricing_tiers": {
                "basic": {"price": 5000, "videos": 3, "margin": 85},
                "growth": {"price": 8000, "videos": 5, "margin": 87},
                "premium": {"price": 12000, "videos": 8, "margin": 90}
            },
            "strategy": "Value-based pricing with high margins",
            "implementation": "Immediate"
        }
    
    def _create_fallback_forecast(self, months: int) -> Dict[str, Any]:
        """Create fallback revenue forecast."""
        current_revenue = self.financial_data["monthly_revenue"]
        growth_rate = 0.20  # 20% monthly growth
        
        forecast = []
        for month in range(1, months + 1):
            projected_revenue = current_revenue * (1 + growth_rate) ** month
            forecast.append({
                "month": month,
                "revenue": round(projected_revenue, 2),
                "confidence": "MEDIUM"
            })
        
        return {
            "forecast_period": f"{months} months",
            "monthly_projections": forecast,
            "assumptions": ["20% monthly growth", "Market conditions remain stable"],
            "confidence_level": "MEDIUM"
        }


def test_cfo_agent():
    """Test the CFO Agent functionality."""
    print("🧪 Testing CFO Agent...")
    
    # Initialize CFO
    cfo = CFOAgent()
    
    # Update financial data
    cfo.update_financial_data({
        "monthly_revenue": 150000,
        "monthly_expenses": 25000,
        "client_acquisition_cost": 500,
        "customer_lifetime_value": 15000
    })
    
    # Test financial analysis
    analysis = cfo.analyze_financial_performance()
    print(f"✅ Financial Analysis: {analysis.get('performance_assessment', 'Unknown')}")
    
    # Test expense approval
    expense_request = {
        "amount": 5000,
        "category": "marketing",
        "purpose": "Social media advertising campaign",
        "expected_roi": "300%"
    }
    
    approval = cfo.approve_expense(expense_request)
    print(f"✅ Expense Approval: {'Approved' if approval.get('approved') else 'Rejected'}")
    
    # Test financial report
    report = cfo.generate_financial_report()
    print(f"✅ Financial Report Generated: {report['executive_summary']['performance_status']}")
    
    print("💰 CFO Agent test complete!")
    return cfo


if __name__ == "__main__":
    test_cfo_agent()
