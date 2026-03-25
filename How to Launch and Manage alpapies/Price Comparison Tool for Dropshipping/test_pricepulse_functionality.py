#!/usr/bin/env python3
"""
Comprehensive test script for PricePulse functionality
Tests all core features including real-time price collection, currency conversion, and cost calculations
"""

import requests
import json
import time
from datetime import datetime
import sys

BASE_URL = "http://localhost:5000/api"

class PricePulseTest:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.total_tests = 0
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        self.log("Testing health check endpoint...")
        self.total_tests += 1
        
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log("✓ Health check passed", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log(f"✗ Health check failed: {data}", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Health check returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Health check exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_platforms_endpoint(self):
        """Test the platforms information endpoint"""
        self.log("Testing platforms endpoint...")
        self.total_tests += 1
        
        try:
            response = requests.get(f"{BASE_URL}/platforms", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("total_platforms") >= 7 and len(data.get("platforms", [])) >= 7:
                    self.log(f"✓ Platforms endpoint returned {data['total_platforms']} platforms", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log(f"✗ Platforms endpoint returned insufficient data", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Platforms endpoint returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Platforms endpoint exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_basic_search(self):
        """Test basic search functionality"""
        self.log("Testing basic search functionality...")
        self.total_tests += 1
        
        try:
            params = {
                'q': 'wireless headphones',
                'currency': 'USD',
                'country': 'US',
                'max_results': 2
            }
            
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/live-search", params=params, timeout=30)
            search_duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                total_products = data.get("summary", {}).get("total_products", 0)
                platforms_with_results = data.get("summary", {}).get("platforms_with_results", 0)
                
                if total_products >= 5 and platforms_with_results >= 3:
                    self.log(f"✓ Basic search found {total_products} products across {platforms_with_results} platforms in {search_duration:.2f}s", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log(f"✗ Basic search returned insufficient results: {total_products} products, {platforms_with_results} platforms", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Basic search returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Basic search exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_currency_conversion(self):
        """Test currency conversion functionality"""
        self.log("Testing currency conversion...")
        self.total_tests += 1
        
        try:
            params = {
                'q': 'iPhone 15',
                'currency': 'EUR',
                'country': 'DE',
                'max_results': 2
            }
            
            response = requests.get(f"{BASE_URL}/live-search", params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if currency conversion worked
                if data.get("user_currency") == "EUR":
                    # Check if products have converted prices
                    has_converted_prices = False
                    for platform, platform_data in data.get("results", {}).items():
                        for product in platform_data.get("products", []):
                            if product.get("user_currency") == "EUR" and product.get("converted_price"):
                                has_converted_prices = True
                                break
                        if has_converted_prices:
                            break
                    
                    if has_converted_prices:
                        self.log("✓ Currency conversion to EUR working correctly", "SUCCESS")
                        self.passed_tests += 1
                        return True
                    else:
                        self.log("✗ Currency conversion failed - no converted prices found", "ERROR")
                        self.failed_tests += 1
                        return False
                else:
                    self.log(f"✗ Currency conversion failed - expected EUR, got {data.get('user_currency')}", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Currency conversion test returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Currency conversion exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_cost_calculation(self):
        """Test hidden cost calculation (shipping, taxes, duties)"""
        self.log("Testing cost calculation with shipping and taxes...")
        self.total_tests += 1
        
        try:
            params = {
                'q': 'laptop',
                'currency': 'GBP',
                'country': 'GB',
                'max_results': 2,
                'include_shipping': 'true',
                'include_taxes': 'true'
            }
            
            response = requests.get(f"{BASE_URL}/live-search", params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if cost breakdown is present
                has_cost_breakdown = False
                for platform, platform_data in data.get("results", {}).items():
                    for product in platform_data.get("products", []):
                        cost_breakdown = product.get("cost_breakdown")
                        if cost_breakdown and cost_breakdown.get("total_cost") > cost_breakdown.get("base_price"):
                            has_cost_breakdown = True
                            self.log(f"   Found cost breakdown: Base £{cost_breakdown['base_price']}, Total £{cost_breakdown['total_cost']}", "INFO")
                            break
                    if has_cost_breakdown:
                        break
                
                if has_cost_breakdown:
                    self.log("✓ Cost calculation with shipping and taxes working correctly", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log("✗ Cost calculation failed - no cost breakdowns found", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Cost calculation test returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Cost calculation exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_multiple_platforms(self):
        """Test that multiple platforms are returning results"""
        self.log("Testing multiple platform integration...")
        self.total_tests += 1
        
        try:
            params = {
                'q': 'smartphone',
                'currency': 'USD',
                'country': 'US',
                'max_results': 3
            }
            
            response = requests.get(f"{BASE_URL}/live-search", params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", {})
                
                platforms_with_products = []
                for platform, platform_data in results.items():
                    if platform_data.get("products"):
                        platforms_with_products.append(platform)
                
                if len(platforms_with_products) >= 4:
                    self.log(f"✓ Multiple platforms working: {', '.join(platforms_with_products)}", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log(f"✗ Insufficient platforms with results: {platforms_with_products}", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Multiple platforms test returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Multiple platforms exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_search_performance(self):
        """Test search performance and response times"""
        self.log("Testing search performance...")
        self.total_tests += 1
        
        try:
            params = {
                'q': 'gaming mouse',
                'currency': 'USD',
                'country': 'US',
                'max_results': 3
            }
            
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/live-search", params=params, timeout=30)
            total_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                reported_duration = data.get("search_duration_seconds", 0)
                
                if total_time <= 15 and reported_duration <= 15:  # Should complete within 15 seconds
                    self.log(f"✓ Search performance acceptable: {total_time:.2f}s total, {reported_duration:.2f}s reported", "SUCCESS")
                    self.passed_tests += 1
                    return True
                else:
                    self.log(f"✗ Search performance too slow: {total_time:.2f}s total, {reported_duration:.2f}s reported", "ERROR")
                    self.failed_tests += 1
                    return False
            else:
                self.log(f"✗ Performance test returned status {response.status_code}", "ERROR")
                self.failed_tests += 1
                return False
        except Exception as e:
            self.log(f"✗ Performance test exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        self.log("Testing edge cases...")
        self.total_tests += 1
        
        try:
            # Test empty query
            response1 = requests.get(f"{BASE_URL}/live-search", params={'q': ''}, timeout=10)
            
            # Test invalid currency
            response2 = requests.get(f"{BASE_URL}/live-search", params={'q': 'test', 'currency': 'INVALID'}, timeout=10)
            
            # Test very long query
            response3 = requests.get(f"{BASE_URL}/live-search", params={'q': 'a' * 1000}, timeout=15)
            
            edge_cases_handled = 0
            
            if response1.status_code == 400:  # Should return error for empty query
                edge_cases_handled += 1
                self.log("   ✓ Empty query handled correctly", "INFO")
            
            if response2.status_code in [200, 400]:  # Should either work with fallback or return error
                edge_cases_handled += 1
                self.log("   ✓ Invalid currency handled", "INFO")
            
            if response3.status_code in [200, 400]:  # Should either work or return error
                edge_cases_handled += 1
                self.log("   ✓ Long query handled", "INFO")
            
            if edge_cases_handled >= 2:
                self.log("✓ Edge cases handled appropriately", "SUCCESS")
                self.passed_tests += 1
                return True
            else:
                self.log("✗ Edge cases not handled properly", "ERROR")
                self.failed_tests += 1
                return False
                
        except Exception as e:
            self.log(f"✗ Edge cases test exception: {e}", "ERROR")
            self.failed_tests += 1
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        self.log("Starting PricePulse functionality tests...")
        self.log("=" * 60)
        
        # Run all tests
        tests = [
            self.test_health_check,
            self.test_platforms_endpoint,
            self.test_basic_search,
            self.test_currency_conversion,
            self.test_cost_calculation,
            self.test_multiple_platforms,
            self.test_search_performance,
            self.test_edge_cases
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.log(f"✗ Test {test.__name__} failed with exception: {e}", "ERROR")
                self.failed_tests += 1
        
        # Generate report
        self.log("=" * 60)
        self.log("TEST RESULTS SUMMARY")
        self.log("=" * 60)
        self.log(f"Total tests run: {self.total_tests}")
        self.log(f"Tests passed: {self.passed_tests}")
        self.log(f"Tests failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        self.log(f"Success rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.log("🎉 PricePulse core functionality is WORKING!", "SUCCESS")
            return True
        else:
            self.log("❌ PricePulse has significant issues that need addressing", "ERROR")
            return False

def main():
    """Main test execution"""
    print("PricePulse Functionality Test Suite")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ PricePulse server is not running or not responding")
            print("Please start the server with: python3 src/main.py")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to PricePulse server: {e}")
        print("Please start the server with: python3 src/main.py")
        sys.exit(1)
    
    # Run tests
    tester = PricePulseTest()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
