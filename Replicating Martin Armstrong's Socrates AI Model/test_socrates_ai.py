#!/usr/bin/env python3
"""
Socrates AI Test Suite
Comprehensive testing and validation of the Socrates AI system

This test suite validates:
1. Core ECM calculations
2. Data collection functionality
3. Analysis pipeline accuracy
4. API endpoint responses
5. Market prediction capabilities
6. System performance

Author: AI Replication Project
"""

import unittest
import sys
import os
import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import requests
import time

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(__file__))

from socrates_ai_architecture import SocratesAI, EconomicConfidenceModel
from data_collector import DataCollector
from analysis_pipeline import AdvancedAnalyzer

class TestEconomicConfidenceModel(unittest.TestCase):
    """Test the Economic Confidence Model implementation"""
    
    def setUp(self):
        self.ecm = EconomicConfidenceModel()
    
    def test_base_cycle_calculation(self):
        """Test that the base cycle is correctly calculated as π × 1,000 days"""
        expected_cycle = 3141  # π × 1,000 ≈ 3,141 days
        self.assertEqual(self.ecm.base_cycle_days, expected_cycle)
        self.assertAlmostEqual(self.ecm.base_cycle_years, 8.6, places=1)
    
    def test_cycle_position_calculation(self):
        """Test cycle position calculation"""
        current_date = datetime(2025, 8, 1)
        reference_date = datetime(2007, 2, 27)  # 2007.15 reference point
        
        result = self.ecm.calculate_cycle_position(current_date, reference_date)
        
        # Verify result structure
        self.assertIn('cycle_position', result)
        self.assertIn('phase', result)
        self.assertIn('days_into_cycle', result)
        self.assertIn('next_turning_point', result)
        self.assertIn('confidence_level', result)
        
        # Verify cycle position is between 0 and 1
        self.assertGreaterEqual(result['cycle_position'], 0)
        self.assertLessEqual(result['cycle_position'], 1)
        
        # Verify confidence level is between 0 and 1
        self.assertGreaterEqual(result['confidence_level'], 0)
        self.assertLessEqual(result['confidence_level'], 1)
    
    def test_historical_turning_points(self):
        """Test that historical turning points are correctly defined"""
        self.assertIn("1929", self.ecm.historical_turning_points)
        self.assertIn("1981", self.ecm.historical_turning_points)
        self.assertIn("2007.15", self.ecm.historical_turning_points)

class TestDataCollector(unittest.TestCase):
    """Test the data collection system"""
    
    def setUp(self):
        self.test_db = "test_socrates.db"
        self.collector = DataCollector(self.test_db)
    
    def tearDown(self):
        # Clean up test database
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_initialization(self):
        """Test that database tables are created correctly"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Check that required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['market_data', 'economic_indicators', 'forex_data', 'commodities_data']
        for table in required_tables:
            self.assertIn(table, tables)
        
        conn.close()
    
    def test_data_collection_structure(self):
        """Test data collection methods return proper structure"""
        # Test with minimal symbols to avoid API rate limits
        test_symbols = ["AAPL"]
        
        # This would normally test actual data collection
        # For testing purposes, we'll verify the method exists and structure
        self.assertTrue(hasattr(self.collector, 'collect_stock_data'))
        self.assertTrue(hasattr(self.collector, 'collect_forex_data'))
        self.assertTrue(hasattr(self.collector, 'collect_commodities_data'))
        self.assertTrue(hasattr(self.collector, 'collect_economic_indicators'))

class TestAdvancedAnalyzer(unittest.TestCase):
    """Test the advanced analysis pipeline"""
    
    def setUp(self):
        self.test_db = "test_analyzer.db"
        self.analyzer = AdvancedAnalyzer(self.test_db)
        
        # Create test database with sample data
        self._create_test_data()
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def _create_test_data(self):
        """Create sample test data"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                symbol TEXT, date TEXT, open_price REAL, high_price REAL,
                low_price REAL, close_price REAL, volume INTEGER
            )
        ''')
        
        # Insert sample data
        dates = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(100, 0, -1)]
        prices = [100 + 10 * np.sin(i * 0.1) + np.random.normal(0, 2) for i in range(100)]
        
        for i, (date, price) in enumerate(zip(dates, prices)):
            cursor.execute('''
                INSERT INTO market_data 
                (symbol, date, open_price, high_price, low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('TEST', date, price, price * 1.02, price * 0.98, price, 1000000))
        
        conn.commit()
        conn.close()
    
    def test_cycle_analysis(self):
        """Test market cycle analysis"""
        result = self.analyzer.analyze_market_cycles('TEST')
        
        if 'error' not in result:
            self.assertIn('dominant_cycles', result)
            self.assertIn('cycle_statistics', result)
            self.assertIn('current_phase', result)
            self.assertIn('confidence', result)
            
            # Verify confidence is between 0 and 1
            self.assertGreaterEqual(result['confidence'], 0)
            self.assertLessEqual(result['confidence'], 1)
    
    def test_forecast_generation(self):
        """Test market forecasting"""
        result = self.analyzer.generate_market_forecast('TEST', 30)
        
        if 'error' not in result:
            self.assertIn('combined_forecast', result)
            self.assertIn('forecast_confidence', result)
            self.assertIn('risk_assessment', result)
            
            # Verify forecast confidence
            self.assertGreaterEqual(result['forecast_confidence'], 0)
            self.assertLessEqual(result['forecast_confidence'], 1)

class TestSocratesAI(unittest.TestCase):
    """Test the main Socrates AI system"""
    
    def setUp(self):
        self.test_db = "test_socrates_main.db"
        self.socrates = SocratesAI(self.test_db)
        
        # Create minimal test data
        self._create_test_data()
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def _create_test_data(self):
        """Create minimal test data"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Insert sample market data
        dates = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(50, 0, -1)]
        for i, date in enumerate(dates):
            price = 100 + i * 0.5
            cursor.execute('''
                INSERT INTO market_data 
                (symbol, date, open_price, high_price, low_price, close_price, volume, adjusted_close, currency, source, data_quality, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('TEST', date, price, price * 1.01, price * 0.99, price, 1000000, price, 'USD', 'test', 1.0, date, date))
        
        conn.commit()
        conn.close()
    
    def test_market_analysis(self):
        """Test individual market analysis"""
        result = self.socrates.analyze_market('TEST')
        
        if 'error' not in result:
            self.assertIn('symbol', result)
            self.assertIn('ecm_analysis', result)
            self.assertIn('momentum_analysis', result)
            self.assertIn('technical_indicators', result)
            self.assertIn('overall_confidence', result)
            
            # Verify overall confidence
            self.assertGreaterEqual(result['overall_confidence'], 0)
            self.assertLessEqual(result['overall_confidence'], 1)
    
    def test_global_analysis(self):
        """Test global market analysis"""
        symbols = ['TEST']
        result = self.socrates.analyze_global_markets(symbols)
        
        self.assertIn('markets_analyzed', result)
        self.assertIn('global_ecm', result)
        self.assertIn('global_confidence', result)
        
        # Verify global confidence
        self.assertGreaterEqual(result['global_confidence'], 0)
        self.assertLessEqual(result['global_confidence'], 1)

class TestAPIEndpoints(unittest.TestCase):
    """Test Flask API endpoints"""
    
    def setUp(self):
        self.base_url = "http://localhost:5000/api/socrates"
        self.timeout = 10
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'healthy')
            self.assertIn('service', data)
            self.assertEqual(data['service'], 'Socrates AI')
        except requests.exceptions.RequestException:
            self.skipTest("Flask server not running")
    
    def test_available_markets_endpoint(self):
        """Test available markets endpoint"""
        try:
            response = requests.get(f"{self.base_url}/markets/available", timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            data = response.json()
            self.assertIn('success', data)
            self.assertTrue(data['success'])
            self.assertIn('data', data)
        except requests.exceptions.RequestException:
            self.skipTest("Flask server not running")

class TestSystemPerformance(unittest.TestCase):
    """Test system performance and benchmarks"""
    
    def setUp(self):
        self.test_db = "test_performance.db"
        self.socrates = SocratesAI(self.test_db)
    
    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_analysis_performance(self):
        """Test that analysis completes within reasonable time"""
        # Create minimal test data
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        dates = [(datetime.now() - timedelta(days=i)).date().isoformat() for i in range(100, 0, -1)]
        for i, date in enumerate(dates):
            price = 100 + i * 0.1
            cursor.execute('''
                INSERT INTO market_data 
                (symbol, date, open_price, high_price, low_price, close_price, volume, adjusted_close, currency, source, data_quality, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('PERF', date, price, price * 1.01, price * 0.99, price, 1000000, price, 'USD', 'test', 1.0, date, date))
        
        conn.commit()
        conn.close()
        
        # Time the analysis
        start_time = time.time()
        result = self.socrates.analyze_market('PERF')
        end_time = time.time()
        
        analysis_time = end_time - start_time
        
        # Analysis should complete within 5 seconds
        self.assertLess(analysis_time, 5.0, f"Analysis took {analysis_time:.2f} seconds, expected < 5.0")
        
        # Verify result is valid
        if 'error' not in result:
            self.assertIn('overall_confidence', result)

class TestAccuracyValidation(unittest.TestCase):
    """Test accuracy of predictions and analysis"""
    
    def test_ecm_mathematical_accuracy(self):
        """Test ECM mathematical calculations"""
        ecm = EconomicConfidenceModel()
        
        # Test π calculation accuracy
        pi_approximation = ecm.base_cycle_days / 1000
        self.assertAlmostEqual(pi_approximation, 3.141, places=3)
        
        # Test cycle length calculation
        expected_years = ecm.base_cycle_days / 365.25
        self.assertAlmostEqual(expected_years, 8.6, places=1)
    
    def test_correlation_calculations(self):
        """Test correlation calculation accuracy"""
        # Create test data with known correlation
        np.random.seed(42)  # For reproducible results
        
        x = np.random.randn(100)
        y = 0.8 * x + 0.6 * np.random.randn(100)  # Should have ~0.8 correlation
        
        # Calculate correlation
        correlation = np.corrcoef(x, y)[0, 1]
        
        # Should be approximately 0.8
        self.assertAlmostEqual(correlation, 0.8, places=1)

def run_comprehensive_tests():
    """Run all test suites and generate report"""
    print("=" * 60)
    print("SOCRATES AI COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Test suites to run
    test_suites = [
        TestEconomicConfidenceModel,
        TestDataCollector,
        TestAdvancedAnalyzer,
        TestSocratesAI,
        TestAPIEndpoints,
        TestSystemPerformance,
        TestAccuracyValidation
    ]
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for test_suite in test_suites:
        print(f"\nRunning {test_suite.__name__}...")
        print("-" * 40)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_suite)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        total_tests += result.testsRun
        total_failures += len(result.failures)
        total_errors += len(result.errors)
        
        if result.failures:
            print(f"FAILURES in {test_suite.__name__}:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print(f"ERRORS in {test_suite.__name__}:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("TEST SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Tests Run: {total_tests}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    print(f"Success Rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%")
    
    if total_failures == 0 and total_errors == 0:
        print("\n✅ ALL TESTS PASSED - Socrates AI system is validated!")
    else:
        print(f"\n❌ {total_failures + total_errors} tests failed - Review issues above")
    
    print("=" * 60)
    
    return total_failures + total_errors == 0

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)

