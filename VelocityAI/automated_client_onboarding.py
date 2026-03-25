"""
Automated Client Onboarding System for VelocityAI Media
Handles complete client lifecycle from lead to active customer
"""

import json
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class AutomatedOnboardingSystem:
    """Complete automated client onboarding system"""
    
    def __init__(self):
        self.init_onboarding_database()
        self.email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "email": "onboarding@velocityai.co.za",
            "password": "your_app_password"  # Replace with actual app password
        }
        
    def init_onboarding_database(self):
        """Initialize onboarding database"""
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        
        # Onboarding pipeline
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onboarding_pipeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT UNIQUE,
                company_name TEXT,
                contact_person TEXT,
                email TEXT,
                phone TEXT,
                industry TEXT,
                monthly_revenue TEXT,
                current_ad_spend TEXT,
                pain_points TEXT,
                stage TEXT DEFAULT 'lead',
                score INTEGER DEFAULT 0,
                assigned_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP,
                next_action TEXT,
                notes TEXT
            )
        ''')
        
        # Onboarding tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS onboarding_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE,
                client_id TEXT,
                task_type TEXT,
                task_description TEXT,
                status TEXT DEFAULT 'pending',
                due_date TIMESTAMP,
                completed_at TIMESTAMP,
                assigned_to TEXT,
                priority TEXT DEFAULT 'medium'
            )
        ''')
        
        # Communication log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS communication_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id TEXT UNIQUE,
                client_id TEXT,
                communication_type TEXT,
                subject TEXT,
                content TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_received BOOLEAN DEFAULT FALSE,
                response_content TEXT,
                response_at TIMESTAMP
            )
        ''')
        
        # Document uploads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT UNIQUE,
                client_id TEXT,
                document_type TEXT,
                file_name TEXT,
                file_path TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending_review'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def capture_lead(self, lead_data: dict):
        """Capture new lead and start onboarding process"""
        client_id = str(uuid.uuid4())
        
        # Calculate lead score
        score = self.calculate_lead_score(lead_data)
        
        # Determine assigned agent based on company size
        monthly_revenue = lead_data.get('monthly_revenue', '0')
        if 'million' in monthly_revenue.lower() or int(monthly_revenue.replace('R', '').replace(',', '').replace(' ', '') or 0) > 10000000:
            assigned_agent = "enterprise_sales_001"
        elif int(monthly_revenue.replace('R', '').replace(',', '').replace(' ', '') or 0) > 1000000:
            assigned_agent = "mid_market_sales_001"
        else:
            assigned_agent = "smb_sales_001"
        
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO onboarding_pipeline 
            (client_id, company_name, contact_person, email, phone, industry, 
             monthly_revenue, current_ad_spend, pain_points, score, assigned_agent, next_action)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            client_id,
            lead_data.get('company_name'),
            lead_data.get('contact_person'),
            lead_data.get('email'),
            lead_data.get('phone'),
            lead_data.get('industry'),
            lead_data.get('monthly_revenue'),
            lead_data.get('current_ad_spend'),
            lead_data.get('pain_points'),
            score,
            assigned_agent,
            'send_welcome_email'
        ))
        
        conn.commit()
        conn.close()
        
        # Trigger automated onboarding sequence
        self.start_onboarding_sequence(client_id)
        
        return {
            'client_id': client_id,
            'score': score,
            'assigned_agent': assigned_agent,
            'status': 'onboarding_started'
        }
    
    def calculate_lead_score(self, lead_data: dict) -> int:
        """Calculate lead score based on qualification criteria"""
        score = 0
        
        # Company size (monthly revenue)
        revenue = lead_data.get('monthly_revenue', '0')
        if 'million' in revenue.lower():
            score += 40
        elif any(x in revenue for x in ['500k', '750k', '1M']):
            score += 30
        elif any(x in revenue for x in ['100k', '250k']):
            score += 20
        else:
            score += 10
        
        # Current ad spend
        ad_spend = lead_data.get('current_ad_spend', '0')
        if any(x in ad_spend for x in ['100k', '200k', '500k']):
            score += 30
        elif any(x in ad_spend for x in ['50k', '75k']):
            score += 20
        elif any(x in ad_spend for x in ['10k', '25k']):
            score += 15
        else:
            score += 5
        
        # Industry fit
        industry = lead_data.get('industry', '').lower()
        high_fit_industries = ['electronics', 'beauty', 'health', 'fashion', 'supplements']
        if any(ind in industry for ind in high_fit_industries):
            score += 20
        else:
            score += 10
        
        # Pain points alignment
        pain_points = lead_data.get('pain_points', '').lower()
        if any(pain in pain_points for pain in ['low conversion', 'expensive ads', 'poor roi']):
            score += 10
        
        return min(score, 100)
    
    def start_onboarding_sequence(self, client_id: str):
        """Start automated onboarding sequence"""
        # Create onboarding tasks
        tasks = [
            {
                'task_type': 'welcome_email',
                'description': 'Send welcome email with company overview',
                'due_date': datetime.now() + timedelta(minutes=5),
                'priority': 'high'
            },
            {
                'task_type': 'discovery_call',
                'description': 'Schedule discovery call to understand needs',
                'due_date': datetime.now() + timedelta(hours=2),
                'priority': 'high'
            },
            {
                'task_type': 'proposal_creation',
                'description': 'Create custom proposal based on discovery',
                'due_date': datetime.now() + timedelta(days=1),
                'priority': 'medium'
            },
            {
                'task_type': 'contract_preparation',
                'description': 'Prepare service agreement and contracts',
                'due_date': datetime.now() + timedelta(days=2),
                'priority': 'medium'
            },
            {
                'task_type': 'onboarding_materials',
                'description': 'Prepare onboarding materials and access',
                'due_date': datetime.now() + timedelta(days=3),
                'priority': 'low'
            }
        ]
        
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        
        for task in tasks:
            task_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO onboarding_tasks 
                (task_id, client_id, task_type, task_description, due_date, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                task_id,
                client_id,
                task['task_type'],
                task['description'],
                task['due_date'],
                task['priority']
            ))
        
        conn.commit()
        conn.close()
        
        # Send welcome email immediately
        self.send_welcome_email(client_id)
    
    def send_welcome_email(self, client_id: str):
        """Send automated welcome email"""
        # Get client details
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM onboarding_pipeline WHERE client_id = ?', (client_id,))
        client = cursor.fetchone()
        conn.close()
        
        if not client:
            return
        
        company_name = client[2]
        contact_person = client[3]
        email = client[4]
        
        # Email content
        subject = f"Welcome to VelocityAI Media, {contact_person}!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2563eb;">VelocityAI Media</h1>
                    <p style="font-size: 18px; color: #666;">AI-Powered UGC Advertising That Converts</p>
                </div>
                
                <h2>Hi {contact_person},</h2>
                
                <p>Thank you for your interest in VelocityAI Media! We're excited to help {company_name} transform your advertising with AI-powered UGC content that converts 40% better at 67% lower cost.</p>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2563eb; margin-top: 0;">What Happens Next?</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li><strong>Discovery Call:</strong> Our AI will schedule a 30-minute call to understand your specific needs</li>
                        <li><strong>Custom Proposal:</strong> We'll create a tailored proposal showing exact ROI projections</li>
                        <li><strong>Sample Content:</strong> See 5 sample UGC ads created specifically for your brand</li>
                        <li><strong>Onboarding:</strong> If you're happy, we'll have you live within 48 hours</li>
                    </ul>
                </div>
                
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #059669; margin-top: 0;">Your VelocityAI Advantage</h3>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>🎥 <strong>100 UGC videos per month</strong> (vs 10-20 traditional agencies)</li>
                        <li>⚡ <strong>48-hour turnaround</strong> (vs weeks with traditional agencies)</li>
                        <li>🎯 <strong>40% higher conversion rates</strong> with AI-optimized content</li>
                        <li>💰 <strong>67% lower cost</strong> than traditional video production</li>
                        <li>🤖 <strong>Fully autonomous</strong> - no project management needed</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://calendly.com/velocityai/discovery" 
                       style="background: #2563eb; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Schedule Your Discovery Call
                    </a>
                </div>
                
                <p>Questions? Simply reply to this email or call us at +27 11 123 4567.</p>
                
                <p>Looking forward to transforming your advertising!</p>
                
                <p><strong>Alexandra Sterling</strong><br>
                CEO, VelocityAI Media<br>
                <a href="mailto:ceo@velocityai.co.za">ceo@velocityai.co.za</a></p>
                
                <div style="border-top: 1px solid #e5e7eb; margin-top: 30px; padding-top: 20px; font-size: 12px; color: #666;">
                    <p>VelocityAI Media (Pty) Ltd | Johannesburg, South Africa | www.velocityai.co.za</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Log communication
        self.log_communication(client_id, 'email', subject, html_content)
        
        return {
            'status': 'sent',
            'client_id': client_id,
            'email': email,
            'subject': subject
        }
    
    def log_communication(self, client_id: str, comm_type: str, subject: str, content: str):
        """Log communication with client"""
        log_id = str(uuid.uuid4())
        
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO communication_log 
            (log_id, client_id, communication_type, subject, content)
            VALUES (?, ?, ?, ?, ?)
        ''', (log_id, client_id, comm_type, subject, content))
        conn.commit()
        conn.close()
    
    def schedule_discovery_call(self, client_id: str, preferred_time: str = None):
        """Schedule discovery call with client"""
        # Get client details
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM onboarding_pipeline WHERE client_id = ?', (client_id,))
        client = cursor.fetchone()
        
        if client:
            # Update stage to 'discovery_scheduled'
            cursor.execute('''
                UPDATE onboarding_pipeline 
                SET stage = 'discovery_scheduled', last_contact = CURRENT_TIMESTAMP,
                    next_action = 'conduct_discovery_call'
                WHERE client_id = ?
            ''', (client_id,))
            
            # Mark discovery call task as completed
            cursor.execute('''
                UPDATE onboarding_tasks 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE client_id = ? AND task_type = 'discovery_call'
            ''', (client_id,))
        
        conn.commit()
        conn.close()
        
        return {
            'status': 'scheduled',
            'client_id': client_id,
            'meeting_link': f'https://meet.google.com/velocityai-{client_id[:8]}',
            'calendar_link': f'https://calendly.com/velocityai/discovery?client={client_id}'
        }
    
    def create_custom_proposal(self, client_id: str, discovery_notes: dict):
        """Create custom proposal based on discovery call"""
        # Get client details
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM onboarding_pipeline WHERE client_id = ?', (client_id,))
        client = cursor.fetchone()
        conn.close()
        
        if not client:
            return None
        
        company_name = client[2]
        industry = client[6]
        monthly_revenue = client[7]
        current_ad_spend = client[8]
        
        # Calculate recommended package
        if 'million' in monthly_revenue.lower():
            package = {
                'name': 'Enterprise',
                'price': 375000,
                'videos': 100,
                'features': [
                    '100 UGC videos per month',
                    'Dedicated account manager',
                    'Custom AI training',
                    'Priority support',
                    'Advanced analytics',
                    'White-label options'
                ]
            }
        elif any(x in monthly_revenue for x in ['500k', '750k', '1M']):
            package = {
                'name': 'Premium',
                'price': 150000,
                'videos': 50,
                'features': [
                    '50 UGC videos per month',
                    'Account manager',
                    'Custom templates',
                    'Standard support',
                    'Performance analytics'
                ]
            }
        else:
            package = {
                'name': 'Standard',
                'price': 75000,
                'videos': 25,
                'features': [
                    '25 UGC videos per month',
                    'Self-service portal',
                    'Template library',
                    'Email support',
                    'Basic analytics'
                ]
            }
        
        # Calculate ROI projections
        current_spend = int(current_ad_spend.replace('R', '').replace(',', '').replace(' ', '') or 100000)
        projected_improvement = 0.40  # 40% improvement
        cost_savings = current_spend * 0.67  # 67% cost reduction
        
        proposal = {
            'client_id': client_id,
            'company_name': company_name,
            'package': package,
            'roi_projections': {
                'current_monthly_ad_spend': current_spend,
                'projected_improvement': f"{projected_improvement*100:.0f}%",
                'monthly_cost_savings': cost_savings,
                'annual_cost_savings': cost_savings * 12,
                'payback_period': '2.1 months',
                'annual_roi': f"{(cost_savings * 12 / package['price']):,.0f}%"
            },
            'implementation_timeline': {
                'contract_signing': '1 day',
                'account_setup': '1 day',
                'first_videos': '2 days',
                'full_production': '1 week'
            },
            'created_at': datetime.now().isoformat()
        }
        
        # Update client stage
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE onboarding_pipeline 
            SET stage = 'proposal_sent', last_contact = CURRENT_TIMESTAMP,
                next_action = 'follow_up_proposal'
            WHERE client_id = ?
        ''', (client_id,))
        conn.commit()
        conn.close()
        
        return proposal
    
    def process_contract_signing(self, client_id: str, signed_contract_path: str):
        """Process signed contract and activate client"""
        # Update client to active status
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE onboarding_pipeline 
            SET stage = 'active_client', last_contact = CURRENT_TIMESTAMP,
                next_action = 'begin_service_delivery'
            WHERE client_id = ?
        ''', (client_id,))
        
        # Store contract document
        document_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO client_documents 
            (document_id, client_id, document_type, file_name, file_path, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            document_id,
            client_id,
            'signed_contract',
            f'contract_{client_id}.pdf',
            signed_contract_path,
            'approved'
        ))
        
        conn.commit()
        conn.close()
        
        # Trigger service activation
        self.activate_client_services(client_id)
        
        return {
            'status': 'activated',
            'client_id': client_id,
            'document_id': document_id,
            'service_start_date': datetime.now().isoformat()
        }
    
    def activate_client_services(self, client_id: str):
        """Activate all client services"""
        # Create client account in main system
        # Set up payment processing
        # Initialize content production
        # Send welcome package
        
        activation_tasks = [
            'Create client portal access',
            'Set up payment processing',
            'Initialize AI content pipeline',
            'Schedule first content delivery',
            'Send welcome package'
        ]
        
        return {
            'status': 'services_activated',
            'client_id': client_id,
            'activation_tasks': activation_tasks,
            'portal_url': f'https://portal.velocityai.co.za/client/{client_id}',
            'first_delivery': (datetime.now() + timedelta(days=2)).isoformat()
        }
    
    def get_onboarding_pipeline(self):
        """Get current onboarding pipeline status"""
        conn = sqlite3.connect('velocityai_onboarding.db')
        cursor = conn.cursor()
        
        # Get pipeline summary
        cursor.execute('''
            SELECT stage, COUNT(*) as count 
            FROM onboarding_pipeline 
            GROUP BY stage
        ''')
        pipeline_summary = dict(cursor.fetchall())
        
        # Get recent leads
        cursor.execute('''
            SELECT client_id, company_name, contact_person, email, stage, score, created_at
            FROM onboarding_pipeline 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        recent_leads = cursor.fetchall()
        
        # Get pending tasks
        cursor.execute('''
            SELECT task_type, COUNT(*) as count
            FROM onboarding_tasks 
            WHERE status = 'pending'
            GROUP BY task_type
        ''')
        pending_tasks = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'pipeline_summary': pipeline_summary,
            'recent_leads': recent_leads,
            'pending_tasks': pending_tasks,
            'total_leads': sum(pipeline_summary.values()),
            'conversion_rate': pipeline_summary.get('active_client', 0) / max(sum(pipeline_summary.values()), 1) * 100
        }

# Test the onboarding system
if __name__ == "__main__":
    onboarding = AutomatedOnboardingSystem()
    
    print("🚀 VelocityAI Automated Onboarding System")
    print("=" * 50)
    
    # Test lead capture
    test_lead = {
        'company_name': 'TechStore Pro',
        'contact_person': 'Sarah Johnson',
        'email': 'sarah@techstore.com',
        'phone': '+27 11 123 4567',
        'industry': 'Electronics',
        'monthly_revenue': 'R2 million',
        'current_ad_spend': 'R200,000',
        'pain_points': 'Low conversion rates, expensive ads'
    }
    
    result = onboarding.capture_lead(test_lead)
    print(f"✅ Lead captured: {result['client_id']}")
    print(f"📊 Lead score: {result['score']}/100")
    print(f"👤 Assigned agent: {result['assigned_agent']}")
    
    # Test discovery call scheduling
    discovery = onboarding.schedule_discovery_call(result['client_id'])
    print(f"✅ Discovery call scheduled: {discovery['meeting_link']}")
    
    # Test proposal creation
    discovery_notes = {
        'pain_points': ['Low conversion rates', 'High cost per acquisition'],
        'goals': ['Increase ROAS', 'Scale advertising'],
        'timeline': 'ASAP'
    }
    
    proposal = onboarding.create_custom_proposal(result['client_id'], discovery_notes)
    print(f"✅ Proposal created: {proposal['package']['name']} package")
    print(f"💰 Recommended price: R{proposal['package']['price']:,}/month")
    print(f"📈 Projected ROI: {proposal['roi_projections']['annual_roi']}")
    
    # Get pipeline status
    pipeline = onboarding.get_onboarding_pipeline()
    print(f"📊 Pipeline summary: {pipeline['pipeline_summary']}")
    print(f"📈 Conversion rate: {pipeline['conversion_rate']:.1f}%")
    
    print("\n🎉 Onboarding System Ready!")
    print("🔄 Automated lead capture and scoring")
    print("📧 Automated email sequences")
    print("📞 Discovery call scheduling")
    print("📋 Custom proposal generation")
    print("📄 Contract processing")
    print("🚀 Service activation")

