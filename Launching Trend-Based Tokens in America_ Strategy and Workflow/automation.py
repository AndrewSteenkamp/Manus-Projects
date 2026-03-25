from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.trend import Trend, Token, MarketingCampaign
from src.routes.trends import fetch_trends
from src.routes.tokens import auto_create_tokens
from src.routes.marketing import auto_launch_campaigns
from src.routes.trading import update_performance, generate_trading_signals, auto_trade
import json
from datetime import datetime
import threading
import time

automation_bp = Blueprint('automation', __name__)

# Global variable to track automation status
automation_status = {
    'running': False,
    'last_run': None,
    'cycles_completed': 0,
    'errors': []
}

@automation_bp.route('/automation/status', methods=['GET'])
def get_automation_status():
    """Get current automation status"""
    return jsonify(automation_status)

@automation_bp.route('/automation/start', methods=['POST'])
def start_automation():
    """Start the full automation cycle"""
    global automation_status
    
    if automation_status['running']:
        return jsonify({'status': 'error', 'message': 'Automation is already running'}), 400
    
    try:
        # Start automation in a separate thread
        automation_thread = threading.Thread(target=run_automation_cycle, daemon=True)
        automation_thread.start()
        
        automation_status['running'] = True
        automation_status['last_run'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'status': 'success',
            'message': 'Automation started successfully'
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@automation_bp.route('/automation/stop', methods=['POST'])
def stop_automation():
    """Stop the automation cycle"""
    global automation_status
    
    automation_status['running'] = False
    
    return jsonify({
        'status': 'success',
        'message': 'Automation stopped'
    })

@automation_bp.route('/automation/run-once', methods=['POST'])
def run_automation_once():
    """Run one complete automation cycle"""
    try:
        cycle_result = execute_automation_cycle()
        
        return jsonify({
            'status': 'success',
            'message': 'Automation cycle completed',
            'results': cycle_result
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@automation_bp.route('/automation/dashboard', methods=['GET'])
def get_dashboard():
    """Get comprehensive dashboard data"""
    try:
        # Get counts for different entities
        trends_count = Trend.query.count()
        tokens_count = Token.query.count()
        campaigns_count = MarketingCampaign.query.count()
        
        # Get recent activity
        recent_trends = Trend.query.order_by(Trend.created_at.desc()).limit(5).all()
        recent_tokens = Token.query.order_by(Token.created_at.desc()).limit(5).all()
        recent_campaigns = MarketingCampaign.query.order_by(MarketingCampaign.created_at.desc()).limit(5).all()
        
        # Get token status distribution
        token_statuses = db.session.query(Token.status, db.func.count(Token.id)).group_by(Token.status).all()
        status_distribution = {status: count for status, count in token_statuses}
        
        dashboard_data = {
            'summary': {
                'total_trends': trends_count,
                'total_tokens': tokens_count,
                'total_campaigns': campaigns_count,
                'automation_status': automation_status
            },
            'recent_activity': {
                'trends': [trend.to_dict() for trend in recent_trends],
                'tokens': [token.to_dict() for token in recent_tokens],
                'campaigns': [campaign.to_dict() for campaign in recent_campaigns]
            },
            'token_status_distribution': status_distribution
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def run_automation_cycle():
    """Run the continuous automation cycle"""
    global automation_status
    
    while automation_status['running']:
        try:
            cycle_result = execute_automation_cycle()
            automation_status['cycles_completed'] += 1
            automation_status['last_run'] = datetime.utcnow().isoformat()
            
            # Log cycle completion
            print(f"Automation cycle {automation_status['cycles_completed']} completed: {cycle_result}")
            
            # Wait before next cycle (e.g., 30 minutes)
            time.sleep(1800)  # 30 minutes
            
        except Exception as e:
            error_msg = f"Automation cycle error: {str(e)}"
            automation_status['errors'].append({
                'timestamp': datetime.utcnow().isoformat(),
                'error': error_msg
            })
            print(error_msg)
            
            # Wait before retrying (e.g., 5 minutes)
            time.sleep(300)  # 5 minutes

def execute_automation_cycle():
    """Execute one complete automation cycle"""
    cycle_results = {}
    
    # Step 1: Fetch new trends
    print("Step 1: Fetching trends...")
    try:
        # Simulate calling the fetch_trends function
        trends_result = simulate_fetch_trends()
        cycle_results['trends_fetched'] = trends_result
    except Exception as e:
        cycle_results['trends_error'] = str(e)
    
    # Step 2: Auto-create tokens for suitable trends
    print("Step 2: Creating tokens...")
    try:
        tokens_result = simulate_auto_create_tokens()
        cycle_results['tokens_created'] = tokens_result
    except Exception as e:
        cycle_results['tokens_error'] = str(e)
    
    # Step 3: Launch marketing campaigns for new tokens
    print("Step 3: Launching marketing campaigns...")
    try:
        marketing_result = simulate_auto_launch_campaigns()
        cycle_results['campaigns_launched'] = marketing_result
    except Exception as e:
        cycle_results['marketing_error'] = str(e)
    
    # Step 4: Update token performance data
    print("Step 4: Updating performance data...")
    try:
        performance_result = simulate_update_performance()
        cycle_results['performance_updated'] = performance_result
    except Exception as e:
        cycle_results['performance_error'] = str(e)
    
    # Step 5: Generate trading signals
    print("Step 5: Generating trading signals...")
    try:
        signals_result = simulate_generate_trading_signals()
        cycle_results['signals_generated'] = signals_result
    except Exception as e:
        cycle_results['signals_error'] = str(e)
    
    # Step 6: Execute high-confidence trades
    print("Step 6: Executing trades...")
    try:
        trading_result = simulate_auto_trade()
        cycle_results['trades_executed'] = trading_result
    except Exception as e:
        cycle_results['trading_error'] = str(e)
    
    return cycle_results

def simulate_fetch_trends():
    """Simulate fetching trends (would call actual function in production)"""
    # In production, this would call the actual fetch_trends function
    # For now, we'll simulate the result
    return {
        'trends_added': 3,
        'status': 'success'
    }

def simulate_auto_create_tokens():
    """Simulate auto-creating tokens (would call actual function in production)"""
    # In production, this would call the actual auto_create_tokens function
    return {
        'tokens_created': 1,
        'status': 'success'
    }

def simulate_auto_launch_campaigns():
    """Simulate auto-launching campaigns (would call actual function in production)"""
    # In production, this would call the actual auto_launch_campaigns function
    return {
        'campaigns_created': 2,
        'status': 'success'
    }

def simulate_update_performance():
    """Simulate updating performance (would call actual function in production)"""
    # In production, this would call the actual update_performance function
    return {
        'updates_count': 5,
        'status': 'success'
    }

def simulate_generate_trading_signals():
    """Simulate generating trading signals (would call actual function in production)"""
    # In production, this would call the actual generate_trading_signals function
    return {
        'signals_generated': 3,
        'status': 'success'
    }

def simulate_auto_trade():
    """Simulate auto-trading (would call actual function in production)"""
    # In production, this would call the actual auto_trade function
    return {
        'executed_count': 1,
        'status': 'success'
    }

