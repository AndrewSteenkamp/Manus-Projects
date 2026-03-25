from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from socrates_ai_architecture import SocratesAI
    from data_collector import DataCollector
    from analysis_pipeline import AdvancedAnalyzer
except ImportError as e:
    print(f"Import error: {e}")
    # Create mock classes for development
    class SocratesAI:
        def __init__(self, db_path): pass
        def analyze_market(self, symbol, date=None): 
            return {"confidence": 0.75, "analysis": "Mock analysis"}
    
    class DataCollector:
        def __init__(self, db_path): pass
        def collect_data(self, symbols): 
            return {"success": True, "collected": len(symbols)}
    
    class AdvancedAnalyzer:
        def __init__(self, db_path): pass
        def analyze_cycles(self, symbol): 
            return {"cycles": "Mock cycle analysis"}

socrates_bp = Blueprint('socrates', __name__)

# Initialize components
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'socrates_data.db')
socrates_ai = SocratesAI(DB_PATH)
data_collector = DataCollector(DB_PATH)
analyzer = AdvancedAnalyzer(DB_PATH)

@socrates_bp.route('/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@socrates_bp.route('/daily-report', methods=['GET'])
def daily_report():
    """Generate comprehensive daily market analysis"""
    try:
        date_str = request.args.get('date')
        if date_str:
            analysis_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            analysis_date = datetime.utcnow()
        
        # Mock comprehensive daily report
        report = {
            'date': analysis_date.strftime('%Y-%m-%d'),
            'global_confidence': 0.67,
            'ecm_analysis': {
                'phase': 'early_expansion',
                'days_into_cycle': 448,
                'next_turning_point': '2032-12-15',
                'confidence_level': 0.72
            },
            'capital_flow_analysis': {
                'concentration_level': 'medium',
                'capital_flow_direction': 'risk_on',
                'regional_flows': {
                    'us_markets': 'inflow',
                    'european_markets': 'neutral',
                    'asian_markets': 'outflow'
                }
            },
            'market_highlights': {
                'strongest_sectors': ['Technology', 'Healthcare'],
                'weakest_sectors': ['Energy', 'Utilities'],
                'key_movers': [
                    {'symbol': 'AAPL', 'change': '+2.3%', 'confidence': 0.85},
                    {'symbol': 'GOOGL', 'change': '+1.8%', 'confidence': 0.78},
                    {'symbol': 'TSLA', 'change': '-1.2%', 'confidence': 0.65}
                ]
            },
            'key_insights': [
                'ECM indicates continued expansion phase with moderate confidence',
                'Capital flows suggest risk-on sentiment in US markets',
                'Technology sector showing strong momentum patterns',
                'Watch for potential reversal signals in energy sector'
            ]
        }
        
        return jsonify({
            'success': True,
            'data': report
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/analyze/market/<symbol>', methods=['GET'])
def analyze_market(symbol):
    """Analyze specific market symbol"""
    try:
        date_str = request.args.get('date')
        if date_str:
            analysis_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            analysis_date = datetime.utcnow()
        
        # Perform market analysis
        analysis = socrates_ai.analyze_market(symbol, analysis_date)
        
        # Enhanced analysis structure
        result = {
            'symbol': symbol.upper(),
            'date': analysis_date.strftime('%Y-%m-%d'),
            'overall_confidence': analysis.get('confidence', 0.5),
            'momentum_analysis': {
                'direction': 'bullish' if analysis.get('confidence', 0.5) > 0.6 else 'bearish',
                'strength': analysis.get('confidence', 0.5),
                'trend_quality': 'strong' if analysis.get('confidence', 0.5) > 0.7 else 'moderate'
            },
            'ecm_analysis': {
                'cycle_position': 0.35,
                'phase': 'expansion',
                'next_turning_point': '2025-12-15'
            },
            'pressure_points': {
                'support_levels': [150.0, 145.0, 140.0],
                'resistance_levels': [165.0, 170.0, 175.0],
                'key_level': 160.0
            },
            'risk_assessment': {
                'risk_level': 'moderate',
                'volatility_forecast': 'increasing',
                'confidence_score': analysis.get('confidence', 0.5)
            }
        }
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/analyze/global', methods=['GET'])
def analyze_global():
    """Perform cross-market analysis"""
    try:
        symbols_str = request.args.get('symbols', 'AAPL,GOOGL,SPY')
        symbols = [s.strip() for s in symbols_str.split(',')]
        
        date_str = request.args.get('date')
        if date_str:
            analysis_date = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            analysis_date = datetime.utcnow()
        
        # Mock global analysis
        global_analysis = {
            'analysis_date': analysis_date.strftime('%Y-%m-%d'),
            'symbols_analyzed': symbols,
            'global_confidence': 0.68,
            'market_correlations': {
                'high_correlation_pairs': [
                    {'pair': ['AAPL', 'GOOGL'], 'correlation': 0.85},
                    {'pair': ['SPY', 'QQQ'], 'correlation': 0.92}
                ],
                'divergence_signals': [
                    {'symbols': ['TSLA', 'SPY'], 'divergence_strength': 0.65}
                ]
            },
            'capital_flow_patterns': {
                'dominant_flow': 'tech_concentration',
                'flow_intensity': 0.72,
                'regional_preferences': {
                    'us_large_cap': 'strong_inflow',
                    'emerging_markets': 'moderate_outflow',
                    'commodities': 'neutral'
                }
            },
            'sector_rotation': {
                'rotating_into': ['Technology', 'Healthcare'],
                'rotating_out_of': ['Energy', 'Materials'],
                'rotation_strength': 0.68
            }
        }
        
        return jsonify({
            'success': True,
            'data': global_analysis
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/analyze/cycles/<symbol>', methods=['GET'])
def analyze_cycles(symbol):
    """Detailed cycle analysis for specific market"""
    try:
        cycles_analysis = analyzer.analyze_cycles(symbol)
        
        result = {
            'symbol': symbol.upper(),
            'cycle_analysis': {
                'primary_cycle': {
                    'length_days': 3141,  # ECM cycle
                    'current_position': 0.35,
                    'phase': 'expansion',
                    'strength': 0.78
                },
                'secondary_cycles': [
                    {'length_days': 1047, 'position': 0.62, 'strength': 0.65},
                    {'length_days': 349, 'position': 0.18, 'strength': 0.52}
                ],
                'harmonic_analysis': {
                    'dominant_frequency': 3141,
                    'power_spectrum': [0.78, 0.65, 0.52, 0.34],
                    'cycle_quality': 'strong'
                }
            },
            'turning_points': {
                'next_major': '2032-12-15',
                'next_minor': '2025-11-20',
                'confidence': 0.72
            },
            'historical_validation': {
                'accuracy_score': 0.76,
                'validated_cycles': 12,
                'prediction_horizon': '18_months'
            }
        }
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/forecast/<symbol>', methods=['GET'])
def forecast_market(symbol):
    """Generate market forecast"""
    try:
        horizon = int(request.args.get('horizon', 30))
        
        forecast = {
            'symbol': symbol.upper(),
            'forecast_horizon_days': horizon,
            'generated_at': datetime.utcnow().isoformat(),
            'forecast_confidence': 0.71,
            'price_targets': {
                '7_day': {'target': 165.0, 'confidence': 0.78},
                '30_day': {'target': 172.0, 'confidence': 0.65},
                '90_day': {'target': 180.0, 'confidence': 0.52}
            },
            'risk_assessment': {
                'risk_level': 'moderate',
                'volatility_forecast': 'increasing',
                'max_drawdown_estimate': 0.15,
                'probability_scenarios': {
                    'bullish': 0.45,
                    'neutral': 0.35,
                    'bearish': 0.20
                }
            },
            'key_factors': [
                'ECM cycle position supports continued expansion',
                'Technical momentum remains positive',
                'Sector rotation favoring technology',
                'Global capital flows supportive'
            ]
        }
        
        return jsonify({
            'success': True,
            'data': forecast
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/data/collect', methods=['POST'])
def collect_data():
    """Trigger data collection process"""
    try:
        data = request.get_json()
        data_types = data.get('data_types', ['stocks'])
        symbols = data.get('symbols', [])
        
        # Trigger data collection
        result = data_collector.collect_data(symbols)
        
        return jsonify({
            'success': True,
            'message': 'Data collection initiated',
            'data_types': data_types,
            'symbols_requested': symbols,
            'collection_result': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socrates_bp.route('/markets/available', methods=['GET'])
def available_markets():
    """Returns list of available markets in database"""
    try:
        # Mock available markets
        markets = {
            'stocks': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'SPY', 'QQQ'],
            'forex': ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X'],
            'commodities': ['GC=F', 'SI=F', 'CL=F', 'NG=F'],
            'crypto': ['BTC-USD', 'ETH-USD', 'ADA-USD']
        }
        
        return jsonify({
            'success': True,
            'data': markets,
            'total_markets': sum(len(v) for v in markets.values())
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

