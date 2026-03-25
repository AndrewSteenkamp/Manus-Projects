"""
Automated Client Onboarding System
Handles the complete journey from lead to active project
"""

import sys
sys.path.append('/home/ubuntu/autonomous_business')

from datetime import datetime
import json
from openai import OpenAI

class ClientOnboarding:
    """
    Automates the entire client onboarding process
    Lead → Qualified → Proposal → Contract → Payment → Project Start
    """
    
    def __init__(self, crm, cro, cfo, legal_dept):
        self.client = OpenAI()
        self.crm = crm
        self.cro = cro
        self.cfo = cfo
        self.legal_dept = legal_dept
        self.onboarding_pipelines = []
        
    def start_onboarding(self, lead_id):
        """
        Start automated onboarding for a lead
        """
        if lead_id not in self.crm.leads:
            return {"error": "Lead not found"}
        
        lead = self.crm.leads[lead_id]
        
        pipeline = {
            "pipeline_id": f"PIPE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "lead_id": lead_id,
            "lead": lead,
            "stage": "qualification",
            "started_at": datetime.now().isoformat(),
            "stages_completed": [],
            "current_action": None
        }
        
        self.onboarding_pipelines.append(pipeline)
        
        # Start qualification
        result = self.qualify_lead(pipeline)
        
        return {
            "pipeline": pipeline,
            "qualification_result": result
        }
    
    def qualify_lead(self, pipeline):
        """
        AI-powered lead qualification
        Determines if lead is worth pursuing
        """
        lead = pipeline["lead"]
        
        prompt = f"""Qualify this lead for our AI automation services:

Name: {lead['name']}
Company: {lead['company']}
Source: {lead['source']}
Niche: {lead['niche']}
Lead Score: {lead['score']}

Qualification criteria:
1. Budget fit (can they afford R10,000+ projects?)
2. Need urgency (do they need solution now?)
3. Decision authority (can they make decisions?)
4. Good fit (is our service right for them?)

Respond in JSON:
{{
    "qualified": true/false,
    "confidence": 0-100,
    "reasoning": "explanation",
    "recommended_next_step": "action",
    "estimated_deal_value": amount
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a sales qualification expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            qualification = json.loads(response.choices[0].message.content)
            
            pipeline["stages_completed"].append({
                "stage": "qualification",
                "result": qualification,
                "timestamp": datetime.now().isoformat()
            })
            
            if qualification["qualified"]:
                pipeline["stage"] = "proposal"
                pipeline["estimated_value"] = qualification.get("estimated_deal_value", 0)
                # Auto-generate proposal
                self.generate_proposal(pipeline)
            else:
                pipeline["stage"] = "disqualified"
                self.crm.update_lead_status(pipeline["lead_id"], "disqualified", qualification["reasoning"])
            
            return qualification
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_proposal(self, pipeline):
        """
        Automatically generate and send proposal
        """
        lead = pipeline["lead"]
        
        # Use CRO agent to generate proposal
        proposal_context = {
            "client": {
                "name": lead["name"],
                "company": lead["company"],
                "budget": f"R{pipeline.get('estimated_value', 10000)}"
            },
            "service": lead["niche"]
        }
        
        proposal = self.cro.generate_proposal(proposal_context)
        
        pipeline["stages_completed"].append({
            "stage": "proposal",
            "result": proposal,
            "timestamp": datetime.now().isoformat()
        })
        
        pipeline["stage"] = "proposal_sent"
        pipeline["proposal"] = proposal
        
        # Update CRM
        self.crm.update_lead_status(
            pipeline["lead_id"],
            "proposal_sent",
            f"Proposal generated and sent: {proposal.get('data', {}).get('proposal_id', 'N/A')}"
        )
        
        return proposal
    
    def handle_proposal_acceptance(self, pipeline_id):
        """
        Handle when client accepts proposal
        Automatically generates contract and invoice
        """
        pipeline = self._get_pipeline(pipeline_id)
        if not pipeline:
            return {"error": "Pipeline not found"}
        
        # Generate contract
        contract = self.generate_contract(pipeline)
        
        # Generate invoice
        invoice = self.generate_invoice(pipeline)
        
        pipeline["stage"] = "contract_sent"
        pipeline["contract"] = contract
        pipeline["invoice"] = invoice
        
        pipeline["stages_completed"].append({
            "stage": "contract_and_invoice",
            "contract": contract,
            "invoice": invoice,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "contract": contract,
            "invoice": invoice,
            "next_step": "Awaiting contract signature and payment"
        }
    
    def generate_contract(self, pipeline):
        """
        Generate legal contract using Legal department
        """
        lead = pipeline["lead"]
        proposal = pipeline.get("proposal", {})
        
        contract_context = {
            "type": "service_agreement",
            "parties": {
                "party_a": "Your Company Name",
                "party_b": lead["company"]
            },
            "scope": lead["niche"],
            "value": pipeline.get("estimated_value", 0),
            "duration": "3 months"
        }
        
        # Use Legal department to draft contract
        contract = self.legal_dept.delegate_task("Draft service agreement contract", contract_context)
        
        return contract
    
    def generate_invoice(self, pipeline):
        """
        Generate invoice with payment link using CFO
        """
        lead = pipeline["lead"]
        amount = pipeline.get("estimated_value", 0)
        
        invoice_context = {
            "invoice_data": {
                "client": lead["name"],
                "amount": amount,
                "description": f"{lead['niche']} services"
            }
        }
        
        # Use CFO to generate invoice
        invoice = self.cfo.process_invoice(invoice_context)
        
        return invoice
    
    def handle_payment_received(self, pipeline_id, payment_data):
        """
        Handle when payment is received
        Converts lead to client and starts project
        """
        pipeline = self._get_pipeline(pipeline_id)
        if not pipeline:
            return {"error": "Pipeline not found"}
        
        # Convert lead to client in CRM
        client = self.crm.convert_to_client(
            pipeline["lead_id"],
            payment_data.get("amount", 0),
            {
                "contract": pipeline.get("contract"),
                "payment": payment_data
            }
        )
        
        # Start project
        project = self.start_project(pipeline, client)
        
        pipeline["stage"] = "active_project"
        pipeline["client"] = client
        pipeline["project"] = project
        
        pipeline["stages_completed"].append({
            "stage": "payment_and_project_start",
            "client": client,
            "project": project,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "client": client,
            "project": project,
            "status": "Onboarding complete - Project active"
        }
    
    def start_project(self, pipeline, client):
        """
        Initialize project for client
        """
        project = {
            "project_id": f"PROJ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "client_id": client["client_id"],
            "client_name": client["name"],
            "service_type": pipeline["lead"]["niche"],
            "status": "active",
            "started_at": datetime.now().isoformat(),
            "deliverables": [],
            "milestones": []
        }
        
        # AI generates project plan
        project_plan = self.generate_project_plan(project)
        project["plan"] = project_plan
        
        return project
    
    def generate_project_plan(self, project):
        """
        AI generates detailed project plan
        """
        prompt = f"""Create a project plan for:

Service: {project['service_type']}
Client: {project['client_name']}

Provide:
1. Key deliverables (3-5 items)
2. Milestones with timelines
3. Success criteria
4. Communication schedule

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a project manager creating detailed plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def _get_pipeline(self, pipeline_id):
        """Get pipeline by ID"""
        for pipeline in self.onboarding_pipelines:
            if pipeline["pipeline_id"] == pipeline_id:
                return pipeline
        return None
    
    def get_pipeline_stats(self):
        """Get onboarding pipeline statistics"""
        stages = {}
        for pipeline in self.onboarding_pipelines:
            stage = pipeline["stage"]
            stages[stage] = stages.get(stage, 0) + 1
        
        return {
            "total_pipelines": len(self.onboarding_pipelines),
            "by_stage": stages,
            "active_projects": len([p for p in self.onboarding_pipelines if p["stage"] == "active_project"]),
            "conversion_rate": f"{(len([p for p in self.onboarding_pipelines if p['stage'] == 'active_project']) / len(self.onboarding_pipelines) * 100):.1f}%" if self.onboarding_pipelines else "0%"
        }
