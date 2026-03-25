"""
Cold Outreach Service for UGC Ads Agency
Integrates with Instantly, Smartlead, InboxApp, Drippy.ai, and Phantom Buster
Automates cold email and social media outreach across all e-commerce platforms
"""

import requests
import json
import time
from typing import List, Dict, Any
import sqlite3
from datetime import datetime, timedelta
import random

class ColdOutreachService:
    def __init__(self):
        # Email service API keys
        self.instantly_api_key = "YOUR_INSTANTLY_API_KEY"
        self.smartlead_api_key = "YOUR_SMARTLEAD_API_KEY"
        self.hyper_tide_api_key = "YOUR_HYPER_TIDE_API_KEY"
        
        # Social media automation API keys
        self.inboxapp_api_key = "YOUR_INBOXAPP_API_KEY"
        self.drippy_api_key = "YOUR_DRIPPY_API_KEY"
        self.phantom_buster_api_key = "YOUR_PHANTOM_BUSTER_API_KEY"
        
        # Initialize outreach database
        self.init_outreach_database()
        
        # Email templates for different platforms and categories
        self.email_templates = {
            "shopify": {
                "subject_lines": [
                    "Quick question about {{company_name}}'s ad creative",
                    "Saw {{company_name}} on Shopify - impressed!",
                    "{{company_name}} + AI-generated UGC ads?",
                    "100 video ads for {{company_name}} - interested?"
                ],
                "templates": [
                    """Hi {{contact_name}},

I noticed {{company_name}} is doing great things in the {{category}} space on Shopify.

Quick question: How much are you currently spending on video ad creative each month?

We just helped a similar {{category}} brand generate 100 high-converting UGC-style video ads for $5,000/month (normally costs $15,000+ with traditional creators).

Would you be interested in seeing 5 sample ads we could create for {{company_name}} at no cost?

Best,
[Your Name]

P.S. - The whole process is AI-automated, so turnaround is 48 hours instead of weeks."""
                ]
            },
            "woocommerce": {
                "subject_lines": [
                    "{{company_name}}'s WooCommerce store caught my attention",
                    "Quick win for {{company_name}}'s video ads",
                    "100 UGC ads for {{company_name}} - $5K/month",
                    "Scaling {{company_name}}'s ad creative efficiently"
                ],
                "templates": [
                    """Hi {{contact_name}},

Love what {{company_name}} is doing in the {{category}} market with WooCommerce!

I'm reaching out because we specialize in helping {{category}} brands scale their video ad creative without the usual headaches.

Instead of paying $150+ per UGC video, we use AI to generate 100 high-quality video ads for just $5,000/month.

Would you be open to seeing 5 free sample ads for {{company_name}}?

Best regards,
[Your Name]"""
                ]
            },
            "magento": {
                "subject_lines": [
                    "Impressed by {{company_name}}'s Magento setup",
                    "Enterprise-level ad creative for {{company_name}}",
                    "{{company_name}} + scalable video ads",
                    "100 video ads monthly - interested?"
                ],
                "templates": [
                    """Hi {{contact_name}},

{{company_name}}'s Magento store shows you're serious about scaling in the {{category}} space.

Quick question: What's your biggest challenge with video ad creative right now?

We help enterprise {{category}} brands generate 100 professional UGC-style video ads monthly for $5,000 (vs $15,000+ with traditional methods).

The entire process is AI-automated, so you get consistent quality and fast turnaround.

Would you like to see 5 sample ads we could create for {{company_name}}?

Best,
[Your Name]"""
                ]
            },
            "custom": {
                "subject_lines": [
                    "{{company_name}}'s custom e-commerce impressed me",
                    "Scaling video ads for {{company_name}}",
                    "100 UGC ads for your {{category}} brand",
                    "Custom solution for {{company_name}}'s ad creative"
                ],
                "templates": [
                    """Hi {{contact_name}},

Your custom e-commerce setup for {{company_name}} shows you're not messing around with scaling in {{category}}.

I'm reaching out because most brands your size struggle with one thing: generating enough high-quality video ad creative to test and scale profitably.

We solve this with AI-generated UGC-style videos. 100 ads per month for $5,000 (normally costs $15,000+ with creators).

Would you be interested in seeing 5 free sample ads for {{company_name}}?

Best regards,
[Your Name]"""
                ]
            }
        }
        
        # Social media templates
        self.social_templates = {
            "twitter": [
                "Hey {{contact_name}}, love what {{company_name}} is doing in {{category}}! Quick question about your video ad strategy - mind if I DM you?",
                "{{company_name}} caught my eye - impressive {{category}} brand! Would love to show you how we're helping similar brands scale video ads with AI.",
                "Saw {{company_name}} and had to reach out. We just helped a {{category}} brand generate 100 video ads for $5K/month instead of $15K+. Interested in learning more?"
            ],
            "linkedin": [
                "Hi {{contact_name}}, I came across {{company_name}} and was impressed by your work in the {{category}} space. I'd love to share how we're helping similar brands scale their video ad creative with AI - would you be open to a brief conversation?",
                "{{contact_name}}, {{company_name}} is doing great things in {{category}}! Quick question: what's your current approach to video ad creative? We've developed an AI solution that might interest you.",
                "Hi {{contact_name}}, I noticed {{company_name}} is growing fast in the {{category}} market. We specialize in helping brands like yours generate 100 high-quality video ads monthly for a fraction of the traditional cost. Would you be interested in learning more?"
            ]
        }
    
    def init_outreach_database(self):
        """Initialize database for tracking outreach campaigns"""
        conn = sqlite3.connect('outreach.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outreach_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT,
                domain TEXT,
                company_name TEXT,
                contact_email TEXT,
                contact_name TEXT,
                category TEXT,
                ecommerce_platform TEXT,
                campaign_type TEXT,
                template_used TEXT,
                subject_line TEXT,
                message_content TEXT,
                sent_at TIMESTAMP,
                opened BOOLEAN DEFAULT FALSE,
                clicked BOOLEAN DEFAULT FALSE,
                replied BOOLEAN DEFAULT FALSE,
                reply_content TEXT,
                status TEXT DEFAULT 'sent',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS social_outreach (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT,
                domain TEXT,
                company_name TEXT,
                contact_name TEXT,
                platform TEXT,
                profile_url TEXT,
                message_content TEXT,
                sent_at TIMESTAMP,
                responded BOOLEAN DEFAULT FALSE,
                response_content TEXT,
                status TEXT DEFAULT 'sent',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_email_campaign(self, leads: List[Dict], platform_filter: str = "all") -> Dict[str, Any]:
        """
        Create and launch email campaign using Instantly or Smartlead
        """
        try:
            campaign_results = []
            
            # Filter leads by platform if specified
            if platform_filter != "all":
                leads = [lead for lead in leads if lead.get('ecommerce_platform') == platform_filter]
            
            for lead in leads:
                # Select appropriate template based on e-commerce platform
                platform = lead.get('ecommerce_platform', 'custom')
                category = lead.get('category', 'general')
                
                # Get template for this platform
                platform_templates = self.email_templates.get(platform, self.email_templates['custom'])
                
                # Select random subject line and template
                subject_template = random.choice(platform_templates['subject_lines'])
                email_template = random.choice(platform_templates['templates'])
                
                # Personalize the email
                personalized_subject = self.personalize_template(subject_template, lead)
                personalized_email = self.personalize_template(email_template, lead)
                
                # Send email via Instantly API (simulated)
                email_result = self.send_email_instantly(
                    lead.get('email', ''),
                    personalized_subject,
                    personalized_email,
                    lead
                )
                
                campaign_results.append(email_result)
                
                # Save to database
                self.save_email_outreach(lead, personalized_subject, personalized_email, email_result)
                
                # Rate limiting
                time.sleep(random.uniform(1, 3))
            
            return {
                "success": True,
                "campaign_type": "email",
                "platform_filter": platform_filter,
                "total_sent": len(campaign_results),
                "successful_sends": len([r for r in campaign_results if r.get('sent', False)]),
                "results": campaign_results[:10]  # Return first 10 for preview
            }
            
        except Exception as e:
            print(f"Error creating email campaign: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_email_instantly(self, email: str, subject: str, content: str, lead: Dict) -> Dict[str, Any]:
        """
        Send email via Instantly API
        """
        try:
            # Simulate Instantly API call
            # In production, this would call the actual Instantly API
            
            # Simulate 95% success rate
            success = random.random() > 0.05
            
            if success:
                return {
                    "sent": True,
                    "email": email,
                    "message_id": f"instantly_{int(time.time())}_{random.randint(1000, 9999)}",
                    "status": "delivered",
                    "sent_at": datetime.now().isoformat()
                }
            else:
                return {
                    "sent": False,
                    "email": email,
                    "error": "Delivery failed",
                    "status": "failed"
                }
                
        except Exception as e:
            return {
                "sent": False,
                "email": email,
                "error": str(e),
                "status": "error"
            }
    
    def create_social_campaign(self, leads: List[Dict], platform: str = "linkedin") -> Dict[str, Any]:
        """
        Create social media outreach campaign
        """
        try:
            campaign_results = []
            
            for lead in leads:
                # Select appropriate social template
                templates = self.social_templates.get(platform, self.social_templates['linkedin'])
                message_template = random.choice(templates)
                
                # Personalize the message
                personalized_message = self.personalize_template(message_template, lead)
                
                # Send social message (simulated)
                social_result = self.send_social_message(
                    platform,
                    lead.get('contact_name', ''),
                    personalized_message,
                    lead
                )
                
                campaign_results.append(social_result)
                
                # Save to database
                self.save_social_outreach(lead, platform, personalized_message, social_result)
                
                # Rate limiting for social platforms
                time.sleep(random.uniform(5, 15))
            
            return {
                "success": True,
                "campaign_type": "social",
                "platform": platform,
                "total_sent": len(campaign_results),
                "successful_sends": len([r for r in campaign_results if r.get('sent', False)]),
                "results": campaign_results[:10]
            }
            
        except Exception as e:
            print(f"Error creating social campaign: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_social_message(self, platform: str, contact_name: str, message: str, lead: Dict) -> Dict[str, Any]:
        """
        Send social media message via platform APIs
        """
        try:
            # Simulate social media API calls
            # In production, this would use Phantom Buster, InboxApp, or Drippy.ai
            
            success = random.random() > 0.1  # 90% success rate
            
            if success:
                return {
                    "sent": True,
                    "platform": platform,
                    "contact_name": contact_name,
                    "message_id": f"{platform}_{int(time.time())}_{random.randint(1000, 9999)}",
                    "status": "delivered",
                    "sent_at": datetime.now().isoformat()
                }
            else:
                return {
                    "sent": False,
                    "platform": platform,
                    "contact_name": contact_name,
                    "error": "Message delivery failed",
                    "status": "failed"
                }
                
        except Exception as e:
            return {
                "sent": False,
                "platform": platform,
                "contact_name": contact_name,
                "error": str(e),
                "status": "error"
            }
    
    def personalize_template(self, template: str, lead: Dict) -> str:
        """
        Personalize email/message templates with lead data
        """
        try:
            personalized = template
            
            # Replace placeholders with lead data
            replacements = {
                "{{company_name}}": lead.get('company_name', 'your company'),
                "{{contact_name}}": lead.get('contact_name', 'there'),
                "{{category}}": lead.get('category', 'e-commerce'),
                "{{domain}}": lead.get('domain', ''),
                "{{platform}}": lead.get('ecommerce_platform', 'e-commerce platform')
            }
            
            for placeholder, value in replacements.items():
                personalized = personalized.replace(placeholder, value)
            
            return personalized
            
        except Exception as e:
            print(f"Error personalizing template: {str(e)}")
            return template
    
    def save_email_outreach(self, lead: Dict, subject: str, content: str, result: Dict):
        """
        Save email outreach to database
        """
        try:
            conn = sqlite3.connect('outreach.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO outreach_campaigns 
                (lead_id, domain, company_name, contact_email, contact_name, category, 
                 ecommerce_platform, campaign_type, subject_line, message_content, 
                 sent_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead.get('id', ''),
                lead.get('domain', ''),
                lead.get('company_name', ''),
                lead.get('email', ''),
                lead.get('contact_name', ''),
                lead.get('category', ''),
                lead.get('ecommerce_platform', ''),
                'email',
                subject,
                content,
                result.get('sent_at'),
                result.get('status', 'unknown')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving email outreach: {str(e)}")
    
    def save_social_outreach(self, lead: Dict, platform: str, message: str, result: Dict):
        """
        Save social media outreach to database
        """
        try:
            conn = sqlite3.connect('outreach.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO social_outreach 
                (lead_id, domain, company_name, contact_name, platform, 
                 message_content, sent_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead.get('id', ''),
                lead.get('domain', ''),
                lead.get('company_name', ''),
                lead.get('contact_name', ''),
                platform,
                message,
                result.get('sent_at'),
                result.get('status', 'unknown')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving social outreach: {str(e)}")
    
    def get_campaign_stats(self, days: int = 30) -> Dict[str, Any]:
        """
        Get outreach campaign statistics
        """
        try:
            conn = sqlite3.connect('outreach.db')
            cursor = conn.cursor()
            
            # Get date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Email campaign stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_emails,
                    SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) as opened,
                    SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) as clicked,
                    SUM(CASE WHEN replied = 1 THEN 1 ELSE 0 END) as replied,
                    ecommerce_platform
                FROM outreach_campaigns 
                WHERE created_at >= ? AND created_at <= ?
                GROUP BY ecommerce_platform
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            email_stats = cursor.fetchall()
            
            # Social campaign stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_messages,
                    SUM(CASE WHEN responded = 1 THEN 1 ELSE 0 END) as responded,
                    platform
                FROM social_outreach 
                WHERE created_at >= ? AND created_at <= ?
                GROUP BY platform
            ''', (start_date.isoformat(), end_date.isoformat()))
            
            social_stats = cursor.fetchall()
            
            conn.close()
            
            return {
                "success": True,
                "period_days": days,
                "email_stats": email_stats,
                "social_stats": social_stats,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting campaign stats: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Example usage and testing
if __name__ == "__main__":
    service = ColdOutreachService()
    
    # Test leads data
    test_leads = [
        {
            "id": "1",
            "domain": "test-supplements.com",
            "company_name": "Test Supplements Co",
            "email": "marketing@test-supplements.com",
            "contact_name": "John Smith",
            "category": "supplements",
            "ecommerce_platform": "shopify"
        }
    ]
    
    # Test email campaign
    email_result = service.create_email_campaign(test_leads)
    print("Email Campaign Result:")
    print(json.dumps(email_result, indent=2))
    
    # Test social campaign
    social_result = service.create_social_campaign(test_leads, "linkedin")
    print("\nSocial Campaign Result:")
    print(json.dumps(social_result, indent=2))

