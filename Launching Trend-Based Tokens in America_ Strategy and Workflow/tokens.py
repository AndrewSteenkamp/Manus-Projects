from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.trend import Trend, Token, MarketingCampaign
import requests
import json
from datetime import datetime
import hashlib
import secrets

tokens_bp = Blueprint('tokens', __name__)

@tokens_bp.route('/tokens', methods=['GET'])
def get_tokens():
    """Get all tokens from the database"""
    tokens = Token.query.order_by(Token.created_at.desc()).all()
    return jsonify([token.to_dict() for token in tokens])

@tokens_bp.route('/tokens/create', methods=['POST'])
def create_token():
    """Create a new token based on a trend"""
    try:
        data = request.get_json()
        trend_id = data.get('trend_id')
        blockchain = data.get('blockchain', 'ethereum')
        
        if not trend_id:
            return jsonify({'status': 'error', 'message': 'trend_id is required'}), 400
        
        trend = Trend.query.get_or_404(trend_id)
        
        # Generate token details based on trend
        token_name, token_symbol = generate_token_details(trend.keyword)
        initial_supply = 1000000000  # 1 billion tokens
        
        # Simulate token creation (in real implementation, this would interact with blockchain)
        contract_address = simulate_token_deployment(token_name, token_symbol, initial_supply, blockchain)
        
        # Create token record
        new_token = Token(
            name=token_name,
            symbol=token_symbol,
            contract_address=contract_address,
            blockchain=blockchain,
            trend_id=trend_id,
            initial_supply=initial_supply,
            status='deployed'
        )
        
        db.session.add(new_token)
        
        # Mark trend as processed
        trend.is_processed = True
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Token created successfully',
            'token': new_token.to_dict()
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@tokens_bp.route('/tokens/<int:token_id>/deploy', methods=['POST'])
def deploy_token(token_id):
    """Deploy a token to the blockchain"""
    try:
        token = Token.query.get_or_404(token_id)
        
        if token.status != 'created':
            return jsonify({'status': 'error', 'message': 'Token is not in created status'}), 400
        
        # Simulate deployment process
        deployment_result = simulate_blockchain_deployment(token)
        
        if deployment_result['success']:
            token.contract_address = deployment_result['contract_address']
            token.status = 'deployed'
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Token deployed successfully',
                'contract_address': token.contract_address,
                'transaction_hash': deployment_result['transaction_hash']
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Deployment failed',
                'error': deployment_result['error']
            }), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@tokens_bp.route('/tokens/<int:token_id>/status', methods=['GET'])
def get_token_status(token_id):
    """Get the current status of a token"""
    try:
        token = Token.query.get_or_404(token_id)
        
        # Simulate getting token metrics from blockchain/exchanges
        metrics = simulate_token_metrics(token)
        
        return jsonify({
            'token': token.to_dict(),
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@tokens_bp.route('/tokens/auto-create', methods=['POST'])
def auto_create_tokens():
    """Automatically create tokens for suitable trends"""
    try:
        # Find unprocessed trends with high potential
        suitable_trends = Trend.query.filter(
            Trend.is_processed == False,
            Trend.virality_score > 0.6,
            Trend.sentiment_score > 0.5
        ).all()
        
        tokens_created = 0
        created_tokens = []
        
        for trend in suitable_trends:
            # Create token for this trend
            token_name, token_symbol = generate_token_details(trend.keyword)
            initial_supply = 1000000000
            
            contract_address = simulate_token_deployment(token_name, token_symbol, initial_supply, 'ethereum')
            
            new_token = Token(
                name=token_name,
                symbol=token_symbol,
                contract_address=contract_address,
                blockchain='ethereum',
                trend_id=trend.id,
                initial_supply=initial_supply,
                status='deployed'
            )
            
            db.session.add(new_token)
            trend.is_processed = True
            
            tokens_created += 1
            created_tokens.append(new_token.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Created {tokens_created} tokens automatically',
            'tokens_created': tokens_created,
            'tokens': created_tokens
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def generate_token_details(keyword):
    """Generate token name and symbol based on keyword"""
    # Clean and format keyword
    clean_keyword = keyword.replace(' ', '').replace('-', '').replace('_', '')
    
    # Generate token name
    token_name = f"{keyword.title()} Token"
    
    # Generate token symbol (3-5 characters)
    if len(clean_keyword) <= 5:
        token_symbol = clean_keyword.upper()
    else:
        # Take first 3 characters and add some from the end
        token_symbol = (clean_keyword[:3] + clean_keyword[-2:]).upper()
    
    return token_name, token_symbol

def simulate_token_deployment(name, symbol, supply, blockchain):
    """Simulate token deployment and return contract address"""
    # Generate a fake contract address
    hash_input = f"{name}{symbol}{supply}{blockchain}{secrets.token_hex(8)}"
    contract_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    if blockchain.lower() == 'ethereum':
        return f"0x{contract_hash[:40]}"
    elif blockchain.lower() == 'polygon':
        return f"0x{contract_hash[:40]}"
    elif blockchain.lower() == 'bsc':
        return f"0x{contract_hash[:40]}"
    else:
        return f"0x{contract_hash[:40]}"

def simulate_blockchain_deployment(token):
    """Simulate the actual blockchain deployment process"""
    # Simulate deployment success/failure
    import random
    
    if random.random() > 0.1:  # 90% success rate
        return {
            'success': True,
            'contract_address': simulate_token_deployment(token.name, token.symbol, token.initial_supply, token.blockchain),
            'transaction_hash': f"0x{secrets.token_hex(32)}"
        }
    else:
        return {
            'success': False,
            'error': 'Insufficient gas fees'
        }

def simulate_token_metrics(token):
    """Simulate token performance metrics"""
    import random
    
    # Simulate metrics based on token age and trend virality
    age_hours = (datetime.utcnow() - token.created_at).total_seconds() / 3600
    trend = token.trend
    
    base_price = 0.001  # Starting price in USD
    price_multiplier = 1 + (trend.virality_score * random.uniform(0.5, 2.0))
    current_price = base_price * price_multiplier
    
    return {
        'current_price_usd': round(current_price, 6),
        'market_cap_usd': round(current_price * token.initial_supply, 2),
        'volume_24h_usd': round(random.uniform(1000, 50000), 2),
        'holders_count': random.randint(100, 5000),
        'price_change_24h': round(random.uniform(-20, 50), 2),
        'age_hours': round(age_hours, 1)
    }

