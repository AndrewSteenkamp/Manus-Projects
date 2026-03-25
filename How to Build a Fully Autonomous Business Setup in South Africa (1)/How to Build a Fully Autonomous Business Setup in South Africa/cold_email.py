"""
Cold Email Automation Service
Implements Nick's cold email strategy using AI
Integrates with Instantly.ai or similar platforms
"""

import json
from datetime import datetime
from openai import OpenAI

class ColdEmailAutomation:
    """
    Automated cold email campaigns for client acquisition
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.campaigns = []
        self.email_sequences = {}
        
    def generate_email_sequence(self, niche, target_audience, value_proposition):
        """
        Generate a complete 5-email sequence
        Nick's strategy: Value-first, not salesy
        """
        prompt = f"""Create a 5-email cold outreach sequence for:

Niche: {niche}
Target: {target_audience}
Value Prop: {value_proposition}

Each email should:
- Be 50-100 words
- Provide value before asking
- Have a clear but soft CTA
- Build on previous email
- Not be pushy

Email 1: Introduction + Value
Email 2: Case study/proof
Email 3: Specific insight for their business
Email 4: Soft offer
Email 5: Final follow-up

Respond in JSON:
{{
    "email_1": {{"subject": "", "body": ""}},
    "email_2": {{"subject": "", "body": ""}},
    "email_3": {{"subject": "", "body": ""}},
    "email_4": {{"subject": "", "body": ""}},
    "email_5": {{"subject": "", "body": ""}}
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a cold email expert with 40% response rates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            sequence = json.loads(response.choices[0].message.content)
            sequence_id = f"SEQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            self.email_sequences[sequence_id] = {
                "sequence": sequence,
                "niche": niche,
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "sequence_id": sequence_id,
                "sequence": sequence
            }
        except Exception as e:
            return {"error": str(e)}
    
    def personalize_email(self, email_template, prospect_data):
        """
        AI-powered email personalization
        """
        prompt = f"""Personalize this email template for a specific prospect:

Template: {email_template}

Prospect Info:
- Name: {prospect_data.get('name', 'Unknown')}
- Company: {prospect_data.get('company', 'Unknown')}
- Industry: {prospect_data.get('industry', 'Unknown')}
- Recent Activity: {prospect_data.get('recent_activity', 'None')}

Add 1-2 sentences of genuine personalization that shows you researched them.
Keep the overall structure but make it feel personal.

Respond with just the personalized email text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at personalizing cold emails."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return email_template  # Fallback to template
    
    def generate_subject_lines(self, email_body, count=5):
        """
        Generate multiple subject line options
        A/B testing is key to cold email success
        """
        prompt = f"""Generate {count} compelling subject lines for this email:

{email_body}

Subject lines should:
- Be 3-7 words
- Create curiosity
- Not be clickbait
- Be relevant to content
- Avoid spam triggers

Respond in JSON:
{{
    "subject_lines": ["line1", "line2", ...]
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a subject line expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"subject_lines": ["Quick question", "Thought of you"]}
    
    def analyze_email_performance(self, campaign_data):
        """
        AI analysis of email campaign performance
        """
        prompt = f"""Analyze this email campaign performance:

Sent: {campaign_data.get('sent', 0)}
Opened: {campaign_data.get('opened', 0)}
Clicked: {campaign_data.get('clicked', 0)}
Replied: {campaign_data.get('replied', 0)}

Open Rate: {campaign_data.get('open_rate', 0)}%
Click Rate: {campaign_data.get('click_rate', 0)}%
Reply Rate: {campaign_data.get('reply_rate', 0)}%

Provide:
1. Performance assessment
2. What's working
3. What needs improvement
4. Specific recommendations

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a cold email analytics expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def create_campaign(self, campaign_name, niche, target_list, sequence_id):
        """
        Create a new email campaign
        """
        campaign = {
            "campaign_id": f"CAMP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "name": campaign_name,
            "niche": niche,
            "sequence_id": sequence_id,
            "target_count": len(target_list),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "stats": {
                "sent": 0,
                "opened": 0,
                "clicked": 0,
                "replied": 0
            }
        }
        
        self.campaigns.append(campaign)
        return campaign
    
    def generate_lead_list(self, niche, target_criteria):
        """
        AI-powered lead list generation
        """
        prompt = f"""Generate ideal lead criteria for {niche}:

Target Criteria: {target_criteria}

Provide:
1. Ideal company size
2. Industries to target
3. Job titles to reach out to
4. Geographic focus
5. Where to find these leads (LinkedIn, databases, etc.)

Respond in JSON format."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a lead generation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}
    
    def get_campaign_stats(self):
        """
        Get overall campaign statistics
        """
        total_sent = sum(c["stats"]["sent"] for c in self.campaigns)
        total_replied = sum(c["stats"]["replied"] for c in self.campaigns)
        
        return {
            "total_campaigns": len(self.campaigns),
            "active_campaigns": len([c for c in self.campaigns if c["status"] == "active"]),
            "total_emails_sent": total_sent,
            "total_replies": total_replied,
            "overall_reply_rate": f"{(total_replied / total_sent * 100):.2f}%" if total_sent > 0 else "0%",
            "recent_campaigns": self.campaigns[-5:]
        }
