#!/usr/bin/env python3
"""
PricePulse Quick Test Script
This script tests if everything is working correctly
"""

import requests
import json
import time
import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*50)
    print(f"🔍 {text}")
    print("="*50)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_backend_health():
    """Test if the backend is running and healthy"""
    print_header("Testing Backend Health")
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Backend is running!")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Message: {data.get('message')}")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend at http://localhost:5000")
        print_info("Make sure you ran 'python app.py' in your backend folder")
        return False
    except Exception as e:
        print_error(f"Backend test failed: {str(e)}")
        return False

def test_product_search():
    """Test product search functionality"""
    print_header("Testing Product Search")
    
    try:
        response = requests.get(
            'http://localhost:5000/api/search',
            params={'q': 'iPhone 15', 'type': 'products'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Product search is working!")
            print_info(f"Query: {data.get('query')}")
            print_info(f"Results found: {data.get('total_products', 0)}")
            print_info(f"Search time: {data.get('search_duration_seconds')}s")
            
            if data.get('products'):
                print_info("Sample results:")
                for i, product in enumerate(data['products'][:2], 1):
                    print(f"  {i}. {product['title']} - {product['platform']} - ${product.get('total_cost', 'N/A')}")
            
            return True
        else:
            print_error(f"Product search failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Product search test failed: {str(e)}")
        return False

def test_service_search():
    """Test service search functionality"""
    print_header("Testing Service Search")
    
    try:
        response = requests.get(
            'http://localhost:5000/api/search',
            params={'q': 'web development', 'type': 'services'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Service search is working!")
            print_info(f"Query: {data.get('query')}")
            print_info(f"Results found: {data.get('total_services', 0)}")
            print_info(f"Search time: {data.get('search_duration_seconds')}s")
            
            if data.get('services'):
                print_info("Sample results:")
                for i, service in enumerate(data['services'][:2], 1):
                    price = service.get('starting_price', service.get('hourly_rate', 'Quote'))
                    print(f"  {i}. {service['title']} - {service['platform']} - ${price}")
            
            return True
        else:
            print_error(f"Service search failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Service search test failed: {str(e)}")
        return False

def test_platforms():
    """Test platforms endpoint"""
    print_header("Testing Platforms Endpoint")
    
    try:
        response = requests.get('http://localhost:5000/api/platforms', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Platforms endpoint is working!")
            print_info(f"Platforms available: {len(data.get('platforms', []))}")
            
            for platform in data.get('platforms', [])[:3]:
                print(f"  • {platform['name']} - Trust: {platform['trust_score']}% - Status: {platform['status']}")
            
            return True
        else:
            print_error(f"Platforms endpoint failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Platforms test failed: {str(e)}")
        return False

def check_frontend():
    """Check if frontend is accessible"""
    print_header("Testing Frontend")
    
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print_success("Frontend is accessible at http://localhost:3000")
            print_info("You can open this in your browser to see the website")
            return True
        else:
            print_error(f"Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to frontend at http://localhost:3000")
        print_info("Make sure you ran 'npm start' in your frontend folder")
        return False
    except Exception as e:
        print_error(f"Frontend test failed: {str(e)}")
        return False

def check_required_packages():
    """Check if required Python packages are installed"""
    print_header("Checking Required Packages")
    
    required_packages = ['flask', 'flask_cors', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print_info("To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_comprehensive_test():
    """Run all tests and provide a summary"""
    print("🚀 PricePulse Comprehensive Test Suite")
    print("This will test if everything is working correctly")
    
    tests = [
        ("Required Packages", check_required_packages),
        ("Backend Health", test_backend_health),
        ("Product Search", test_product_search),
        ("Service Search", test_service_search),
        ("Platforms API", test_platforms),
        ("Frontend Access", check_frontend)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print_header("Test Results Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall Score: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your PricePulse system is working perfectly!")
        print_info("You can now:")
        print("   • Open http://localhost:3000 in your browser")
        print("   • Search for products and services")
        print("   • Start customizing your website")
        print("   • Deploy to the internet when ready")
    else:
        print_error("⚠️  Some tests failed. Please check the errors above.")
        print_info("Common solutions:")
        print("   • Make sure backend is running: python app.py")
        print("   • Make sure frontend is running: npm start")
        print("   • Install missing packages: pip install flask flask-cors requests")
        print("   • Check if ports 3000 and 5000 are available")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
