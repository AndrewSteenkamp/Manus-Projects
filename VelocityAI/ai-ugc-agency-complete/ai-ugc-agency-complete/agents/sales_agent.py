#!/usr/bin/env python3
"""
Sales Agent - Lead Generation and Client Acquisition
Autonomous sales operations for the UGC advertising agency
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

class SalesAgent:
    """
    The Sales Agent handles all aspects of lead generation and client acquisition.
    
    Responsibilities:
    - Lead generation and prospecting
    - Lead qualification and scoring
    - Outreach campaign management
    - Sales pipeline management
    - Proposal creation and pricing
    - Client onboarding coordination
    - Sales performance tracking
    - CRM data management
    - Follow-up automation
    - Conversion optimization
    
    The Sales Agent operates autonomously to identify, qualify, and convert
    prospects into paying clients for the UGC advertising agency.
    """
    
    def __init__(self, ai_provider: str = None):
        """
        Initialize the Sales Agent with AI capabilities.
        
        Args:
            ai_provider (str): Preferred AI provider for sales intelligence
        """
        self.ai_helper = AIHelper(provider=ai_provider)
        self.agent_id = "SALES-001"
        self.name = "Sarah Rodriguez"
        self.role = "Head of Sales"
        
        # Sales configuration
        self.qualification_threshold = 70  # Minimum score for qualified leads
        self.daily_outreach_target = 50    # Daily outreach target
        self.follow_up_intervals = [1, 3, 7, 14, 30]  # Days between follow-ups
        
        # Sales pipeline stages
        self.pipeline_stages = {
            "prospect": {"conversion_rate": 0.15, "avg_time_days": 0},
            "qualified": {"conversion_rate": 0.35, "avg_time_days": 3},
            "proposal_sent": {"conversion_rate": 0.60, "avg_time_days": 7},
            "negotiation": {"conversion_rate": 0.80, "avg_time_days": 14},
            "closed_won": {"conversion_rate": 1.0, "avg_time_days": 21},
            "closed_lost": {"conversion_rate": 0.0, "avg_time_days": 21}
        }
        
        # Sales metrics tracking
        self.sales_metrics = {
            "leads_generated": 0,
            "leads_qualified": 0,
            "proposals_sent": 0,
            "deals_closed": 0,
            "revenue_generated": 0,
            "conversion_rate": 0,
            "avg_deal_size": 0,
            "sales_cycle_length": 21
        }
        
        # Lead database (in production, this would be a proper CRM)
        self.leads_database = []
        self.active_campaigns = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"SALES-{self.agent_id}")
        
        print(f"📈 Sales Agent '{self.name}' initialized")
        print(f"   Role: {self.role}")
        print(f"   AI Provider: {self.ai_helper.provider}")
        print(f"   Daily Outreach Target: {self.daily_outreach_target}")
        print(f"   Qualification Threshold: {self.qualification_threshold}%")
    
    def generate_leads(self, target_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate qualified leads based on target criteria.
        
        Args:
            target_criteria (Dict): Criteria for ideal customer profile
            
        Returns:
            List[Dict]: Generated leads with contact information and qualification scores
        """
        self.logger.info(f"Generating leads with criteria: {target_criteria.get('industry', 'All industries')}")
        
        context_prompt = f"""
        As a sales expert, generate qualified leads for our UGC advertising agency based on these criteria:
        
        TARGET CRITERIA:
        {json.dumps(target_criteria, indent=2)}
        
        IDEAL CUSTOMER PROFILE:
        - E-commerce businesses with $100K+ annual revenue
        - Companies selling physical products (beauty, health, electronics, fashion)
        - Businesses currently using paid advertising
        - Companies with social media presence
        - Brands looking to scale their marketing
        
        OUR VALUE PROPOSITION:
        - AI-powered UGC video creation
        - 10x faster than traditional methods
        - 85% cost reduction vs hiring influencers
        - Proven to increase conversion rates by 200%+
        
        Generate 20 realistic leads including:
        1. Company name and industry
        2. Contact person (decision maker)
        3. Email and phone (realistic format)
        4. Company size and revenue estimate
        5. Current marketing challenges
        6. Qualification score (0-100)
        7. Recommended approach strategy
        8. Estimated deal value
        
        Focus on companies that would genuinely benefit from UGC video content.
        Respond in JSON format with array of leads.
        """
        
        system_message = """You are Sarah Rodriguez, a top-performing B2B sales professional with 8 years experience in digital marketing services. 
        You excel at identifying high-value prospects and understanding their pain points. 
        You focus on quality over quantity and build genuine business relationships."""
        
        try:
            response = self.ai_helper.generate_response(context_prompt, system_message)
            leads_data = self._parse_leads_response(response)
            
            # Add generated leads to database
            for lead in leads_data.get("leads", []):
                lead["id"] = f"LEAD-{len(self.leads_database) + 1:04d}"
                lead["status"] = "prospect"
                lead["created_date"] = datetime.now().isoformat()
                lead["last_contact"] = None
                lead["next_follow_up"] = datetime.now().isoformat()
                self.leads_database.append(lead)
            
            generated_count = len(leads_data.get("leads", []))
            self.sales_metrics["leads_generated"] += generated_count
            
            self.logger.info(f"Generated {generated_count} new leads")
            return leads_data.get("leads", [])
            
        except Exception as e:
            self.logger.error(f"Error generating leads: {str(e)}")
            return self._create_fallback_leads()
    
    def qualify_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Qualify a lead based on BANT criteria and company fit.
        
        Args:
            lead (Dict): Lead information to qualify
            
        Returns:
            Dict: Qualification results with score and recommendations
        """
        lead_id = lead.get("id", "Unknown")
        company = lead.get("company_name", "Unknown")
        
        self.logger.info(f"Qualifying lead {lead_id}: {company}")
        
        context_prompt = f"""
        As a sales expert, qualify this lead for our UGC advertising agency:
        
        LEAD INFORMATION:
        {json.dumps(lead, indent=2)}
        
        QUALIFICATION CRITERIA (BANT):
        
        BUDGET:
        - Can they afford $5,000-$15,000/month for UGC content?
        - Do they currently spend on marketing/advertising?
        - What's their likely budget range?
        
        AUTHORITY:
        - Is the contact a decision maker?
        - Who else might be involved in the decision?
        - What's the decision-making process?
        
        NEED:
        - Do they need authentic content for their products?
        - Are they struggling with ad performance?
        - Do they want to scale their marketing?
        
        TIMELINE:
        - When do they need to improve their marketing?
        - Are there seasonal considerations?
        - What's driving urgency?
        
        ADDITIONAL FACTORS:
        - Company size and growth stage
        - Industry fit for UGC content
        - Current marketing sophistication
        - Competitive landscape
        
        Provide qualification including:
        1. Overall qualification score (0-100)
        2. BANT breakdown scores
        3. Qualification status (QUALIFIED/UNQUALIFIED/NURTURE)
        4. Key strengths and concerns
        5. Recommended next steps
        6. Estimated deal value and probability
        7. Suggested approach strategy
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            qualification = self._parse_qualification_response(response)
            
            # Update lead status based on qualification
            if qualification.get("qualification_score", 0) >= self.qualification_threshold:
                lead["status"] = "qualified"
                self.sales_metrics["leads_qualified"] += 1
                self.logger.info(f"Lead {lead_id} qualified with score {qualification.get('qualification_score', 0)}")
            else:
                lead["status"] = "nurture"
                self.logger.info(f"Lead {lead_id} moved to nurture with score {qualification.get('qualification_score', 0)}")
            
            # Update lead record
            lead["qualification"] = qualification
            lead["last_updated"] = datetime.now().isoformat()
            
            return qualification
            
        except Exception as e:
            self.logger.error(f"Error qualifying lead {lead_id}: {str(e)}")
            return self._create_fallback_qualification()
    
    def create_outreach_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and launch an automated outreach campaign.
        
        Args:
            campaign_config (Dict): Campaign configuration and targeting
            
        Returns:
            Dict: Campaign details and performance tracking setup
        """
        campaign_name = campaign_config.get("name", f"Campaign-{datetime.now().strftime('%Y%m%d')}")
        
        self.logger.info(f"Creating outreach campaign: {campaign_name}")
        
        context_prompt = f"""
        As a sales expert, create an outreach campaign for our UGC advertising agency:
        
        CAMPAIGN CONFIGURATION:
        {json.dumps(campaign_config, indent=2)}
        
        OUR SERVICES:
        - AI-powered UGC video creation
        - 3-10 videos per package
        - Pricing: $5,000-$15,000 per package
        - 48-hour delivery time
        - 200%+ conversion rate improvement
        
        TARGET AUDIENCE:
        - E-commerce business owners
        - Marketing directors
        - Brand managers
        - CMOs of growing companies
        
        Create campaign including:
        1. Email sequence (3-5 emails)
        2. LinkedIn outreach messages
        3. Follow-up cadence
        4. Personalization variables
        5. Call-to-action strategies
        6. Success metrics to track
        7. A/B testing recommendations
        
        Each message should:
        - Be personalized and relevant
        - Focus on business outcomes
        - Include social proof
        - Have clear next steps
        - Avoid being salesy or pushy
        
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            campaign = self._parse_campaign_response(response)
            
            # Add campaign to active campaigns
            campaign_record = {
                "id": f"CAMP-{len(self.active_campaigns) + 1:04d}",
                "name": campaign_name,
                "config": campaign_config,
                "campaign_data": campaign,
                "created_date": datetime.now().isoformat(),
                "status": "active",
                "metrics": {
                    "emails_sent": 0,
                    "emails_opened": 0,
                    "emails_replied": 0,
                    "meetings_booked": 0,
                    "deals_generated": 0
                }
            }
            
            self.active_campaigns.append(campaign_record)
            
            self.logger.info(f"Outreach campaign '{campaign_name}' created and activated")
            return campaign_record
            
        except Exception as e:
            self.logger.error(f"Error creating outreach campaign: {str(e)}")
            return self._create_fallback_campaign(campaign_name)
    
    def generate_proposal(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a customized proposal for a qualified lead.
        
        Args:
            lead (Dict): Qualified lead information
            
        Returns:
            Dict: Complete proposal with pricing and terms
        """
        lead_id = lead.get("id", "Unknown")
        company = lead.get("company_name", "Unknown")
        
        self.logger.info(f"Generating proposal for {lead_id}: {company}")
        
        context_prompt = f"""
        As a sales expert, create a customized proposal for this qualified lead:
        
        LEAD INFORMATION:
        {json.dumps(lead, indent=2)}
        
        OUR SERVICE PACKAGES:
        
        STARTER PACKAGE - $5,000
        - 3 UGC videos
        - Basic product research
        - Standard delivery (48 hours)
        - Email support
        
        GROWTH PACKAGE - $8,000
        - 5 UGC videos
        - Advanced market research
        - Priority delivery (24 hours)
        - Dedicated account manager
        - Performance analytics
        
        PREMIUM PACKAGE - $12,000
        - 8 UGC videos
        - Comprehensive competitor analysis
        - Same-day delivery option
        - Strategic consultation
        - A/B testing recommendations
        - Monthly performance review
        
        CUSTOM ENTERPRISE - Quote on request
        - Unlimited videos
        - White-label solution
        - API integration
        - Custom workflows
        
        Create proposal including:
        1. Executive summary tailored to their needs
        2. Recommended package with justification
        3. Custom pricing (if applicable)
        4. Timeline and deliverables
        5. Success metrics and ROI projections
        6. Case studies relevant to their industry
        7. Next steps and decision timeline
        8. Terms and conditions
        
        Make it compelling and focused on their specific business outcomes.
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            proposal = self._parse_proposal_response(response)
            
            # Update lead status
            lead["status"] = "proposal_sent"
            lead["proposal"] = proposal
            lead["proposal_sent_date"] = datetime.now().isoformat()
            lead["last_updated"] = datetime.now().isoformat()
            
            self.sales_metrics["proposals_sent"] += 1
            
            self.logger.info(f"Proposal generated for {lead_id}: {proposal.get('recommended_package', 'Unknown')} package")
            return proposal
            
        except Exception as e:
            self.logger.error(f"Error generating proposal for {lead_id}: {str(e)}")
            return self._create_fallback_proposal(lead)
    
    def manage_sales_pipeline(self) -> Dict[str, Any]:
        """
        Analyze and manage the sales pipeline with recommendations.
        
        Returns:
            Dict: Pipeline analysis with insights and action items
        """
        self.logger.info("Managing sales pipeline")
        
        # Calculate pipeline metrics
        pipeline_analysis = self._analyze_pipeline()
        
        context_prompt = f"""
        As a sales manager, analyze our current sales pipeline and provide recommendations:
        
        PIPELINE ANALYSIS:
        {json.dumps(pipeline_analysis, indent=2)}
        
        SALES METRICS:
        {json.dumps(self.sales_metrics, indent=2)}
        
        PIPELINE STAGES:
        {json.dumps(self.pipeline_stages, indent=2)}
        
        Provide analysis including:
        1. Pipeline health assessment
        2. Conversion rate analysis by stage
        3. Revenue forecasting
        4. Bottleneck identification
        5. Recommended actions for each stage
        6. Lead nurturing strategies
        7. Follow-up priorities
        8. Resource allocation recommendations
        
        Focus on actionable insights to improve sales performance.
        Respond in JSON format.
        """
        
        try:
            response = self.ai_helper.generate_response(context_prompt)
            management_plan = self._parse_pipeline_response(response)
            
            self.logger.info("Sales pipeline analysis complete")
            return {
                "pipeline_analysis": pipeline_analysis,
                "management_plan": management_plan,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error managing sales pipeline: {str(e)}")
            return self._create_fallback_pipeline_analysis()
    
    def execute_follow_ups(self) -> Dict[str, Any]:
        """
        Execute automated follow-ups for leads based on their stage and timing.
        
        Returns:
            Dict: Follow-up execution results
        """
        self.logger.info("Executing automated follow-ups")
        
        current_time = datetime.now()
        follow_ups_executed = 0
        
        for lead in self.leads_database:
            next_follow_up = datetime.fromisoformat(lead.get("next_follow_up", current_time.isoformat()))
            
            if next_follow_up <= current_time and lead["status"] not in ["closed_won", "closed_lost"]:
                follow_up_result = self._execute_single_follow_up(lead)
                if follow_up_result["executed"]:
                    follow_ups_executed += 1
        
        self.logger.info(f"Executed {follow_ups_executed} follow-ups")
        
        return {
            "follow_ups_executed": follow_ups_executed,
            "total_active_leads": len([l for l in self.leads_database if l["status"] not in ["closed_won", "closed_lost"]]),
            "execution_time": datetime.now().isoformat()
        }
    
    def get_sales_dashboard(self) -> Dict[str, Any]:
        """
        Generate sales performance dashboard.
        
        Returns:
            Dict: Comprehensive sales dashboard data
        """
        pipeline_analysis = self._analyze_pipeline()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "sales_metrics": self.sales_metrics,
            "pipeline_summary": pipeline_analysis,
            "active_campaigns": len(self.active_campaigns),
            "total_leads": len(self.leads_database),
            "qualified_leads": len([l for l in self.leads_database if l["status"] == "qualified"]),
            "proposals_pending": len([l for l in self.leads_database if l["status"] == "proposal_sent"]),
            "deals_in_negotiation": len([l for l in self.leads_database if l["status"] == "negotiation"]),
            "monthly_target": 50000,  # $50K monthly target
            "monthly_progress": self.sales_metrics["revenue_generated"],
            "ai_provider": self.ai_helper.provider,
            "cost_per_lead": self.ai_helper.get_cost_per_request() * 5  # Estimated cost per lead
        }
    
    def _analyze_pipeline(self) -> Dict[str, Any]:
        """Analyze current sales pipeline."""
        pipeline_counts = {}
        pipeline_values = {}
        
        for stage in self.pipeline_stages.keys():
            stage_leads = [l for l in self.leads_database if l["status"] == stage]
            pipeline_counts[stage] = len(stage_leads)
            pipeline_values[stage] = sum(l.get("estimated_value", 8000) for l in stage_leads)
        
        total_pipeline_value = sum(pipeline_values.values())
        weighted_pipeline_value = sum(
            pipeline_values[stage] * self.pipeline_stages[stage]["conversion_rate"]
            for stage in pipeline_values.keys()
        )
        
        return {
            "stage_counts": pipeline_counts,
            "stage_values": pipeline_values,
            "total_pipeline_value": total_pipeline_value,
            "weighted_pipeline_value": weighted_pipeline_value,
            "average_deal_size": total_pipeline_value / max(1, sum(pipeline_counts.values())),
            "conversion_rates": {stage: data["conversion_rate"] for stage, data in self.pipeline_stages.items()}
        }
    
    def _execute_single_follow_up(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Execute follow-up for a single lead."""
        # Simulate follow-up execution
        lead["last_contact"] = datetime.now().isoformat()
        
        # Set next follow-up based on stage
        days_to_next = self.follow_up_intervals[0]  # Default to 1 day
        lead["next_follow_up"] = (datetime.now() + timedelta(days=days_to_next)).isoformat()
        
        return {
            "executed": True,
            "lead_id": lead.get("id"),
            "follow_up_type": "email",
            "next_follow_up": lead["next_follow_up"]
        }
    
    def _parse_leads_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for lead generation."""
        try:
            return json.loads(response)
        except:
            return {"leads": self._create_fallback_leads()}
    
    def _parse_qualification_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for lead qualification."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_qualification()
    
    def _parse_campaign_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for campaign creation."""
        try:
            return json.loads(response)
        except:
            return {"campaign_type": "email_sequence", "status": "created"}
    
    def _parse_proposal_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for proposal generation."""
        try:
            return json.loads(response)
        except:
            return self._create_fallback_proposal({})
    
    def _parse_pipeline_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for pipeline management."""
        try:
            return json.loads(response)
        except:
            return {"recommendations": ["Review pipeline manually", "Follow up on stalled deals"]}
    
    def _create_fallback_leads(self) -> List[Dict[str, Any]]:
        """Create fallback leads when AI is unavailable."""
        return [
            {
                "company_name": "TechStyle Fashion",
                "contact_name": "Jennifer Martinez",
                "email": "j.martinez@techstyle.com",
                "industry": "Fashion E-commerce",
                "qualification_score": 85,
                "estimated_value": 12000
            },
            {
                "company_name": "HealthVita Supplements",
                "contact_name": "David Kim",
                "email": "david@healthvita.com",
                "industry": "Health & Wellness",
                "qualification_score": 78,
                "estimated_value": 8000
            }
        ]
    
    def _create_fallback_qualification(self) -> Dict[str, Any]:
        """Create fallback qualification when AI is unavailable."""
        return {
            "qualification_score": 65,
            "qualification_status": "QUALIFIED",
            "budget_score": 70,
            "authority_score": 60,
            "need_score": 80,
            "timeline_score": 50,
            "recommended_next_steps": ["Send proposal", "Schedule demo call"]
        }
    
    def _create_fallback_campaign(self, name: str) -> Dict[str, Any]:
        """Create fallback campaign when AI is unavailable."""
        return {
            "id": f"CAMP-{len(self.active_campaigns) + 1:04d}",
            "name": name,
            "status": "created",
            "campaign_data": {
                "email_sequence": ["Introduction email", "Value proposition email", "Case study email"],
                "follow_up_cadence": "1, 3, 7 days"
            },
            "created_date": datetime.now().isoformat()
        }
    
    def _create_fallback_proposal(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback proposal when AI is unavailable."""
        return {
            "recommended_package": "Growth Package",
            "price": 8000,
            "deliverables": "5 UGC videos with full production guidelines",
            "timeline": "48 hours delivery",
            "next_steps": "Schedule call to discuss details"
        }
    
    def _create_fallback_pipeline_analysis(self) -> Dict[str, Any]:
        """Create fallback pipeline analysis."""
        return {
            "pipeline_analysis": {
                "total_pipeline_value": 100000,
                "weighted_pipeline_value": 35000,
                "stage_counts": {"prospect": 20, "qualified": 8, "proposal_sent": 5}
            },
            "management_plan": {
                "recommendations": ["Follow up on proposals", "Qualify more prospects", "Focus on closing deals"]
            }
        }


def test_sales_agent():
    """Test the Sales Agent functionality."""
    print("🧪 Testing Sales Agent...")
    
    # Initialize Sales Agent
    sales = SalesAgent()
    
    # Test lead generation
    target_criteria = {
        "industry": "E-commerce",
        "company_size": "50-200 employees",
        "revenue": "$1M-$10M"
    }
    
    leads = sales.generate_leads(target_criteria)
    print(f"✅ Lead Generation: {len(leads)} leads generated")
    
    # Test lead qualification
    if leads:
        qualification = sales.qualify_lead(leads[0])
        print(f"✅ Lead Qualification: Score {qualification.get('qualification_score', 0)}")
    
    # Test proposal generation
    if leads:
        proposal = sales.generate_proposal(leads[0])
        print(f"✅ Proposal Generation: {proposal.get('recommended_package', 'Unknown')} package")
    
    # Test sales dashboard
    dashboard = sales.get_sales_dashboard()
    print(f"✅ Sales Dashboard: {dashboard['total_leads']} total leads")
    
    print("📈 Sales Agent test complete!")
    return sales


if __name__ == "__main__":
    test_sales_agent()
