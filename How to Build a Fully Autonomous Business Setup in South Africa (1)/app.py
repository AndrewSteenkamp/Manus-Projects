"""
Autonomous AI-Powered Business - Main Application
Complete implementation of Nick's $400k/month framework
"""

from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('/home/ubuntu/autonomous_business')

from agents.finance.cfo import CFOAgent
from agents.sales.cro import CROAgent
from services.upwork_automation import UpworkAutomation
from services.cold_email import ColdEmailAutomation
from services.crm import CRM

app = Flask(__name__)

# Initialize AI agents
print("🤖 Initializing AI Agents...")
cfo = CFOAgent()
cro = CROAgent()
print("✅ Agents initialized")

# Initialize services
print("⚙️  Initializing Services...")
upwork = UpworkAutomation()
cold_email = ColdEmailAutomation()
crm = CRM()
print("✅ Services ready")

# Set default niches (Nick's multi-niche strategy)
upwork.set_niches(["AI automation", "web scraping", "data analysis"])

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

# ============ AGENT ENDPOINTS ============

@app.route('/api/agent/execute', methods=['POST'])
def execute_agent_task():
    """Execute a task through an AI agent"""
    data = request.get_json()
    agent_type = data.get('agent')
    task = data.get('task')
    context = data.get('context', {})
    
    try:
        if agent_type == 'cfo':
            result = cfo.execute_task(task, context)
        elif agent_type == 'cro':
            result = cro.execute_task(task, context)
        else:
            return jsonify({'error': 'Unknown agent type'}), 400
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ FINANCE ENDPOINTS ============

@app.route('/api/finance/report', methods=['GET'])
def get_financial_report():
    """Get current financial report"""
    try:
        report = cfo.generate_financial_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/finance/analyze', methods=['GET'])
def analyze_finances():
    """AI-powered financial analysis"""
    try:
        analysis = cfo.analyze_financial_health()
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/invoice', methods=['POST'])
def create_invoice():
    """Create and process invoice"""
    data = request.get_json()
    try:
        result = cfo.process_invoice({'invoice_data': data})
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment', methods=['POST'])
def process_payment():
    """Process incoming payment"""
    data = request.get_json()
    try:
        result = cfo.process_payment({'payment_data': data})
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ SALES ENDPOINTS ============

@app.route('/api/sales/leads', methods=['POST'])
def find_leads():
    """Find new leads using AI"""
    data = request.get_json()
    try:
        result = cro.find_leads(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/loom', methods=['POST'])
def create_loom():
    """Generate Loom video script"""
    data = request.get_json()
    try:
        result = cro.create_loom_pitch(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/proposal', methods=['POST'])
def generate_proposal():
    """Generate AI-powered proposal"""
    data = request.get_json()
    try:
        result = cro.generate_proposal(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/metrics', methods=['GET'])
def get_sales_metrics():
    """Get sales performance metrics"""
    try:
        metrics = cro.get_sales_metrics()
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ UPWORK AUTOMATION ENDPOINTS ============

@app.route('/api/upwork/search', methods=['POST'])
def upwork_search():
    """Search for Upwork jobs"""
    data = request.get_json()
    niche = data.get('niche', 'AI automation')
    try:
        jobs = upwork.simulate_job_search(niche)
        return jsonify({'jobs': jobs, 'count': len(jobs)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upwork/analyze-job', methods=['POST'])
def analyze_upwork_job():
    """Analyze if an Upwork job is worth applying to"""
    data = request.get_json()
    try:
        analysis = upwork.analyze_job_posting(
            data.get('description', ''),
            data.get('title', ''),
            data.get('budget', '')
        )
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upwork/generate-proposal', methods=['POST'])
def generate_upwork_proposal():
    """Generate Upwork proposal"""
    data = request.get_json()
    try:
        proposal = upwork.generate_upwork_proposal(
            data.get('job_title', ''),
            data.get('job_description', ''),
            data.get('client_info', {})
        )
        return jsonify(proposal)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upwork/auto-apply', methods=['POST'])
def upwork_auto_apply():
    """Run complete auto-apply workflow"""
    data = request.get_json()
    niche = data.get('niche', 'AI automation')
    max_apps = data.get('max_applications', 5)
    try:
        results = upwork.auto_apply_workflow(niche, max_apps)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upwork/stats', methods=['GET'])
def upwork_stats():
    """Get Upwork automation stats"""
    try:
        stats = upwork.get_daily_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ COLD EMAIL ENDPOINTS ============

@app.route('/api/email/sequence', methods=['POST'])
def create_email_sequence():
    """Generate email sequence"""
    data = request.get_json()
    try:
        sequence = cold_email.generate_email_sequence(
            data.get('niche', ''),
            data.get('target_audience', ''),
            data.get('value_proposition', '')
        )
        return jsonify(sequence)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/personalize', methods=['POST'])
def personalize_email():
    """Personalize an email"""
    data = request.get_json()
    try:
        personalized = cold_email.personalize_email(
            data.get('template', ''),
            data.get('prospect', {})
        )
        return jsonify({'personalized_email': personalized})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/subject-lines', methods=['POST'])
def generate_subject_lines():
    """Generate subject line options"""
    data = request.get_json()
    try:
        subjects = cold_email.generate_subject_lines(
            data.get('email_body', ''),
            data.get('count', 5)
        )
        return jsonify(subjects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email/stats', methods=['GET'])
def email_stats():
    """Get email campaign stats"""
    try:
        stats = cold_email.get_campaign_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ CRM ENDPOINTS ============

@app.route('/api/crm/lead', methods=['POST'])
def add_lead():
    """Add a new lead"""
    data = request.get_json()
    try:
        lead = crm.add_lead(
            data.get('name', ''),
            data.get('company', ''),
            data.get('email', ''),
            data.get('source', ''),
            data.get('niche', '')
        )
        return jsonify(lead)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/lead/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get lead details"""
    try:
        if lead_id in crm.leads:
            return jsonify(crm.leads[lead_id])
        return jsonify({'error': 'Lead not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/lead/<lead_id>/status', methods=['PUT'])
def update_lead_status(lead_id):
    """Update lead status"""
    data = request.get_json()
    try:
        updated = crm.update_lead_status(
            lead_id,
            data.get('status', ''),
            data.get('notes', '')
        )
        return jsonify(updated)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/lead/<lead_id>/convert', methods='POST'])
def convert_lead(lead_id):
    """Convert lead to client"""
    data = request.get_json()
    try:
        client = crm.convert_to_client(
            lead_id,
            data.get('deal_value', 0),
            data.get('contract_details', {})
        )
        return jsonify(client)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/follow-ups', methods=['GET'])
def get_follow_ups():
    """Get leads needing follow-up"""
    try:
        follow_ups = crm.get_leads_needing_follow_up()
        return jsonify({'follow_ups': follow_ups, 'count': len(follow_ups)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/pipeline', methods=['GET'])
def get_pipeline():
    """Get sales pipeline stats"""
    try:
        stats = crm.get_pipeline_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crm/top-leads', methods=['GET'])
def get_top_leads():
    """Get highest-scoring leads"""
    try:
        leads = crm.get_top_leads(10)
        return jsonify({'leads': leads})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ SYSTEM ENDPOINTS ============

@app.route('/api/status', methods=['GET'])
def get_system_status():
    """Get overall system status"""
    return jsonify({
        'agents': {
            'cfo': cfo.get_status(),
            'cro': cro.get_status()
        },
        'services': {
            'upwork': upwork.get_daily_stats(),
            'email': cold_email.get_campaign_stats(),
            'crm': crm.get_pipeline_stats()
        },
        'system': 'operational'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AUTONOMOUS BUSINESS SYSTEM STARTING")
    print("="*60)
    print("📊 Dashboard: http://127.0.0.1:5000")
    print("🤖 AI Agents: CFO, CRO")
    print("⚙️  Services: Upwork, Cold Email, CRM")
    print("✅ All Systems Operational")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
