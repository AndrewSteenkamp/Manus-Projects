#!/usr/bin/env python3
"""
Main Flask Application - AI-Powered UGC Advertising Agency
Web interface and API for managing the autonomous advertising agency
"""

import os
import sys
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import all agents
from agents.ceo_agent import CEOAgent
from agents.cfo_agent import CFOAgent
from agents.sales_agent import SalesAgent
from agents.creative_agent import CreativeAgent
from services.ai_helper import AIHelper

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutonomousAgency:
    """
    Main orchestrator for the autonomous UGC advertising agency.
    Manages all AI agents and coordinates their operations.
    """
    
    def __init__(self):
        """Initialize the autonomous agency with all AI agents."""
        logger.info("🚀 Initializing Autonomous UGC Advertising Agency...")
        
        # Determine AI provider
        self.ai_provider = os.getenv('AI_PROVIDER', 'huggingface')
        logger.info(f"Using AI Provider: {self.ai_provider}")
        
        # Initialize all agents
        try:
            self.ceo = CEOAgent(ai_provider=self.ai_provider)
            self.cfo = CFOAgent(ai_provider=self.ai_provider)
            self.sales = SalesAgent(ai_provider=self.ai_provider)
            self.creative = CreativeAgent(ai_provider=self.ai_provider)
            
            logger.info("✅ All agents initialized successfully")
            
            # Initialize company data
            self._initialize_company_data()
            
        except Exception as e:
            logger.error(f"❌ Error initializing agents: {str(e)}")
            raise
    
    def _initialize_company_data(self):
        """Initialize the company with sample data for demonstration."""
        # Update financial data
        initial_financial_data = {
            "monthly_revenue": 150000,
            "monthly_expenses": 22500,
            "client_acquisition_cost": 500,
            "customer_lifetime_value": 15000,
            "cash_flow": 127500,
            "accounts_receivable": 45000,
            "accounts_payable": 8000,
            "client_count": 25
        }
        
        self.cfo.update_financial_data(initial_financial_data)
        
        # Update CEO KPIs
        initial_kpis = {
            "monthly_revenue": 150000,
            "client_acquisition_rate": 8,
            "profit_margin": 85,
            "client_retention_rate": 92,
            "market_share": 2.5
        }
        
        self.ceo.update_kpis(initial_kpis)
        
        # Generate initial leads for sales
        target_criteria = {
            "industry": "E-commerce",
            "company_size": "50-500 employees",
            "revenue": "$1M-$50M",
            "location": "Global"
        }
        
        self.sales.generate_leads(target_criteria)
        
        logger.info("✅ Company data initialized")
    
    def get_executive_dashboard(self):
        """Get comprehensive executive dashboard data."""
        try:
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "company_status": "OPERATIONAL",
                "ceo_dashboard": self.ceo.get_performance_dashboard(),
                "financial_report": self.cfo.generate_financial_report(),
                "sales_dashboard": self.sales.get_sales_dashboard(),
                "creative_dashboard": self.creative.get_creative_dashboard(),
                "ai_provider": self.ai_provider,
                "system_health": "HEALTHY"
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error generating executive dashboard: {str(e)}")
            return {
                "timestamp": datetime.now().isoformat(),
                "company_status": "ERROR",
                "error": str(e)
            }
    
    def process_new_client_request(self, client_data):
        """Process a new client request through the entire pipeline."""
        try:
            logger.info(f"Processing new client request: {client_data.get('company_name', 'Unknown')}")
            
            # Step 1: Sales qualification
            qualification = self.sales.qualify_lead(client_data)
            
            if qualification.get("qualification_score", 0) < 70:
                return {
                    "status": "REJECTED",
                    "reason": "Did not meet qualification criteria",
                    "qualification": qualification
                }
            
            # Step 2: Generate proposal
            proposal = self.sales.generate_proposal(client_data)
            
            # Step 3: CFO budget approval (if needed)
            if proposal.get("price", 0) > 10000:
                budget_request = {
                    "amount": proposal.get("price", 0) * 0.1,  # 10% operational cost
                    "purpose": f"Client onboarding: {client_data.get('company_name')}",
                    "department": "operations",
                    "expected_roi": "300%"
                }
                
                approval = self.cfo.approve_expense(budget_request)
                if not approval.get("approved"):
                    return {
                        "status": "BUDGET_REJECTED",
                        "reason": approval.get("reasoning"),
                        "proposal": proposal
                    }
            
            # Step 4: Create UGC video package
            project_brief = {
                "client_name": client_data.get("company_name"),
                "product_name": client_data.get("product_name"),
                "product_category": client_data.get("industry"),
                "video_count": proposal.get("video_count", 3),
                "target_audience": client_data.get("target_audience"),
                "key_benefits": client_data.get("key_benefits", []),
                "brand_voice": client_data.get("brand_voice", "Professional")
            }
            
            video_package = self.creative.create_ugc_video_package(project_brief)
            
            # Step 5: CEO strategic approval for large deals
            if proposal.get("price", 0) > 15000:
                decision_context = {
                    "decision_type": "large_client_approval",
                    "client": client_data.get("company_name"),
                    "deal_value": proposal.get("price", 0),
                    "strategic_fit": "High-value client acquisition"
                }
                
                ceo_decision = self.ceo.make_strategic_decision(decision_context)
                if ceo_decision.get("decision") != "APPROVE":
                    return {
                        "status": "CEO_REVIEW_REQUIRED",
                        "reason": ceo_decision.get("reasoning"),
                        "proposal": proposal,
                        "video_package": video_package
                    }
            
            return {
                "status": "APPROVED",
                "qualification": qualification,
                "proposal": proposal,
                "video_package": video_package,
                "next_steps": [
                    "Send proposal to client",
                    "Schedule onboarding call",
                    "Begin video production upon approval"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error processing client request: {str(e)}")
            return {
                "status": "ERROR",
                "error": str(e)
            }

# Initialize the autonomous agency
try:
    agency = AutonomousAgency()
    logger.info("🎉 Autonomous Agency ready for operations!")
except Exception as e:
    logger.error(f"Failed to initialize agency: {str(e)}")
    agency = None

# Flask Routes

@app.route('/')
def index():
    """Main dashboard page."""
    if not agency:
        return render_template('error.html', error="Agency not initialized"), 500
    
    try:
        dashboard_data = agency.get_executive_dashboard()
        return render_template('dashboard.html', data=dashboard_data)
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        return render_template('error.html', error=str(e)), 500

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        dashboard_data = agency.get_executive_dashboard()
        return jsonify(dashboard_data)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/client/new', methods=['POST'])
def api_new_client():
    """API endpoint for processing new client requests."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        client_data = request.get_json()
        
        if not client_data:
            return jsonify({"error": "No client data provided"}), 400
        
        result = agency.process_new_client_request(client_data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing new client: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/status')
def api_agents_status():
    """API endpoint for agent status."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                "ceo": {
                    "name": agency.ceo.name,
                    "role": agency.ceo.role,
                    "status": "ACTIVE",
                    "decisions_made": len(agency.ceo.decision_history)
                },
                "cfo": {
                    "name": agency.cfo.name,
                    "role": agency.cfo.role,
                    "status": "ACTIVE",
                    "financial_records": len(agency.cfo.financial_history)
                },
                "sales": {
                    "name": agency.sales.name,
                    "role": agency.sales.role,
                    "status": "ACTIVE",
                    "leads_generated": agency.sales.sales_metrics["leads_generated"]
                },
                "creative": {
                    "name": agency.creative.name,
                    "role": agency.creative.role,
                    "status": "ACTIVE",
                    "videos_created": agency.creative.creative_metrics["videos_created"]
                }
            },
            "ai_provider": agency.ai_provider
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate/video', methods=['POST'])
def api_generate_video():
    """API endpoint for generating UGC videos."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        project_data = request.get_json()
        
        if not project_data:
            return jsonify({"error": "No project data provided"}), 400
        
        video_package = agency.creative.create_ugc_video_package(project_data)
        return jsonify(video_package)
        
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/financial/report')
def api_financial_report():
    """API endpoint for financial reports."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        report = agency.cfo.generate_financial_report()
        return jsonify(report)
        
    except Exception as e:
        logger.error(f"Error generating financial report: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sales/leads')
def api_sales_leads():
    """API endpoint for sales leads."""
    if not agency:
        return jsonify({"error": "Agency not initialized"}), 500
    
    try:
        leads_data = {
            "total_leads": len(agency.sales.leads_database),
            "qualified_leads": len([l for l in agency.sales.leads_database if l["status"] == "qualified"]),
            "recent_leads": agency.sales.leads_database[-10:],  # Last 10 leads
            "sales_metrics": agency.sales.sales_metrics
        }
        
        return jsonify(leads_data)
        
    except Exception as e:
        logger.error(f"Error getting sales leads: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    if not agency:
        return jsonify({"status": "UNHEALTHY", "error": "Agency not initialized"}), 500
    
    return jsonify({
        "status": "HEALTHY",
        "timestamp": datetime.now().isoformat(),
        "ai_provider": agency.ai_provider,
        "agents_active": 4
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    # Development server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"🌐 Starting web server on port {port}")
    logger.info(f"🔧 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
