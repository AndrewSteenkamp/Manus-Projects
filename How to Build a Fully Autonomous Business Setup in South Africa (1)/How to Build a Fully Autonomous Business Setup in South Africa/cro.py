"""
CRO (Chief Revenue Officer) Agent
Handles client acquisition, sales strategy, and revenue generation
Implements Nick's framework for getting clients
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from core.base_agent import BaseAgent
import json
from datetime import datetime

class CROAgent(BaseAgent):
    """
    CRO Agent - Autonomous sales and client acquisition
    Implements Nick's 4-phase framework
    """
    
    def __init__(self):
        super().__init__(
            name="CRO",
            role="Chief Revenue Officer",
            department="Sales"
        )
        self.leads = []
        self.clients = []
        self.proposals_sent = 0
        self.conversion_rate = 0
    
    def _execute_actions(self, actions, context):
        """
        Execute sales-specific actions
        """
        results = []
        
        for action in actions:
            if "find_leads" in action.lower() or "prospect" in action.lower():
                results.append(self.find_leads(context))
            elif "loom" in action.lower() or "video" in action.lower():
                results.append(self.create_loom_pitch(context))
            elif "proposal" in action.lower():
                results.append(self.generate_proposal(context))
            elif "follow_up" in action.lower():
                results.append(self.follow_up_lead(context))
            elif "close" in action.lower():
                results.append(self.close_deal(context))
            else:
                results.append(f"Executed sales action: {action}")
        
        return results
    
    def find_leads(self, context):
        """
        Find potential clients using AI analysis
        Implements Nick's Phase 1: Front-loading client acquisition
        """
        niche = context.get("niche", "AI automation")
        
        # Use AI to generate lead criteria
        prompt = f"""As a sales expert, identify the ideal client profile for {niche} services.

Provide:
1. Industry sectors most likely to need this
2. Company size range
3. Pain points they face
4. Budget range
5. Decision maker titles

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CRO expert at identifying ideal clients."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            lead_criteria = json.loads(response.choices[0].message.content)
            
            # Simulate finding leads (in production, this would scrape Upwork, LinkedIn, etc.)
            leads_found = {
                "criteria": lead_criteria,
                "potential_leads": 25,  # Simulated
                "sources": ["Upwork", "LinkedIn", "Cold Email Lists"],
                "timestamp": datetime.now().isoformat()
            }
            
            self.leads.append(leads_found)
            
            return {
                "type": "lead_generation",
                "data": leads_found,
                "status": "completed"
            }
        except Exception as e:
            return {
                "type": "lead_generation",
                "error": str(e),
                "status": "failed"
            }
    
    def create_loom_pitch(self, context):
        """
        Generate personalized Loom video script
        Implements Nick's strategy: 20-25 Loom videos per day
        """
        lead_info = context.get("lead", {})
        
        prompt = f"""Create a personalized Loom video script for this lead:

Company: {lead_info.get('company', 'Unknown')}
Industry: {lead_info.get('industry', 'Unknown')}
Pain Point: {lead_info.get('pain_point', 'Unknown')}

The script should:
1. Hook them in first 5 seconds
2. Show you understand their specific problem
3. Present a clear solution
4. Include a soft call-to-action
5. Be 60-90 seconds long

Respond with the script in JSON format with sections: hook, problem, solution, cta"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sales expert creating compelling video pitches."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            script = json.loads(response.choices[0].message.content)
            self.proposals_sent += 1
            
            return {
                "type": "loom_script",
                "data": script,
                "lead": lead_info,
                "status": "completed"
            }
        except Exception as e:
            return {
                "type": "loom_script",
                "error": str(e),
                "status": "failed"
            }
    
    def generate_proposal(self, context):
        """
        Generate AI-powered custom proposal
        """
        client_info = context.get("client", {})
        service_type = context.get("service", "AI Automation")
        
        prompt = f"""Create a professional service proposal for:

Client: {client_info.get('name', 'Potential Client')}
Service: {service_type}
Budget Range: {client_info.get('budget', 'R5,000 - R50,000')}

Include:
1. Executive summary
2. Problem statement
3. Proposed solution
4. Deliverables
5. Timeline
6. Pricing (fixed price, not hourly)
7. Next steps

Respond in JSON format with all sections."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CRO creating winning proposals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            
            proposal = json.loads(response.choices[0].message.content)
            proposal["proposal_id"] = f"PROP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            proposal["created_at"] = datetime.now().isoformat()
            
            return {
                "type": "proposal",
                "data": proposal,
                "status": "completed"
            }
        except Exception as e:
            return {
                "type": "proposal",
                "error": str(e),
                "status": "failed"
            }
    
    def follow_up_lead(self, context):
        """
        AI-generated follow-up messages
        """
        lead_info = context.get("lead", {})
        previous_contact = context.get("previous_contact", "initial_outreach")
        
        prompt = f"""Create a follow-up message for:

Lead: {lead_info.get('name', 'Prospect')}
Previous Contact: {previous_contact}
Days Since Last Contact: {context.get('days_since', 3)}

The message should be:
1. Brief and respectful
2. Add new value
3. Include a clear next step
4. Not be pushy

Respond with the message text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a CRO crafting effective follow-ups."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            follow_up = {
                "message": response.choices[0].message.content,
                "lead": lead_info,
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "type": "follow_up",
                "data": follow_up,
                "status": "completed"
            }
        except Exception as e:
            return {
                "type": "follow_up",
                "error": str(e),
                "status": "failed"
            }
    
    def close_deal(self, context):
        """
        Process closed deal and convert lead to client
        """
        lead_info = context.get("lead", {})
        deal_value = context.get("deal_value", 0)
        
        client = {
            "client_id": f"CLI-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "name": lead_info.get('name', 'New Client'),
            "deal_value": deal_value,
            "signed_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.clients.append(client)
        self.conversion_rate = len(self.clients) / max(len(self.leads), 1) * 100
        
        return {
            "type": "deal_closed",
            "data": client,
            "conversion_rate": self.conversion_rate,
            "status": "completed"
        }
    
    def get_sales_metrics(self):
        """
        Return current sales performance metrics
        """
        return {
            "total_leads": len(self.leads),
            "total_clients": len(self.clients),
            "proposals_sent": self.proposals_sent,
            "conversion_rate": f"{self.conversion_rate:.2f}%",
            "recent_clients": self.clients[-5:] if self.clients else []
        }
