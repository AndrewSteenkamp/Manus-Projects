#!/usr/bin/env python3
"""
Real-time WebSocket Streaming System for Socrates AI
Provides live market data updates and analysis results via WebSocket connections
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Set, Any, Optional
import threading
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
import schedule
import queue

# Import our existing components
from socrates_ai_architecture import SocratesAI
from data_collector import DataCollector
from enhanced_error_handling import ErrorHandler, RateLimiter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamType(Enum):
    """Types of data streams available"""
    MARKET_DATA = "market_data"
    ANALYSIS_RESULTS = "analysis_results"
    GLOBAL_ANALYSIS = "global_analysis"
    ECM_UPDATES = "ecm_updates"
    ALERTS = "alerts"
    SYSTEM_STATUS = "system_status"

@dataclass
class StreamMessage:
    """Structure for WebSocket stream messages"""
    stream_type: StreamType
    symbol: Optional[str]
    data: Dict[str, Any]
    timestamp: str
    message_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'stream_type': self.stream_type.value,
            'symbol': self.symbol,
            'data': self.data,
            'timestamp': self.timestamp,
            'message_id': self.message_id
        }

class WebSocketStreamer:
    """Real-time WebSocket streaming manager"""
    
    def __init__(self, app: Flask, db_path: str = "socrates_data.db"):
        self.app = app
        self.db_path = db_path
        self.socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
        
        # Initialize components
        self.socrates_ai = SocratesAI(db_path)
        self.data_collector = DataCollector(db_path)
        self.error_handler = ErrorHandler()
        
        # Streaming state
        self.active_streams: Dict[str, Set[str]] = {stream.value: set() for stream in StreamType}
        self.client_subscriptions: Dict[str, Set[StreamType]] = {}
        self.message_queue = queue.Queue()
        self.streaming_active = False
        
        # Rate limiting
        self.rate_limiter = RateLimiter(calls_per_minute=120)  # 2 per second max
        
        # Setup WebSocket event handlers
        self._setup_websocket_handlers()
        
        # Start background tasks
        self.background_thread = None
        self.scheduler_thread = None
    
    def _setup_websocket_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            client_id = self._get_client_id()
            logger.info(f"Client {client_id} connected")
            
            # Initialize client subscriptions
            self.client_subscriptions[client_id] = set()
            
            # Send welcome message
            emit('connected', {
                'message': 'Connected to Socrates AI streaming service',
                'client_id': client_id,
                'available_streams': [stream.value for stream in StreamType],
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            client_id = self._get_client_id()
            logger.info(f"Client {client_id} disconnected")
            
            # Clean up subscriptions
            if client_id in self.client_subscriptions:
                for stream_type in self.client_subscriptions[client_id]:
                    self.active_streams[stream_type.value].discard(client_id)
                del self.client_subscriptions[client_id]
        
        @self.socketio.on('subscribe')
        def handle_subscribe(data):
            client_id = self._get_client_id()
            stream_type = data.get('stream_type')
            symbol = data.get('symbol')
            
            try:
                stream_enum = StreamType(stream_type)
                
                # Add to subscriptions
                self.client_subscriptions[client_id].add(stream_enum)
                
                # Create room name
                room_name = f"{stream_type}_{symbol}" if symbol else stream_type
                join_room(room_name)
                
                logger.info(f"Client {client_id} subscribed to {stream_type} for {symbol or 'all'}")
                
                emit('subscription_confirmed', {
                    'stream_type': stream_type,
                    'symbol': symbol,
                    'status': 'subscribed',
                    'timestamp': datetime.now().isoformat()
                })
                
                # Send initial data if available
                self._send_initial_data(client_id, stream_enum, symbol)
                
            except ValueError:
                emit('error', {
                    'message': f'Invalid stream type: {stream_type}',
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.socketio.on('unsubscribe')
        def handle_unsubscribe(data):
            client_id = self._get_client_id()
            stream_type = data.get('stream_type')
            symbol = data.get('symbol')
            
            try:
                stream_enum = StreamType(stream_type)
                
                # Remove from subscriptions
                self.client_subscriptions[client_id].discard(stream_enum)
                
                # Leave room
                room_name = f"{stream_type}_{symbol}" if symbol else stream_type
                leave_room(room_name)
                
                logger.info(f"Client {client_id} unsubscribed from {stream_type} for {symbol or 'all'}")
                
                emit('subscription_cancelled', {
                    'stream_type': stream_type,
                    'symbol': symbol,
                    'status': 'unsubscribed',
                    'timestamp': datetime.now().isoformat()
                })
                
            except ValueError:
                emit('error', {
                    'message': f'Invalid stream type: {stream_type}',
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.socketio.on('request_analysis')
        def handle_analysis_request(data):
            """Handle real-time analysis requests"""
            client_id = self._get_client_id()
            symbol = data.get('symbol')
            analysis_type = data.get('analysis_type', 'market')
            
            if not symbol:
                emit('error', {'message': 'Symbol is required for analysis'})
                return
            
            try:
                # Perform analysis
                if analysis_type == 'market':
                    result = self.socrates_ai.analyze_market(symbol)
                elif analysis_type == 'cycles':
                    result = self.socrates_ai.analyzer.analyze_market_cycles(symbol)
                elif analysis_type == 'forecast':
                    result = self.socrates_ai.analyzer.generate_market_forecast(symbol, 30)
                else:
                    emit('error', {'message': f'Invalid analysis type: {analysis_type}'})
                    return
                
                # Send result
                emit('analysis_result', {
                    'symbol': symbol,
                    'analysis_type': analysis_type,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                })
                
                logger.info(f"Sent {analysis_type} analysis for {symbol} to client {client_id}")
                
            except Exception as e:
                error_info = self.error_handler.handle_error(e, f"Analysis request for {symbol}")
                emit('error', error_info)
    
    def _get_client_id(self) -> str:
        """Get unique client ID"""
        from flask import request
        return request.sid
    
    def _send_initial_data(self, client_id: str, stream_type: StreamType, symbol: Optional[str]):
        """Send initial data when client subscribes"""
        try:
            if stream_type == StreamType.MARKET_DATA and symbol:
                # Send latest market data
                data = self._get_latest_market_data(symbol)
                if data:
                    self._emit_to_client(client_id, stream_type, symbol, data)
            
            elif stream_type == StreamType.ANALYSIS_RESULTS and symbol:
                # Send latest analysis
                data = self._get_latest_analysis(symbol)
                if data:
                    self._emit_to_client(client_id, stream_type, symbol, data)
            
            elif stream_type == StreamType.GLOBAL_ANALYSIS:
                # Send global analysis
                data = self._get_global_analysis()
                if data:
                    self._emit_to_client(client_id, stream_type, None, data)
            
            elif stream_type == StreamType.SYSTEM_STATUS:
                # Send system status
                data = self._get_system_status()
                self._emit_to_client(client_id, stream_type, None, data)
                
        except Exception as e:
            logger.error(f"Error sending initial data: {e}")
    
    def _emit_to_client(self, client_id: str, stream_type: StreamType, symbol: Optional[str], data: Dict[str, Any]):
        """Emit data to specific client"""
        message = StreamMessage(
            stream_type=stream_type,
            symbol=symbol,
            data=data,
            timestamp=datetime.now().isoformat(),
            message_id=f"{stream_type.value}_{symbol or 'global'}_{int(time.time() * 1000)}"
        )
        
        room_name = f"{stream_type.value}_{symbol}" if symbol else stream_type.value
        self.socketio.emit('stream_data', message.to_dict(), room=room_name)
    
    def _get_latest_market_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest market data for symbol"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM market_data 
                WHERE symbol = ? 
                ORDER BY date DESC 
                LIMIT 1
            ''', (symbol,))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest market data for {symbol}: {e}")
            return None
    
    def _get_latest_analysis(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest analysis for symbol"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM analysis_results 
                WHERE symbol = ? 
                ORDER BY analysis_date DESC 
                LIMIT 1
            ''', (symbol,))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                result = dict(zip(columns, row))
                
                # Parse JSON results
                if result.get('results'):
                    result['results'] = json.loads(result['results'])
                
                return result
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest analysis for {symbol}: {e}")
            return None
    
    def _get_global_analysis(self) -> Dict[str, Any]:
        """Get global market analysis"""
        try:
            # Get list of active symbols
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD', 'EURUSD=X']
            result = self.socrates_ai.analyze_global_markets(symbols)
            return result
            
        except Exception as e:
            logger.error(f"Error getting global analysis: {e}")
            return {'error': str(e)}
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get data counts
            stats = {}
            tables = ['market_data', 'forex_data', 'commodities_data', 'economic_indicators']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()[0]
            
            # Get latest collection info
            cursor.execute('''
                SELECT collection_date, status, records_collected 
                FROM collection_log 
                ORDER BY collection_date DESC 
                LIMIT 5
            ''')
            
            recent_collections = []
            for row in cursor.fetchall():
                recent_collections.append({
                    'date': row[0],
                    'status': row[1],
                    'records': row[2]
                })
            
            conn.close()
            
            return {
                'status': 'operational',
                'data_stats': stats,
                'recent_collections': recent_collections,
                'active_connections': len(self.client_subscriptions),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def start_streaming(self):
        """Start the streaming service"""
        if self.streaming_active:
            return
        
        self.streaming_active = True
        
        # Start background data collection and analysis
        self.background_thread = threading.Thread(target=self._background_worker)
        self.background_thread.daemon = True
        self.background_thread.start()
        
        # Start scheduler for periodic tasks
        self.scheduler_thread = threading.Thread(target=self._scheduler_worker)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        logger.info("WebSocket streaming service started")
    
    def stop_streaming(self):
        """Stop the streaming service"""
        self.streaming_active = False
        logger.info("WebSocket streaming service stopped")
    
    def _background_worker(self):
        """Background worker for real-time updates"""
        while self.streaming_active:
            try:
                # Process any queued messages
                while not self.message_queue.empty():
                    try:
                        message = self.message_queue.get_nowait()
                        self._process_stream_message(message)
                    except queue.Empty:
                        break
                
                # Check for new market data updates
                self._check_market_data_updates()
                
                # Sleep to avoid overwhelming the system
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in background worker: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _scheduler_worker(self):
        """Scheduler worker for periodic tasks"""
        # Schedule periodic analysis updates
        schedule.every(15).minutes.do(self._periodic_analysis_update)
        schedule.every(1).hours.do(self._periodic_global_analysis)
        schedule.every(5).minutes.do(self._system_status_update)
        
        while self.streaming_active:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in scheduler worker: {e}")
                time.sleep(60)
    
    def _check_market_data_updates(self):
        """Check for new market data and stream updates"""
        try:
            # Get symbols that have active subscriptions
            subscribed_symbols = set()
            for client_id, streams in self.client_subscriptions.items():
                if StreamType.MARKET_DATA in streams:
                    # For now, check common symbols
                    subscribed_symbols.update(['AAPL', 'GOOGL', 'MSFT', 'SPY', 'GLD'])
            
            if not subscribed_symbols:
                return
            
            # Check for recent updates (last 10 minutes)
            cutoff_time = (datetime.now() - timedelta(minutes=10)).isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for symbol in subscribed_symbols:
                cursor.execute('''
                    SELECT * FROM market_data 
                    WHERE symbol = ? AND updated_at > ?
                    ORDER BY date DESC 
                    LIMIT 1
                ''', (symbol, cutoff_time))
                
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    data = dict(zip(columns, row))
                    
                    # Stream the update
                    self._emit_to_client(None, StreamType.MARKET_DATA, symbol, data)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking market data updates: {e}")
    
    def _periodic_analysis_update(self):
        """Periodic analysis update for subscribed symbols"""
        try:
            # Get symbols with analysis subscriptions
            subscribed_symbols = set()
            for client_id, streams in self.client_subscriptions.items():
                if StreamType.ANALYSIS_RESULTS in streams:
                    subscribed_symbols.update(['AAPL', 'GOOGL', 'MSFT', 'SPY'])
            
            for symbol in subscribed_symbols:
                try:
                    # Perform analysis
                    result = self.socrates_ai.analyze_market(symbol)
                    
                    # Stream the result
                    self._emit_to_client(None, StreamType.ANALYSIS_RESULTS, symbol, result)
                    
                    # Rate limiting
                    self.rate_limiter.wait_if_needed()
                    
                except Exception as e:
                    logger.error(f"Error in periodic analysis for {symbol}: {e}")
            
        except Exception as e:
            logger.error(f"Error in periodic analysis update: {e}")
    
    def _periodic_global_analysis(self):
        """Periodic global analysis update"""
        try:
            if any(StreamType.GLOBAL_ANALYSIS in streams for streams in self.client_subscriptions.values()):
                result = self._get_global_analysis()
                self._emit_to_client(None, StreamType.GLOBAL_ANALYSIS, None, result)
                
        except Exception as e:
            logger.error(f"Error in periodic global analysis: {e}")
    
    def _system_status_update(self):
        """Periodic system status update"""
        try:
            if any(StreamType.SYSTEM_STATUS in streams for streams in self.client_subscriptions.values()):
                status = self._get_system_status()
                self._emit_to_client(None, StreamType.SYSTEM_STATUS, None, status)
                
        except Exception as e:
            logger.error(f"Error in system status update: {e}")
    
    def _process_stream_message(self, message: StreamMessage):
        """Process a stream message"""
        try:
            room_name = f"{message.stream_type.value}_{message.symbol}" if message.symbol else message.stream_type.value
            self.socketio.emit('stream_data', message.to_dict(), room=room_name)
            
        except Exception as e:
            logger.error(f"Error processing stream message: {e}")
    
    def queue_message(self, stream_type: StreamType, symbol: Optional[str], data: Dict[str, Any]):
        """Queue a message for streaming"""
        message = StreamMessage(
            stream_type=stream_type,
            symbol=symbol,
            data=data,
            timestamp=datetime.now().isoformat(),
            message_id=f"{stream_type.value}_{symbol or 'global'}_{int(time.time() * 1000)}"
        )
        
        self.message_queue.put(message)
    
    def get_streaming_stats(self) -> Dict[str, Any]:
        """Get streaming statistics"""
        return {
            'active_connections': len(self.client_subscriptions),
            'active_streams': {stream: len(clients) for stream, clients in self.active_streams.items()},
            'queue_size': self.message_queue.qsize(),
            'streaming_active': self.streaming_active
        }

def create_websocket_app(db_path: str = "socrates_data.db") -> tuple[Flask, WebSocketStreamer]:
    """Create Flask app with WebSocket streaming"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'socrates_ai_websocket_secret'
    
    # Create streamer
    streamer = WebSocketStreamer(app, db_path)
    
    # Add HTTP endpoints for WebSocket management
    @app.route('/api/streaming/status')
    def streaming_status():
        return streamer.get_streaming_stats()
    
    @app.route('/api/streaming/start', methods=['POST'])
    def start_streaming():
        streamer.start_streaming()
        return {'status': 'started', 'timestamp': datetime.now().isoformat()}
    
    @app.route('/api/streaming/stop', methods=['POST'])
    def stop_streaming():
        streamer.stop_streaming()
        return {'status': 'stopped', 'timestamp': datetime.now().isoformat()}
    
    return app, streamer

def main():
    """Test the WebSocket streaming system"""
    print("Socrates AI WebSocket Streaming System")
    print("=" * 50)
    
    # Create app and streamer
    app, streamer = create_websocket_app()
    
    # Start streaming
    streamer.start_streaming()
    
    print("WebSocket server starting on http://localhost:5001")
    print("Available streams:")
    for stream in StreamType:
        print(f"  - {stream.value}")
    
    print("\nTest with a WebSocket client:")
    print("1. Connect to ws://localhost:5001")
    print("2. Send: {'stream_type': 'market_data', 'symbol': 'AAPL'}")
    print("3. Receive real-time updates")
    
    # Run the server
    try:
        streamer.socketio.run(app, host='0.0.0.0', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down WebSocket server...")
        streamer.stop_streaming()

if __name__ == "__main__":
    main()

