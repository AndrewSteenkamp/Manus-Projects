from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.trend import Trend, Token, MarketingCampaign
import requests
import json
from datetime import datetime, timedelta
import random
import secrets

trading_bp = Blueprint('trading', __name__)

class TokenPerformance(db.Model):
    __tablename__ = 'token_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    market_cap_usd = db.Column(db.Float, nullable=False)
    volume_24h_usd = db.Column(db.Float, nullable=False)
    holders_count = db.Column(db.Integer, nullable=False)
    price_change_24h = db.Column(db.Float, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    token = db.relationship('Token', backref=db.backref('performance_history', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_id': self.token_id,
            'price_usd': self.price_usd,
            'market_cap_usd': self.market_cap_usd,
            'volume_24h_usd': self.volume_24h_usd,
            'holders_count': self.holders_count,
            'price_change_24h': self.price_change_24h,
            'sentiment_score': self.sentiment_score,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }

class TradingSignal(db.Model):
    __tablename__ = 'trading_signals'
    
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=False)
    signal_type = db.Column(db.String(50), nullable=False)  # buy, sell, hold
    confidence = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    target_price = db.Column(db.Float, nullable=True)
    stop_loss = db.Column(db.Float, nullable=True)
    executed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    token = db.relationship('Token', backref=db.backref('trading_signals', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_id': self.token_id,
            'signal_type': self.signal_type,
            'confidence': self.confidence,
            'reason': self.reason,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'executed': self.executed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@trading_bp.route('/trading/performance', methods=['GET'])
def get_all_performance():
    """Get performance data for all tokens"""
    performance_data = TokenPerformance.query.order_by(TokenPerformance.recorded_at.desc()).limit(100).all()
    return jsonify([perf.to_dict() for perf in performance_data])

@trading_bp.route('/trading/performance/<int:token_id>', methods=['GET'])
def get_token_performance(token_id):
    """Get performance history for a specific token"""
    token = Token.query.get_or_404(token_id)
    performance_data = TokenPerformance.query.filter_by(token_id=token_id).order_by(TokenPerformance.recorded_at.desc()).all()
    
    return jsonify({
        'token': token.to_dict(),
        'performance_history': [perf.to_dict() for perf in performance_data]
    })

@trading_bp.route('/trading/performance/update', methods=['POST'])
def update_performance():
    """Update performance data for all active tokens"""
    try:
        # Get all tokens that are in trading phase
        active_tokens = Token.query.filter(Token.status.in_(['deployed', 'marketing', 'trading'])).all()
        
        updates_count = 0
        
        for token in active_tokens:
            # Simulate getting current market data
            current_metrics = simulate_current_token_metrics(token)
            
            # Create performance record
            performance = TokenPerformance(
                token_id=token.id,
                price_usd=current_metrics['current_price_usd'],
                market_cap_usd=current_metrics['market_cap_usd'],
                volume_24h_usd=current_metrics['volume_24h_usd'],
                holders_count=current_metrics['holders_count'],
                price_change_24h=current_metrics['price_change_24h'],
                sentiment_score=current_metrics.get('sentiment_score', 0.5)
            )
            
            db.session.add(performance)
            updates_count += 1
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Updated performance data for {updates_count} tokens',
            'updates_count': updates_count
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trading_bp.route('/trading/signals', methods=['GET'])
def get_trading_signals():
    """Get all trading signals"""
    signals = TradingSignal.query.order_by(TradingSignal.created_at.desc()).all()
    return jsonify([signal.to_dict() for signal in signals])

@trading_bp.route('/trading/signals/generate', methods=['POST'])
def generate_trading_signals():
    """Generate trading signals for all active tokens"""
    try:
        # Get all tokens with recent performance data
        active_tokens = Token.query.filter(Token.status.in_(['deployed', 'marketing', 'trading'])).all()
        
        signals_generated = 0
        generated_signals = []
        
        for token in active_tokens:
            # Get recent performance data
            recent_performance = TokenPerformance.query.filter_by(token_id=token.id).order_by(TokenPerformance.recorded_at.desc()).limit(10).all()
            
            if len(recent_performance) >= 3:  # Need at least 3 data points
                signal = analyze_token_and_generate_signal(token, recent_performance)
                
                if signal:
                    new_signal = TradingSignal(
                        token_id=token.id,
                        signal_type=signal['type'],
                        confidence=signal['confidence'],
                        reason=signal['reason'],
                        target_price=signal.get('target_price'),
                        stop_loss=signal.get('stop_loss')
                    )
                    
                    db.session.add(new_signal)
                    signals_generated += 1
                    generated_signals.append(new_signal.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Generated {signals_generated} trading signals',
            'signals_generated': signals_generated,
            'signals': generated_signals
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trading_bp.route('/trading/signals/<int:signal_id>/execute', methods=['POST'])
def execute_trading_signal(signal_id):
    """Execute a trading signal"""
    try:
        signal = TradingSignal.query.get_or_404(signal_id)
        
        if signal.executed:
            return jsonify({'status': 'error', 'message': 'Signal already executed'}), 400
        
        # Simulate trade execution
        execution_result = simulate_trade_execution(signal)
        
        if execution_result['success']:
            signal.executed = True
            
            # Update token status if selling
            if signal.signal_type == 'sell':
                token = signal.token
                token.status = 'sold'
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Trading signal executed successfully',
                'execution_result': execution_result
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Trade execution failed',
                'error': execution_result['error']
            }), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trading_bp.route('/trading/auto-trade', methods=['POST'])
def auto_trade():
    """Automatically execute high-confidence trading signals"""
    try:
        # Get unexecuted signals with high confidence
        high_confidence_signals = TradingSignal.query.filter(
            TradingSignal.executed == False,
            TradingSignal.confidence >= 0.8
        ).all()
        
        executed_count = 0
        execution_results = []
        
        for signal in high_confidence_signals:
            execution_result = simulate_trade_execution(signal)
            
            if execution_result['success']:
                signal.executed = True
                
                # Update token status if selling
                if signal.signal_type == 'sell':
                    token = signal.token
                    token.status = 'sold'
                
                executed_count += 1
                execution_results.append({
                    'signal_id': signal.id,
                    'token_id': signal.token_id,
                    'signal_type': signal.signal_type,
                    'result': execution_result
                })
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Executed {executed_count} high-confidence trading signals',
            'executed_count': executed_count,
            'executions': execution_results
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@trading_bp.route('/trading/portfolio', methods=['GET'])
def get_portfolio():
    """Get current portfolio status"""
    try:
        # Get all tokens and their current status
        all_tokens = Token.query.all()
        
        portfolio = {
            'total_tokens': len(all_tokens),
            'active_tokens': 0,
            'sold_tokens': 0,
            'total_value_usd': 0,
            'total_profit_usd': 0,
            'tokens_by_status': {}
        }
        
        for token in all_tokens:
            status = token.status
            if status not in portfolio['tokens_by_status']:
                portfolio['tokens_by_status'][status] = 0
            portfolio['tokens_by_status'][status] += 1
            
            if status in ['deployed', 'marketing', 'trading']:
                portfolio['active_tokens'] += 1
                
                # Get latest performance data
                latest_performance = TokenPerformance.query.filter_by(token_id=token.id).order_by(TokenPerformance.recorded_at.desc()).first()
                if latest_performance:
                    portfolio['total_value_usd'] += latest_performance.market_cap_usd
            elif status == 'sold':
                portfolio['sold_tokens'] += 1
                # Simulate profit calculation
                portfolio['total_profit_usd'] += random.uniform(100, 10000)
        
        return jsonify(portfolio)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def simulate_current_token_metrics(token):
    """Simulate current token metrics based on age and trend"""
    age_hours = (datetime.utcnow() - token.created_at).total_seconds() / 3600
    trend = token.trend
    
    # Base price starts low and can grow based on virality and time
    base_price = 0.001
    
    # Price evolution based on trend virality and time
    if age_hours < 24:  # First 24 hours - high volatility
        price_multiplier = 1 + (trend.virality_score * random.uniform(0.5, 3.0))
    elif age_hours < 168:  # First week - moderate growth
        price_multiplier = 1 + (trend.virality_score * random.uniform(0.2, 1.5))
    else:  # After a week - stabilization or decline
        price_multiplier = 1 + (trend.virality_score * random.uniform(-0.3, 0.8))
    
    current_price = base_price * price_multiplier
    
    # Market cap based on circulating supply and price
    market_cap = current_price * token.initial_supply
    
    # Volume based on market cap and activity
    volume_24h = market_cap * random.uniform(0.01, 0.5)
    
    # Holders grow over time
    base_holders = 100
    holder_growth = age_hours * random.uniform(1, 10)
    holders_count = int(base_holders + holder_growth)
    
    # Price change (simulate daily volatility)
    price_change_24h = random.uniform(-30, 50)
    
    # Sentiment based on price performance and trend sentiment
    sentiment_score = (trend.sentiment_score + (price_change_24h / 100)) / 2
    sentiment_score = max(0, min(1, sentiment_score))  # Clamp between 0 and 1
    
    return {
        'current_price_usd': round(current_price, 8),
        'market_cap_usd': round(market_cap, 2),
        'volume_24h_usd': round(volume_24h, 2),
        'holders_count': holders_count,
        'price_change_24h': round(price_change_24h, 2),
        'sentiment_score': round(sentiment_score, 3)
    }

def analyze_token_and_generate_signal(token, performance_history):
    """Analyze token performance and generate trading signal"""
    if len(performance_history) < 3:
        return None
    
    # Get recent prices
    recent_prices = [p.price_usd for p in performance_history[:3]]
    recent_volumes = [p.volume_24h_usd for p in performance_history[:3]]
    recent_sentiment = [p.sentiment_score for p in performance_history[:3] if p.sentiment_score]
    
    # Calculate trends
    price_trend = (recent_prices[0] - recent_prices[-1]) / recent_prices[-1] if recent_prices[-1] > 0 else 0
    volume_trend = (recent_volumes[0] - recent_volumes[-1]) / recent_volumes[-1] if recent_volumes[-1] > 0 else 0
    
    avg_sentiment = sum(recent_sentiment) / len(recent_sentiment) if recent_sentiment else 0.5
    
    # Token age
    age_hours = (datetime.utcnow() - token.created_at).total_seconds() / 3600
    
    # Generate signal based on analysis
    if price_trend > 0.5 and volume_trend > 0.3 and avg_sentiment > 0.6:
        # Strong upward trend - hold or buy more
        return {
            'type': 'hold',
            'confidence': 0.8,
            'reason': f'Strong upward trend: price +{price_trend*100:.1f}%, volume +{volume_trend*100:.1f}%, positive sentiment',
            'target_price': recent_prices[0] * 1.5,
            'stop_loss': recent_prices[0] * 0.8
        }
    elif price_trend < -0.3 and age_hours > 168:  # Declining after a week
        # Downward trend after initial period - consider selling
        return {
            'type': 'sell',
            'confidence': 0.7,
            'reason': f'Declining trend after initial period: price {price_trend*100:.1f}%, age {age_hours:.1f}h',
            'target_price': recent_prices[0],
            'stop_loss': recent_prices[0] * 0.9
        }
    elif price_trend > 2.0 and age_hours < 48:  # Massive pump in first 48 hours
        # Take profits on massive early gains
        return {
            'type': 'sell',
            'confidence': 0.9,
            'reason': f'Massive early gains: price +{price_trend*100:.1f}% in {age_hours:.1f}h - taking profits',
            'target_price': recent_prices[0],
            'stop_loss': recent_prices[0] * 0.8
        }
    elif avg_sentiment < 0.3 and price_trend < -0.2:
        # Negative sentiment and declining price
        return {
            'type': 'sell',
            'confidence': 0.6,
            'reason': f'Negative sentiment ({avg_sentiment:.2f}) and declining price ({price_trend*100:.1f}%)',
            'target_price': recent_prices[0],
            'stop_loss': recent_prices[0] * 0.95
        }
    else:
        # Hold position
        return {
            'type': 'hold',
            'confidence': 0.5,
            'reason': 'Neutral conditions - maintaining position',
            'target_price': recent_prices[0] * 1.2,
            'stop_loss': recent_prices[0] * 0.9
        }

def simulate_trade_execution(signal):
    """Simulate executing a trade"""
    # Simulate execution success/failure
    if random.random() > 0.05:  # 95% success rate
        if signal.signal_type == 'sell':
            profit_usd = random.uniform(50, 5000)
            return {
                'success': True,
                'transaction_hash': f"0x{secrets.token_hex(32)}",
                'executed_price': signal.target_price,
                'profit_usd': profit_usd,
                'fees_usd': profit_usd * 0.003  # 0.3% fees
            }
        else:
            return {
                'success': True,
                'transaction_hash': f"0x{secrets.token_hex(32)}",
                'executed_price': signal.target_price,
                'amount_usd': random.uniform(100, 1000)
            }
    else:
        return {
            'success': False,
            'error': 'Insufficient liquidity'
        }

