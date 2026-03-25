#!/usr/bin/env python3
"""
Final System Test Suite for Enhanced Socrates AI
Comprehensive end-to-end testing of all system components
"""

import sys
import os
import time
import json
import sqlite3
import requests
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocratesAISystemTester:
    """Comprehensive system tester for Socrates AI"""
    
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'summary': {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'success_rate': 0.0
            }
        }
        self.flask_process = None
        
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and record results"""
        try:
            logger.info(f"Running test: {test_name}")
            start_time = time.time()
            
            result = test_func()
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.test_results['tests'][test_name] = {
                'status': 'PASSED' if result else 'FAILED',
                'duration': duration,
                'timestamp': datetime.now().isoformat(),
                'details': result if isinstance(result, dict) else {'success': result}
            }
            
            self.test_results['summary']['total_tests'] += 1
            if result:
                self.test_results['summary']['passed_tests'] += 1
                logger.info(f"✓ {test_name} PASSED ({duration:.3f}s)")
            else:
                self.test_results['summary']['failed_tests'] += 1
                logger.error(f"✗ {test_name} FAILED ({duration:.3f}s)")
            
            return bool(result)
            
        except Exception as e:
            logger.error(f"✗ {test_name} ERROR: {e}")
            self.test_results['tests'][test_name] = {
                'status': 'ERROR',
                'duration': 0,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            self.test_results['summary']['total_tests'] += 1
            self.test_results['summary']['failed_tests'] += 1
            return False
    
    def test_database_integrity(self) -> bool:
        """Test database integrity and schema"""
        try:
            conn = sqlite3.connect('socrates_data.db')
            cursor = conn.cursor()
            
            # Check all required tables exist
            required_tables = [
                'market_data', 'analysis_results', 'ecm_analysis', 
                'global_analysis', 'validation_results', 'data_quality_metrics',
                'tradingview_cache', 'alert_conditions', 'alert_history',
                'portfolios', 'portfolio_positions', 'alternative_data'
            ]
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                logger.error(f"Missing tables: {missing_tables}")
                conn.close()
                return False
            
            # Check data integrity
            data_counts = {}
            for table in required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                data_counts[table] = count
            
            conn.close()
            
            # Verify we have sufficient data
            if data_counts.get('market_data', 0) < 100:
                logger.error("Insufficient market data")
                return False
            
            logger.info(f"Database integrity check passed. Data counts: {data_counts}")
            return True
            
        except Exception as e:
            logger.error(f"Database integrity test failed: {e}")
            return False
    
    def test_core_api_endpoints(self) -> bool:
        """Test all core API endpoints"""
        try:
            endpoints = [
                '/api/socrates/health',
                '/api/socrates/analysis/AAPL',
                '/api/socrates/daily-report',
                '/api/socrates/global-analysis',
                '/api/socrates/ecm-analysis/AAPL',
                '/api/socrates/validation/AAPL',
                '/api/socrates/performance',
                '/api/socrates/portfolio/summary',
                '/api/socrates/alerts/active'
            ]
            
            results = {}
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                    results[endpoint] = {
                        'status_code': response.status_code,
                        'response_time': response.elapsed.total_seconds(),
                        'success': response.status_code == 200
                    }
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            results[endpoint]['has_data'] = bool(data)
                        except:
                            results[endpoint]['has_data'] = False
                    
                except requests.RequestException as e:
                    results[endpoint] = {
                        'status_code': 0,
                        'error': str(e),
                        'success': False
                    }
            
            # Check results
            failed_endpoints = [ep for ep, result in results.items() if not result['success']]
            
            if failed_endpoints:
                logger.error(f"Failed endpoints: {failed_endpoints}")
                return False
            
            avg_response_time = sum(r.get('response_time', 0) for r in results.values()) / len(results)
            logger.info(f"All API endpoints passed. Average response time: {avg_response_time:.3f}s")
            
            return True
            
        except Exception as e:
            logger.error(f"API endpoints test failed: {e}")
            return False
    
    def test_tradingview_validation(self) -> bool:
        """Test TradingView validation system"""
        try:
            # Import and test TradingView validator
            sys.path.append('/home/ubuntu')
            from tradingview_validation import TradingViewValidator
            
            validator = TradingViewValidator()
            
            # Test data fetching
            tv_data = validator.fetch_tradingview_data("AAPL")
            if not tv_data:
                logger.error("Failed to fetch TradingView data")
                return False
            
            # Test price validation
            price_validations = validator.validate_price_data("AAPL")
            if not price_validations:
                logger.error("Failed to validate price data")
                return False
            
            # Test comprehensive validation
            comprehensive = validator.validate_symbol_comprehensive("AAPL")
            if 'error' in comprehensive:
                logger.error(f"Comprehensive validation failed: {comprehensive['error']}")
                return False
            
            # Check accuracy rate
            summary = comprehensive.get('summary', {})
            accuracy_rate = summary.get('accuracy_rate', 0)
            
            if accuracy_rate < 80:  # Require at least 80% accuracy
                logger.error(f"TradingView validation accuracy too low: {accuracy_rate}%")
                return False
            
            logger.info(f"TradingView validation passed. Accuracy: {accuracy_rate:.1f}%")
            return True
            
        except Exception as e:
            logger.error(f"TradingView validation test failed: {e}")
            return False
    
    def test_machine_learning_models(self) -> bool:
        """Test machine learning prediction models"""
        try:
            # Import and test ML models
            sys.path.append('/home/ubuntu')
            from ml_prediction_models_fixed import SocratesMLPredictor
            
            predictor = SocratesMLPredictor()
            
            # Test prediction generation
            predictions = predictor.generate_predictions("AAPL")
            if not predictions:
                logger.error("Failed to generate ML predictions")
                return False
            
            # Check prediction quality
            if 'price_forecast' not in predictions:
                logger.error("Missing price forecast in predictions")
                return False
            
            if 'confidence' not in predictions:
                logger.error("Missing confidence in predictions")
                return False
            
            confidence = predictions.get('confidence', 0)
            if confidence < 0.5:  # Require at least 50% confidence
                logger.error(f"ML prediction confidence too low: {confidence}")
                return False
            
            logger.info(f"ML models passed. Confidence: {confidence:.1f}")
            return True
            
        except Exception as e:
            logger.error(f"ML models test failed: {e}")
            return False
    
    def test_alert_system(self) -> bool:
        """Test alert and notification system"""
        try:
            # Import and test alert system
            sys.path.append('/home/ubuntu')
            from alert_notification_system import SocratesAlertSystem
            
            alert_system = SocratesAlertSystem()
            
            # Test alert creation
            alert_id = alert_system.create_alert(
                symbol="AAPL",
                alert_type="price_threshold",
                condition="above",
                threshold=200.0,
                priority="medium"
            )
            
            if not alert_id:
                logger.error("Failed to create alert")
                return False
            
            # Test alert monitoring
            alerts = alert_system.check_alerts()
            if alerts is None:
                logger.error("Failed to check alerts")
                return False
            
            # Test notification delivery
            test_notification = {
                'type': 'test',
                'message': 'System test notification',
                'priority': 'low',
                'timestamp': datetime.now().isoformat()
            }
            
            delivery_result = alert_system.deliver_notification(test_notification, ['webhook'])
            if not delivery_result:
                logger.error("Failed to deliver test notification")
                return False
            
            logger.info("Alert system passed all tests")
            return True
            
        except Exception as e:
            logger.error(f"Alert system test failed: {e}")
            return False
    
    def test_portfolio_integration(self) -> bool:
        """Test portfolio management system"""
        try:
            # Import and test portfolio system
            sys.path.append('/home/ubuntu')
            from portfolio_integration import SocratesPortfolioManager
            
            portfolio_manager = SocratesPortfolioManager()
            
            # Test portfolio creation
            portfolio_id = portfolio_manager.create_portfolio(
                name="Test Portfolio",
                initial_capital=100000.0,
                strategy="growth"
            )
            
            if not portfolio_id:
                logger.error("Failed to create test portfolio")
                return False
            
            # Test position management
            position_id = portfolio_manager.add_position(
                portfolio_id=portfolio_id,
                symbol="AAPL",
                position_type="long",
                quantity=100,
                entry_price=200.0
            )
            
            if not position_id:
                logger.error("Failed to add position to portfolio")
                return False
            
            # Test portfolio analysis
            analysis = portfolio_manager.analyze_portfolio(portfolio_id)
            if not analysis:
                logger.error("Failed to analyze portfolio")
                return False
            
            # Test performance metrics
            performance = portfolio_manager.calculate_performance_metrics(portfolio_id)
            if not performance:
                logger.error("Failed to calculate portfolio performance")
                return False
            
            logger.info("Portfolio integration passed all tests")
            return True
            
        except Exception as e:
            logger.error(f"Portfolio integration test failed: {e}")
            return False
    
    def test_performance_optimization(self) -> bool:
        """Test performance optimization features"""
        try:
            # Import and test performance system
            sys.path.append('/home/ubuntu')
            from performance_optimization import SocratesPerformanceOptimizer
            
            optimizer = SocratesPerformanceOptimizer()
            
            # Test caching system
            cache_stats = optimizer.get_cache_statistics()
            if not cache_stats:
                logger.error("Failed to get cache statistics")
                return False
            
            # Test performance monitoring
            performance_metrics = optimizer.get_performance_metrics()
            if not performance_metrics:
                logger.error("Failed to get performance metrics")
                return False
            
            # Test system optimization
            optimization_result = optimizer.optimize_system()
            if not optimization_result:
                logger.error("Failed to optimize system")
                return False
            
            # Check performance improvements
            if 'cache_stats' not in performance_metrics:
                logger.error("Missing cache statistics in performance metrics")
                return False
            
            logger.info("Performance optimization passed all tests")
            return True
            
        except Exception as e:
            logger.error(f"Performance optimization test failed: {e}")
            return False
    
    def test_alternative_data_sources(self) -> bool:
        """Test alternative data sources integration"""
        try:
            # Import and test alternative data system
            sys.path.append('/home/ubuntu')
            from alternative_data_sources import SocratesAlternativeDataCollector
            
            data_collector = SocratesAlternativeDataCollector()
            
            # Test data collection
            collection_result = data_collector.collect_comprehensive_data("AAPL")
            if not collection_result:
                logger.error("Failed to collect alternative data")
                return False
            
            # Test data quality
            quality_score = data_collector.calculate_data_quality("AAPL")
            if quality_score < 0.7:  # Require at least 70% quality
                logger.error(f"Alternative data quality too low: {quality_score}")
                return False
            
            # Test sentiment analysis
            sentiment = data_collector.analyze_sentiment("AAPL")
            if not sentiment:
                logger.error("Failed to analyze sentiment")
                return False
            
            logger.info(f"Alternative data sources passed. Quality: {quality_score:.1f}")
            return True
            
        except Exception as e:
            logger.error(f"Alternative data sources test failed: {e}")
            return False
    
    def test_websocket_streaming(self) -> bool:
        """Test WebSocket real-time streaming"""
        try:
            import websocket
            import json
            
            # Test WebSocket connection
            messages_received = []
            
            def on_message(ws, message):
                messages_received.append(json.loads(message))
            
            def on_error(ws, error):
                logger.error(f"WebSocket error: {error}")
            
            def on_close(ws, close_status_code, close_msg):
                logger.info("WebSocket connection closed")
            
            def on_open(ws):
                logger.info("WebSocket connection opened")
                # Send test subscription
                ws.send(json.dumps({
                    'type': 'subscribe',
                    'channels': ['market_data', 'analysis_results']
                }))
            
            # Create WebSocket connection
            ws = websocket.WebSocketApp(
                "ws://localhost:5000/ws",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Run WebSocket in separate thread
            ws_thread = threading.Thread(target=ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            # Wait for messages
            time.sleep(5)
            ws.close()
            
            if not messages_received:
                logger.error("No WebSocket messages received")
                return False
            
            logger.info(f"WebSocket streaming passed. Received {len(messages_received)} messages")
            return True
            
        except Exception as e:
            logger.error(f"WebSocket streaming test failed: {e}")
            return False
    
    def test_mobile_optimization(self) -> bool:
        """Test mobile optimization features"""
        try:
            # Test mobile API endpoints
            mobile_endpoints = [
                '/api/socrates/analysis/AAPL?mobile=true',
                '/api/socrates/daily-report?mobile=true',
                '/api/socrates/global-analysis?mobile=true'
            ]
            
            for endpoint in mobile_endpoints:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                if response.status_code != 200:
                    logger.error(f"Mobile endpoint failed: {endpoint}")
                    return False
                
                # Check response size (should be smaller for mobile)
                content_length = len(response.content)
                if content_length > 50000:  # 50KB limit for mobile responses
                    logger.error(f"Mobile response too large: {content_length} bytes")
                    return False
            
            logger.info("Mobile optimization passed all tests")
            return True
            
        except Exception as e:
            logger.error(f"Mobile optimization test failed: {e}")
            return False
    
    def start_flask_server(self) -> bool:
        """Start Flask server for testing"""
        try:
            # Start enhanced Flask backend
            cmd = [
                'python', '/home/ubuntu/enhanced_flask_backend.py'
            ]
            
            self.flask_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd='/home/ubuntu'
            )
            
            # Wait for server to start
            time.sleep(10)
            
            # Test if server is running
            try:
                response = requests.get(f"{self.base_url}/api/socrates/health", timeout=5)
                if response.status_code == 200:
                    logger.info("Flask server started successfully")
                    return True
            except:
                pass
            
            logger.error("Failed to start Flask server")
            return False
            
        except Exception as e:
            logger.error(f"Error starting Flask server: {e}")
            return False
    
    def stop_flask_server(self):
        """Stop Flask server"""
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process.wait()
            logger.info("Flask server stopped")
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run complete test suite"""
        logger.info("Starting comprehensive Socrates AI system test suite")
        logger.info("=" * 60)
        
        # Start Flask server
        if not self.start_flask_server():
            logger.error("Failed to start Flask server - aborting tests")
            return self.test_results
        
        try:
            # Run all tests
            test_functions = [
                ("Database Integrity", self.test_database_integrity),
                ("Core API Endpoints", self.test_core_api_endpoints),
                ("TradingView Validation", self.test_tradingview_validation),
                ("Machine Learning Models", self.test_machine_learning_models),
                ("Alert System", self.test_alert_system),
                ("Portfolio Integration", self.test_portfolio_integration),
                ("Performance Optimization", self.test_performance_optimization),
                ("Alternative Data Sources", self.test_alternative_data_sources),
                ("WebSocket Streaming", self.test_websocket_streaming),
                ("Mobile Optimization", self.test_mobile_optimization)
            ]
            
            for test_name, test_func in test_functions:
                self.run_test(test_name, test_func)
                time.sleep(1)  # Brief pause between tests
            
        finally:
            # Stop Flask server
            self.stop_flask_server()
        
        # Calculate final statistics
        total = self.test_results['summary']['total_tests']
        passed = self.test_results['summary']['passed_tests']
        
        if total > 0:
            self.test_results['summary']['success_rate'] = (passed / total) * 100
        
        logger.info("=" * 60)
        logger.info("FINAL TEST RESULTS:")
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {self.test_results['summary']['failed_tests']}")
        logger.info(f"Success Rate: {self.test_results['summary']['success_rate']:.1f}%")
        logger.info("=" * 60)
        
        return self.test_results

def main():
    """Run the comprehensive test suite"""
    tester = SocratesAISystemTester()
    results = tester.run_comprehensive_test_suite()
    
    # Save results to file
    with open('/home/ubuntu/final_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    success_rate = results['summary']['success_rate']
    if success_rate >= 90:
        print(f"\n🎉 EXCELLENT! System test passed with {success_rate:.1f}% success rate")
        print("✅ Socrates AI is ready for production deployment!")
    elif success_rate >= 80:
        print(f"\n✅ GOOD! System test passed with {success_rate:.1f}% success rate")
        print("⚠️  Some minor issues detected - review failed tests")
    elif success_rate >= 70:
        print(f"\n⚠️  ACCEPTABLE! System test passed with {success_rate:.1f}% success rate")
        print("🔧 Several issues detected - recommend fixes before deployment")
    else:
        print(f"\n❌ FAILED! System test failed with {success_rate:.1f}% success rate")
        print("🚨 Major issues detected - system not ready for deployment")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

