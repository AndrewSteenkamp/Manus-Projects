"""
CRM (Customer Relationship Management) Service
Track all leads, clients, and interactions
Implements Nick's systematic approach to client management
"""

import json
from datetime import datetime, timedelta
from openai import OpenAI

class CRM:
    """
    Autonomous CRM system for managing the entire client lifecycle
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.leads = {}
        self.clients = {}
        self.interactions = []
        
    def add_lead(self, name, company, email, source, niche):
        """
        Add a new lead to the system
        """
        lead_id = f"LEAD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        lead = {
            "lead_id": lead_id,
            "name": name,
            "company": company,
            "email": email,
            "source": source,  # upwork, cold_email, referral, etc.
            "niche": niche,
            "status": "new",
            "score": 0,
            "created_at": datetime.now().isoformat(),
            "last_contact": None,
            "interactions": [],
            "notes": []
        }
        
        # AI scores the lead quality
        lead["score"] = self._score_lead(lead)
        
        self.leads[lead_id] = lead
        return lead
    
    def _score_lead(self, lead):
        """
        AI-powered lead scoring (0-100)
        """
        prompt = f"""Score this lead's quality (0-100):

Name: {lead['name']}
Company: {lead['company']}
Source: {lead['source']}
Niche: {lead['niche']}

Consider:
1. Source quality (Upwork referrals > cold email)
2. Company legitimacy
3. Niche fit
4. Likelihood to convert

Respond with just a number 0-100."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a lead scoring expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            score = int(response.choices[0].message.content.strip())
            return min(max(score, 0), 100)  # Ensure 0-100
        except:
            return 50  # Default score
    
    def log_interaction(self, lead_id, interaction_type, details):
        """
        Log any interaction with a lead
        """
        interaction = {
            "interaction_id": f"INT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "lead_id": lead_id,
            "type": interaction_type,  # email, call, meeting, proposal, etc.
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        self.interactions.append(interaction)
        
        if lead_id in self.leads:
            self.leads[lead_id]["interactions"].append(interaction)
            self.leads[lead_id]["last_contact"] = datetime.now().isoformat()
        
        return interaction
    
    def get_follow_up_recommendations(self, lead_id):
        """
        AI recommends next steps for a lead
        """
        if lead_id not in self.leads:
            return {"error": "Lead not found"}
        
        lead = self.leads[lead_id]
        
        prompt = f"""Recommend next steps for this lead:

Status: {lead['status']}
Last Contact: {lead['last_contact']}
Interactions: {len(lead['interactions'])}
Recent Interactions: {json.dumps(lead['interactions'][-3:])}

Provide:
1. Recommended next action
2. Timing (when to do it)
3. Message/approach to use
4. Expected outcome

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a sales follow-up expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def update_lead_status(self, lead_id, new_status, notes=None):
        """
        Update lead status
        Statuses: new, contacted, interested, proposal_sent, negotiating, won, lost
        """
        if lead_id in self.leads:
            old_status = self.leads[lead_id]["status"]
            self.leads[lead_id]["status"] = new_status
            self.leads[lead_id]["status_updated_at"] = datetime.now().isoformat()
            
            if notes:
                self.leads[lead_id]["notes"].append({
                    "note": notes,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Log status change
            self.log_interaction(lead_id, "status_change", {
                "from": old_status,
                "to": new_status,
                "notes": notes
            })
            
            return self.leads[lead_id]
        
        return {"error": "Lead not found"}
    
    def convert_to_client(self, lead_id, deal_value, contract_details):
        """
        Convert a lead to a paying client
        """
        if lead_id not in self.leads:
            return {"error": "Lead not found"}
        
        lead = self.leads[lead_id]
        client_id = f"CLI-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        client = {
            "client_id": client_id,
            "lead_id": lead_id,
            "name": lead["name"],
            "company": lead["company"],
            "email": lead["email"],
            "deal_value": deal_value,
            "contract_details": contract_details,
            "converted_at": datetime.now().isoformat(),
            "status": "active",
            "projects": [],
            "lifetime_value": deal_value
        }
        
        self.clients[client_id] = client
        self.update_lead_status(lead_id, "won", f"Converted to client. Deal value: R{deal_value}")
        
        return client
    
    def get_leads_needing_follow_up(self):
        """
        Get all leads that need follow-up
        """
        needs_follow_up = []
        now = datetime.now()
        
        for lead_id, lead in self.leads.items():
            if lead["status"] in ["lost", "won"]:
                continue
            
            # Check last contact
            if lead["last_contact"]:
                last_contact = datetime.fromisoformat(lead["last_contact"])
                days_since = (now - last_contact).days
                
                # Follow up after 3 days
                if days_since >= 3:
                    needs_follow_up.append({
                        "lead": lead,
                        "days_since_contact": days_since,
                        "priority": "high" if days_since >= 7 else "medium"
                    })
            else:
                # Never contacted
                needs_follow_up.append({
                    "lead": lead,
                    "days_since_contact": None,
                    "priority": "high"
                })
        
        # Sort by priority and score
        needs_follow_up.sort(key=lambda x: (
            0 if x["priority"] == "high" else 1,
            -x["lead"]["score"]
        ))
        
        return needs_follow_up
    
    def get_pipeline_stats(self):
        """
        Get sales pipeline statistics
        """
        status_counts = {}
        for lead in self.leads.values():
            status = lead["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_deal_value = sum(c["lifetime_value"] for c in self.clients.values())
        
        return {
            "total_leads": len(self.leads),
            "total_clients": len(self.clients),
            "status_breakdown": status_counts,
            "total_revenue": total_deal_value,
            "conversion_rate": f"{(len(self.clients) / len(self.leads) * 100):.2f}%" if self.leads else "0%",
            "needs_follow_up": len(self.get_leads_needing_follow_up())
        }
    
    def search_leads(self, query):
        """
        Search leads by name, company, or email
        """
        results = []
        query_lower = query.lower()
        
        for lead in self.leads.values():
            if (query_lower in lead["name"].lower() or
                query_lower in lead["company"].lower() or
                query_lower in lead["email"].lower()):
                results.append(lead)
        
        return results
    
    def get_top_leads(self, limit=10):
        """
        Get highest-scoring leads
        """
        sorted_leads = sorted(
            self.leads.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return sorted_leads[:limit]
