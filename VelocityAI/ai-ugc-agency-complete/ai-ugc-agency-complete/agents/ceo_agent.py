#!/usr/bin/env python3
"""
CEO Agent - Chief Executive Officer
Strategic leadership and high-level decision making for the autonomous UGC advertising agency
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

class CEOAgent:
    """
    The CEO Agent is the strategic leader of the autonomous advertising agency.
    
    Responsibilities:
    - Strategic planning and vision setting
    - High-level decision making
    - Resource allocation and budget approval
    - Performance monitoring and KPI tracking
    - Risk assessment and mitigation
    - Market analysis and competitive positioning
    - Partnership and expansion decisions
    
    The CEO Agent operates at the highest level, making decisions that affect
    the entire organization and its long-term success.
    """
    
    def __init__(self, ai_provider: str = None):
        """
        Initialize the CEO Agent with AI capabilities.
        
        Args:
            ai_provider (str): Preferred AI provider for decision making
        """
        self.ai_helper = AIHelper(provider=ai_provider)
        self.agent_id = "CEO-001"
        self.name = "Alexandra Sterling"
        self.role = "Chief Executive Officer"
        
        # CEO-specific configuration
        self.decision_threshold = 0.7  # Minimum confidence for autonomous decisions
        self.budget_authority = 100000  # Maximum budget approval without board consent
        self.strategic_focus = ["growth", "profitability", "market_expansion", "innovation"]
        
        # Performance tracking
        self.kpis = {
            "monthly_revenue": 0,
            "client_acquisition_rate": 0,
            "profit_margin": 0,
            "client_retention_rate": 0,
            "market_share": 0
        }
        
        # Decision history for learning and improvement
        self.decision_history = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"CEO-{self.agent_id}")
        
        print(f"🎯 CEO Agent '{self.name}' initialized")
        print(f"   Role: {self.role}")
        print(f"   AI Provider: {self.ai_helper.provider}")
        print(f"   Budget Authority: ${self.budget_authority:,}")
    
    def make_strategic_decision(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make high-level strategic decisions based on business context.
        
        Args:
            decision_context (Dict): Context including market data, financials, opportunities
            
        Returns:
            Dict: Decision outcome with reasoning, confidence, and action plan
        """
        self.logger.info(f"Making strategic decision: {decision_context.get('decision_type', 'Unknown')}")
        
        # Prepare context for AI analysis
        context_prompt = f"""
        As the CEO of an AI-powered UGC advertising agency, analyze this business situation and make a strategic decision:
        
        CONTEXT:
        {json.dumps(decision_context, indent=2)}
        
        CURRENT COMPANY STATUS:
        - Monthly Revenue: ${self.kpis['monthly_revenue']:,}
        - Profit Margin: {self.kpis['profit_margin']}%
        - Client Retention: {self.kpis['client_retention_rate']}%
        - Market Position: Growing
        
        STRATEGIC PRIORITIES:
        {', '.join(self.strategic_focus)}
        
        Please provide a strategic decision with:
        1. Decision (APPROVE/REJECT/MODIFY/INVESTIGATE)
        2. Reasoning (detailed business rationale)
        3. Confidence score (0-100)
        4. Risk assessment (LOW/MEDIUM/HIGH)
        5. Expected ROI (if applicable)
        6. Implementation timeline
        7. Success metrics
        8. Contingency plans
        
        Respond in JSON format.
        """
        
        system_message = """You are Alexandra Sterling, an experienced CEO with 15 years in digital marketing and AI technology. 
        You make data-driven decisions focused on sustainable growth, profitability, and market leadership. 
        You balance aggressive growth with risk management."""
        
        try:
            response = self.ai_helper.generate_response(context_prompt, system_message)
            decision = self._parse_decision_response(response)
            
            # Record decision in history
            decision_record = {
                "timestamp": datetime.now().isoformat(),
                "context": decision_context,
                "decision": decision,
                "agent_id": self.agent_id
            }
            self.decision_history.append(decision_record)
            
            # Log the decision
            self.logger.info(f"Strategic decision made: {decision.get('decision', 'Unknown')}")
            self.logger.info(f"Confidence: {decision.get('confidence_score', 0)}")
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Error making strategic decision: {str(e)}")
            return self._create_fallback_decision(decision_context)
    
    def approve_budget(self, budget_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Approve or reject budget requests based on strategic priorities.
        
        Args:
            budget_request (Dict): Budget request details including amount, purpose, ROI
            
        Returns:
            Dict: Approval decision with conditions and reasoning
        """
        amount = budget_request.get('amount', 0)
        purpose = budget_request.get('purpose', 'Unknown')
        
        self.logger.info(f"Budget approval request: ${amount:,} for {purpose}")
        
        # Automatic approval for small amounts
        if amount <= 1000:
            return {
                "approved": True,
                "amount": amount,
                "reasoning": "Auto-approved: Amount within discretionary limit",
                "conditions": [],
                "approval_level": "automatic"
            }
        
        # CEO approval required for larger amounts
        if amount <= self.budget_authority:
            context_prompt = f"""
            As CEO, evaluate this budget request:
            
            REQUEST DETAILS:
            - Amount: ${amount:,}
            - Purpose: {purpose}
            - Department: {budget_request.get('department', 'Unknown')}
            - Expected ROI: {budget_request.get('expected_roi', 'Not specified')}
            - Timeline: {budget_request.get('timeline', 'Not specified')}
            - Justification: {budget_request.get('justification', 'Not provided')}
            
            CURRENT FINANCIAL STATUS:
            - Monthly Revenue: ${self.kpis['monthly_revenue']:,}
            - Profit Margin: {self.kpis['profit_margin']}%
            - Available Budget: ${self.budget_authority:,}
            
            Provide approval decision with:
            1. Approved (true/false)
            2. Reasoning
            3. Conditions (if any)
            4. Alternative suggestions (if rejected)
            
            Respond in JSON format.
            """
            
            try:
                response = self.ai_helper.generate_response(context_prompt)
                approval = self._parse_approval_response(response)
                
                self.logger.info(f"Budget decision: {'Approved' if approval.get('approved') else 'Rejected'}")
                return approval
                
            except Exception as e:
                self.logger.error(f"Error processing budget approval: {str(e)}")
                return {
                    "approved": False,
                    "reasoning": "Error in approval process, defaulting to rejection for safety",
                    "conditions": ["Resubmit with more details"],
                    "approval_level": "error_fallback"
                }
        
        else:
            return {
                "approved": False,
                "reasoning": f"Amount ${amount:,} exceeds CEO authority limit of ${self.budget_authority:,}",
                "conditions": ["Requires board approval"],
                "approval_level": "board_required"
            }
    
    def analyze_market_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze new market opportunities and provide strategic recommendations.
        
        Args:
            opportunity (Dict): Market opportunity details
            
        Returns:
            Dict: Analysis with recommendations and strategic fit assessment
        """
        self.logger.info(f"Analyzing market opportunity: {opportunity.get('name', 'Unknown')}")
        
        context_prompt = f"""
        As CEO, analyze this market opportunity for our UGC advertising agency:
        
        OPPORTUNITY:
        {json.dumps(opportunity, indent=2)}
        
        COMPANY STRENGTHS:
        - AI-powered UGC video creation
        - Automated client acquisition
        - Multi-platform content distribution
        - Cost-effective operations
        
        CURRENT MARKET POSITION:
        - Revenue: ${self.kpis['monthly_revenue']:,}/month
        - Client base: Growing
        - Technology advantage: High
        
        Analyze:
        1. Market size and potential
        2. Competitive landscape
        3. Strategic fit with our capabilities
        4. Resource requirements
        5. Risk factors
        6. Expected timeline to profitability
        7. Recommendation (PURSUE/INVESTIGATE/REJECT)
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            analysis = self._parse_analysis_response(response)
            
            self.logger.info(f"Market analysis complete: {analysis.get('recommendation', 'Unknown')}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing market opportunity: {str(e)}")
            return self._create_fallback_analysis(opportunity)
    
    def set_quarterly_objectives(self) -> Dict[str, Any]:
        """
        Set strategic objectives for the next quarter based on current performance.
        
        Returns:
            Dict: Quarterly objectives with targets and success metrics
        """
        self.logger.info("Setting quarterly objectives")
        
        context_prompt = f"""
        As CEO, set strategic objectives for the next quarter based on current performance:
        
        CURRENT PERFORMANCE:
        - Monthly Revenue: ${self.kpis['monthly_revenue']:,}
        - Profit Margin: {self.kpis['profit_margin']}%
        - Client Retention: {self.kpis['client_retention_rate']}%
        - Growth Rate: 25% month-over-month
        
        STRATEGIC FOCUS AREAS:
        {', '.join(self.strategic_focus)}
        
        Set objectives for:
        1. Revenue targets
        2. Client acquisition goals
        3. Market expansion plans
        4. Technology improvements
        5. Operational efficiency
        6. Team development
        
        For each objective, include:
        - Specific target
        - Success metrics
        - Timeline
        - Resource requirements
        - Risk mitigation
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            objectives = self._parse_objectives_response(response)
            
            self.logger.info(f"Quarterly objectives set: {len(objectives.get('objectives', []))} objectives")
            return objectives
            
        except Exception as e:
            self.logger.error(f"Error setting quarterly objectives: {str(e)}")
            return self._create_fallback_objectives()
    
    def update_kpis(self, new_kpis: Dict[str, float]) -> None:
        """
        Update key performance indicators.
        
        Args:
            new_kpis (Dict): Updated KPI values
        """
        for kpi, value in new_kpis.items():
            if kpi in self.kpis:
                old_value = self.kpis[kpi]
                self.kpis[kpi] = value
                
                change = ((value - old_value) / old_value * 100) if old_value > 0 else 0
                self.logger.info(f"KPI Updated - {kpi}: {value} ({change:+.1f}%)")
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """
        Generate executive dashboard with key metrics and insights.
        
        Returns:
            Dict: Dashboard data with KPIs, trends, and recommendations
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "kpis": self.kpis,
            "decision_count": len(self.decision_history),
            "strategic_focus": self.strategic_focus,
            "budget_utilization": f"{(self.budget_authority * 0.7):,.0f}",  # Simulated
            "next_review": (datetime.now() + timedelta(days=7)).isoformat(),
            "status": "OPERATIONAL",
            "ai_provider": self.ai_helper.provider,
            "cost_efficiency": self.ai_helper.get_cost_info()
        }
    
    def _parse_decision_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for strategic decisions."""
        try:
            return json.loads(response)
        except:
            return {
                "decision": "INVESTIGATE",
                "reasoning": "Unable to parse AI response, defaulting to investigation",
                "confidence_score": 50,
                "risk_assessment": "MEDIUM"
            }
    
    def _parse_approval_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for budget approvals."""
        try:
            return json.loads(response)
        except:
            return {
                "approved": False,
                "reasoning": "Unable to parse AI response, defaulting to rejection for safety",
                "conditions": ["Resubmit with clearer details"]
            }
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for market analysis."""
        try:
            return json.loads(response)
        except:
            return {
                "recommendation": "INVESTIGATE",
                "reasoning": "Unable to parse AI response, requires further analysis",
                "confidence": 50
            }
    
    def _parse_objectives_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for quarterly objectives."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_objectives()
    
    def _create_fallback_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback decision when AI is unavailable."""
        return {
            "decision": "INVESTIGATE",
            "reasoning": "AI unavailable, defaulting to investigation for safety",
            "confidence_score": 30,
            "risk_assessment": "MEDIUM",
            "next_steps": ["Gather more data", "Consult with department heads", "Reassess in 24 hours"]
        }
    
    def _create_fallback_analysis(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback market analysis."""
        return {
            "recommendation": "INVESTIGATE",
            "market_potential": "Unknown - requires research",
            "strategic_fit": "To be determined",
            "risk_level": "MEDIUM",
            "next_steps": ["Conduct market research", "Analyze competitors", "Assess resource requirements"]
        }
    
    def _create_fallback_objectives(self) -> Dict[str, Any]:
        """Create fallback quarterly objectives."""
        return {
            "objectives": [
                {
                    "name": "Revenue Growth",
                    "target": "Increase monthly revenue by 20%",
                    "timeline": "Q1 2024"
                },
                {
                    "name": "Client Acquisition",
                    "target": "Acquire 50 new clients",
                    "timeline": "Q1 2024"
                },
                {
                    "name": "Operational Efficiency",
                    "target": "Reduce operational costs by 10%",
                    "timeline": "Q1 2024"
                }
            ],
            "success_metrics": ["Revenue targets", "Client satisfaction", "Cost reduction"],
            "review_schedule": "Monthly"
        }


def test_ceo_agent():
    """Test the CEO Agent functionality."""
    print("🧪 Testing CEO Agent...")
    
    # Initialize CEO
    ceo = CEOAgent()
    
    # Test strategic decision making
    decision_context = {
        "decision_type": "market_expansion",
        "opportunity": "Enter European market",
        "investment_required": 50000,
        "expected_roi": "200% in 12 months",
        "risk_factors": ["Currency fluctuation", "Regulatory compliance"]
    }
    
    decision = ceo.make_strategic_decision(decision_context)
    print(f"✅ Strategic Decision: {decision.get('decision', 'Unknown')}")
    
    # Test budget approval
    budget_request = {
        "amount": 15000,
        "purpose": "Marketing campaign expansion",
        "department": "Marketing",
        "expected_roi": "300%",
        "timeline": "3 months"
    }
    
    approval = ceo.approve_budget(budget_request)
    print(f"✅ Budget Approval: {'Approved' if approval.get('approved') else 'Rejected'}")
    
    # Test performance dashboard
    dashboard = ceo.get_performance_dashboard()
    print(f"✅ Dashboard Generated: {len(dashboard)} metrics")
    
    print("🎯 CEO Agent test complete!")
    return ceo


if __name__ == "__main__":
    test_ceo_agent()
