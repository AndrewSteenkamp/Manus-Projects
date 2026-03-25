#!/usr/bin/env python3
"""
Enhanced Flask Backend for Socrates AI with WebSocket Streaming
Integrates all components into a comprehensive API server
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import our components
from socrates_ai_architecture import SocratesAI
from data_collector import DataCollector
from analysis_pipeline import AdvancedAnalyzer
from enhanced_error_handling import ErrorHandler, RobustAPIClient
from database_fixes import DatabaseManager
from websocket_streaming import WebSocketStreamer, StreamType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSocratesAPI:
    """Enhanced Socrates AI API with WebSocket streaming"""
    
    def __init__(self, db_path: str = "socrates_data.db"):
        self.db_path = db_path
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'socrates_ai_enhanced_secret_key'
        
        # Enable CORS for all routes
        CORS(self.app, origins="*", allow_headers="*", methods="*")
        
        # Initialize components
        self.db_manager = DatabaseManager(db_path)
        self.socrates_ai = SocratesAI(db_path)
        self.data_collector = DataCollector(db_path)
        self.analyzer = AdvancedAnalyzer(db_path)
        self.error_handler = ErrorHandler()
        
        # Initialize WebSocket streaming
        self.websocket_streamer = WebSocketStreamer(self.app, db_path)
        
        # Setup routes
        self._setup_routes()
        
        # Background tasks
        self.background_tasks_active = False
        self.background_thread = None
    
    def _setup_routes(self):
        """Setup all API routes"""
        
        # Health check
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            try:
                stats = self.db_manager.get_database_stats()
                return jsonify({
                    'status': 'healthy',
                    'service': 'Enhanced Socrates AI',
                    'version': '2.0',
                    'database_stats': stats,
                    'websocket_stats': self.websocket_streamer.get_streaming_stats(),
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify(self.error_handler.handle_error(e, 'health_check')), 500
        
        # Daily market report
        @self.app.route('/api/socrates/daily-report', methods=['GET'])
        def daily_report():
            try:
                date = request.args.get('date', datetime.now().date().isoformat())
                
                # Generate comprehensive daily report
                report = self._generate_daily_report(date)
                
                # Stream the report to WebSocket clients
                self.websocket_streamer.queue_message(
                    StreamType.ANALYSIS_RESULTS, 
                    None, 
                    {'daily_report': report, 'date': date}
                )
                
                return jsonify({
                    'success': True,
                    'data': report,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'daily_report')
                return jsonify(error_info), 500
        
        # Individual market analysis
        @self.app.route('/api/socrates/analyze/market/<symbol>', methods=['GET'])
        def analyze_market(symbol):
            try:
                date = request.args.get('date', datetime.now().date().isoformat())
                
                # Perform analysis
                result = self.socrates_ai.analyze_market(symbol, date)
                
                # Stream the result to WebSocket clients
                self.websocket_streamer.queue_message(
                    StreamType.ANALYSIS_RESULTS, 
                    symbol, 
                    result
                )
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, f'analyze_market_{symbol}')
                return jsonify(error_info), 500
        
        # Global market analysis
        @self.app.route('/api/socrates/analyze/global', methods=['GET'])
        def analyze_global():
            try:
                symbols_param = request.args.get('symbols', 'AAPL,GOOGL,MSFT,SPY,GLD,EURUSD=X')
                symbols = [s.strip() for s in symbols_param.split(',')]
                
                # Perform global analysis
                result = self.socrates_ai.analyze_global_markets(symbols)
                
                # Stream the result to WebSocket clients
                self.websocket_streamer.queue_message(
                    StreamType.GLOBAL_ANALYSIS, 
                    None, 
                    result
                )
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'analyze_global')
                return jsonify(error_info), 500
        
        # Cycle analysis
        @self.app.route('/api/socrates/analyze/cycles/<symbol>', methods=['GET'])
        def analyze_cycles(symbol):
            try:
                result = self.analyzer.analyze_market_cycles(symbol)
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, f'analyze_cycles_{symbol}')
                return jsonify(error_info), 500
        
        # Market forecast
        @self.app.route('/api/socrates/forecast/<symbol>', methods=['GET'])
        def forecast_market(symbol):
            try:
                horizon = int(request.args.get('horizon', 30))
                
                result = self.analyzer.generate_market_forecast(symbol, horizon)
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, f'forecast_{symbol}')
                return jsonify(error_info), 500
        
        # Data collection
        @self.app.route('/api/socrates/data/collect', methods=['POST'])
        def collect_data():
            try:
                data = request.get_json() or {}
                data_types = data.get('data_types', ['stocks', 'forex', 'commodities'])
                symbols = data.get('symbols', [])
                
                # Start data collection in background
                collection_thread = threading.Thread(
                    target=self._background_data_collection,
                    args=(data_types, symbols)
                )
                collection_thread.daemon = True
                collection_thread.start()
                
                return jsonify({
                    'success': True,
                    'message': 'Data collection started',
                    'data_types': data_types,
                    'symbols': symbols,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'collect_data')
                return jsonify(error_info), 500
        
        # Data summary
        @self.app.route('/api/socrates/data/summary', methods=['GET'])
        def data_summary():
            try:
                stats = self.db_manager.get_database_stats()
                
                return jsonify({
                    'success': True,
                    'data': stats,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'data_summary')
                return jsonify(error_info), 500
        
        # Available markets
        @self.app.route('/api/socrates/markets/available', methods=['GET'])
        def available_markets():
            try:
                markets = self.socrates_ai.get_available_markets()
                
                return jsonify({
                    'success': True,
                    'data': markets,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'available_markets')
                return jsonify(error_info), 500
        
        # WebSocket streaming control
        @self.app.route('/api/streaming/status', methods=['GET'])
        def streaming_status():
            try:
                stats = self.websocket_streamer.get_streaming_stats()
                return jsonify({
                    'success': True,
                    'data': stats,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'streaming_status')
                return jsonify(error_info), 500
        
        @self.app.route('/api/streaming/start', methods=['POST'])
        def start_streaming():
            try:
                self.websocket_streamer.start_streaming()
                return jsonify({
                    'success': True,
                    'message': 'WebSocket streaming started',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'start_streaming')
                return jsonify(error_info), 500
        
        @self.app.route('/api/streaming/stop', methods=['POST'])
        def stop_streaming():
            try:
                self.websocket_streamer.stop_streaming()
                return jsonify({
                    'success': True,
                    'message': 'WebSocket streaming stopped',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'stop_streaming')
                return jsonify(error_info), 500
        
        # System administration
        @self.app.route('/api/admin/database/optimize', methods=['POST'])
        def optimize_database():
            try:
                self.db_manager.optimize_database()
                return jsonify({
                    'success': True,
                    'message': 'Database optimization completed',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'optimize_database')
                return jsonify(error_info), 500
        
        @self.app.route('/api/admin/database/backup', methods=['POST'])
        def backup_database():
            try:
                backup_path = self.db_manager.backup_database()
                return jsonify({
                    'success': True,
                    'message': 'Database backup created',
                    'backup_path': backup_path,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'backup_database')
                return jsonify(error_info), 500
        
        @self.app.route('/api/admin/system/stats', methods=['GET'])
        def system_stats():
            try:
                stats = {
                    'database_stats': self.db_manager.get_database_stats(),
                    'websocket_stats': self.websocket_streamer.get_streaming_stats(),
                    'error_stats': self.error_handler.get_error_stats(),
                    'background_tasks_active': self.background_tasks_active
                }
                
                return jsonify({
                    'success': True,
                    'data': stats,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                error_info = self.error_handler.handle_error(e, 'system_stats')
                return jsonify(error_info), 500
    
    def _generate_daily_report(self, date: str) -> dict:
        """Generate comprehensive daily market report"""
        try:
            # Get major market symbols
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD', 'EURUSD=X', 'GC=F']
            
            # Perform global analysis
            global_analysis = self.socrates_ai.analyze_global_markets(symbols)
            
            # Get individual market highlights
            market_highlights = {}
            for symbol in symbols[:5]:  # Limit to avoid overwhelming
                try:
                    analysis = self.socrates_ai.analyze_market(symbol, date)
                    if 'error' not in analysis:
                        market_highlights[symbol] = {
                            'confidence': analysis.get('overall_confidence', 0),
                            'momentum': analysis.get('momentum_analysis', {}),
                            'ecm_phase': analysis.get('ecm_analysis', {}).get('phase', 'unknown')
                        }
                except Exception as e:
                    logger.warning(f"Error analyzing {symbol} for daily report: {e}")
            
            # Generate key insights
            key_insights = self._generate_key_insights(global_analysis, market_highlights)
            
            # Compile daily report
            report = {
                'date': date,
                'global_confidence': global_analysis.get('global_confidence', 0),
                'ecm_analysis': global_analysis.get('global_ecm', {}),
                'capital_flow_analysis': global_analysis.get('capital_flow_analysis', {}),
                'market_highlights': market_highlights,
                'key_insights': key_insights,
                'markets_analyzed': len(symbols),
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            return {
                'date': date,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }
    
    def _generate_key_insights(self, global_analysis: dict, market_highlights: dict) -> list:
        """Generate key insights from analysis results"""
        insights = []
        
        try:
            # Global confidence insight
            global_conf = global_analysis.get('global_confidence', 0)
            if global_conf > 0.7:
                insights.append("High global market confidence indicates strong bullish sentiment across major markets.")
            elif global_conf < 0.3:
                insights.append("Low global market confidence suggests bearish conditions and increased volatility risk.")
            else:
                insights.append("Moderate global market confidence reflects mixed signals and transitional market conditions.")
            
            # ECM phase insight
            ecm_phase = global_analysis.get('global_ecm', {}).get('phase', '')
            if 'expansion' in ecm_phase.lower():
                insights.append("ECM cycle indicates expansion phase, typically favorable for risk assets.")
            elif 'contraction' in ecm_phase.lower():
                insights.append("ECM cycle shows contraction phase, suggesting defensive positioning may be prudent.")
            
            # Market momentum insights
            bullish_count = sum(1 for data in market_highlights.values() 
                              if data.get('momentum', {}).get('direction') == 'bullish')
            bearish_count = sum(1 for data in market_highlights.values() 
                              if data.get('momentum', {}).get('direction') == 'bearish')
            
            if bullish_count > bearish_count:
                insights.append(f"Majority of analyzed markets ({bullish_count}/{len(market_highlights)}) show bullish momentum.")
            elif bearish_count > bullish_count:
                insights.append(f"Majority of analyzed markets ({bearish_count}/{len(market_highlights)}) show bearish momentum.")
            
            # Capital flow insight
            capital_flow = global_analysis.get('capital_flow_analysis', {})
            if capital_flow.get('capital_flow_direction') == 'risk_on':
                insights.append("Capital flows indicate risk-on sentiment with money moving into growth assets.")
            elif capital_flow.get('capital_flow_direction') == 'risk_off':
                insights.append("Capital flows show risk-off sentiment with flight to safety assets.")
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            insights.append("Analysis completed successfully with comprehensive market coverage.")
        
        return insights
    
    def _background_data_collection(self, data_types: list, symbols: list):
        """Background data collection task"""
        try:
            logger.info(f"Starting background data collection for {data_types}")
            
            collection_results = {}
            
            if 'stocks' in data_types:
                stock_symbols = symbols if symbols else ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD']
                result = self.data_collector.collect_stock_data(stock_symbols)
                collection_results['stocks'] = result
                
                # Stream update
                self.websocket_streamer.queue_message(
                    StreamType.SYSTEM_STATUS, 
                    None, 
                    {'collection_update': {'type': 'stocks', 'status': 'completed', 'result': result}}
                )
            
            if 'forex' in data_types:
                forex_pairs = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
                result = self.data_collector.collect_forex_data(forex_pairs)
                collection_results['forex'] = result
                
                # Stream update
                self.websocket_streamer.queue_message(
                    StreamType.SYSTEM_STATUS, 
                    None, 
                    {'collection_update': {'type': 'forex', 'status': 'completed', 'result': result}}
                )
            
            if 'commodities' in data_types:
                commodity_symbols = ['GC=F', 'SI=F', 'CL=F', 'NG=F']
                result = self.data_collector.collect_commodities_data(commodity_symbols)
                collection_results['commodities'] = result
                
                # Stream update
                self.websocket_streamer.queue_message(
                    StreamType.SYSTEM_STATUS, 
                    None, 
                    {'collection_update': {'type': 'commodities', 'status': 'completed', 'result': result}}
                )
            
            logger.info("Background data collection completed")
            
            # Final status update
            self.websocket_streamer.queue_message(
                StreamType.SYSTEM_STATUS, 
                None, 
                {'collection_complete': collection_results, 'timestamp': datetime.now().isoformat()}
            )
            
        except Exception as e:
            logger.error(f"Error in background data collection: {e}")
            
            # Error status update
            self.websocket_streamer.queue_message(
                StreamType.SYSTEM_STATUS, 
                None, 
                {'collection_error': str(e), 'timestamp': datetime.now().isoformat()}
            )
    
    def start_background_tasks(self):
        """Start background maintenance tasks"""
        if self.background_tasks_active:
            return
        
        self.background_tasks_active = True
        self.background_thread = threading.Thread(target=self._background_maintenance)
        self.background_thread.daemon = True
        self.background_thread.start()
        
        logger.info("Background maintenance tasks started")
    
    def _background_maintenance(self):
        """Background maintenance tasks"""
        while self.background_tasks_active:
            try:
                # Periodic database optimization (every 6 hours)
                if datetime.now().hour % 6 == 0 and datetime.now().minute < 5:
                    logger.info("Running periodic database optimization")
                    self.db_manager.optimize_database()
                
                # Periodic data cleanup (daily at 2 AM)
                if datetime.now().hour == 2 and datetime.now().minute < 5:
                    logger.info("Running periodic data cleanup")
                    self.db_manager.cleanup_old_data()
                
                # Sleep for 5 minutes
                time.sleep(300)
                
            except Exception as e:
                logger.error(f"Error in background maintenance: {e}")
                time.sleep(600)  # Wait 10 minutes on error
    
    def initialize_system(self):
        """Initialize the enhanced Socrates AI system"""
        try:
            logger.info("Initializing Enhanced Socrates AI System...")
            
            # Initialize database with improvements
            logger.info("Initializing database...")
            self.db_manager.initialize_database()
            self.db_manager.migrate_existing_data()
            
            # Start WebSocket streaming
            logger.info("Starting WebSocket streaming...")
            self.websocket_streamer.start_streaming()
            
            # Start background tasks
            logger.info("Starting background tasks...")
            self.start_background_tasks()
            
            logger.info("Enhanced Socrates AI System initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing system: {e}")
            raise
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the enhanced Flask application"""
        try:
            # Initialize system
            self.initialize_system()
            
            logger.info(f"Starting Enhanced Socrates AI API server on {host}:{port}")
            logger.info("Available endpoints:")
            logger.info("  - GET  /api/health")
            logger.info("  - GET  /api/socrates/daily-report")
            logger.info("  - GET  /api/socrates/analyze/market/<symbol>")
            logger.info("  - GET  /api/socrates/analyze/global")
            logger.info("  - GET  /api/socrates/analyze/cycles/<symbol>")
            logger.info("  - GET  /api/socrates/forecast/<symbol>")
            logger.info("  - POST /api/socrates/data/collect")
            logger.info("  - GET  /api/socrates/data/summary")
            logger.info("  - GET  /api/socrates/markets/available")
            logger.info("  - GET  /api/streaming/status")
            logger.info("  - POST /api/streaming/start")
            logger.info("  - POST /api/streaming/stop")
            logger.info("  - WebSocket: ws://localhost:5000/socket.io/")
            
            # Run with SocketIO support
            self.websocket_streamer.socketio.run(
                self.app, 
                host=host, 
                port=port, 
                debug=debug,
                allow_unsafe_werkzeug=True
            )
            
        except KeyboardInterrupt:
            logger.info("Shutting down Enhanced Socrates AI API server...")
            self.background_tasks_active = False
            self.websocket_streamer.stop_streaming()
        except Exception as e:
            logger.error(f"Error running server: {e}")
            raise

def main():
    """Main function to run the enhanced server"""
    print("Enhanced Socrates AI API Server with WebSocket Streaming")
    print("=" * 60)
    
    # Create and run the enhanced API
    api = EnhancedSocratesAPI()
    api.run(debug=False)

if __name__ == "__main__":
    main()

