#!/usr/bin/env python3
"""
Test script to verify service search functionality
"""

import requests
import json

API_BASE_URL = 'http://localhost:5000/api'

def test_service_search():
    """Test the service search endpoint"""
    print("🔍 Testing Service Search...")
    
    # Test service search
    response = requests.get(f'{API_BASE_URL}/service-search', params={
        'q': 'graphic design',
        'category': 'Digital Services',
        'max_results': 5,
        'currency': 'USD'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total_services']} services across {data['platforms_searched']} platforms")
        print(f"⏱️  Search completed in {data['search_duration_seconds']}s")
        
        if data['services']:
            print("\n📋 Top Services:")
            for i, service in enumerate(data['services'][:3], 1):
                price = service.get('starting_price', service.get('hourly_rate', service.get('bid_amount', 'Quote')))
                print(f"{i}. {service['title']} ({service['platform']}) - ${price}")
                print(f"   Rating: {service.get('provider_rating', 'N/A')}/5 | {service.get('recommendation_level', 'N/A')}")
        
        if data['recommendations']:
            print(f"\n💡 Recommendations: {len(data['recommendations'])}")
            for rec in data['recommendations'][:2]:
                print(f"   • {rec}")
        
        return True
    else:
        print(f"❌ Service search failed: {response.status_code}")
        return False

def test_service_categories():
    """Test the service categories endpoint"""
    print("\n📂 Testing Service Categories...")
    
    response = requests.get(f'{API_BASE_URL}/service-categories')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total_categories']} categories and {data['total_platforms']} platforms")
        
        print("\n📋 Categories:")
        for category, info in data['categories'].items():
            print(f"   • {category}: {len(info['subcategories'])} subcategories")
        
        return True
    else:
        print(f"❌ Categories test failed: {response.status_code}")
        return False

def test_service_suggestions():
    """Test the service suggestions endpoint"""
    print("\n💭 Testing Service Suggestions...")
    
    response = requests.get(f'{API_BASE_URL}/service-suggestions', params={'q': 'web'})
    
    if response.status_code == 200:
        data = response.json()
        suggestions = data.get('suggestions', [])
        print(f"✅ Found {len(suggestions)} suggestions for 'web'")
        
        if suggestions:
            print("📋 Suggestions:")
            for suggestion in suggestions[:5]:
                print(f"   • {suggestion}")
        
        return True
    else:
        print(f"❌ Suggestions test failed: {response.status_code}")
        return False

def main():
    """Run all service search tests"""
    print("🚀 PricePulse Service Search Test Suite")
    print("=" * 50)
    
    tests = [
        test_service_search,
        test_service_categories,
        test_service_suggestions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All service search functionality is working perfectly!")
        return True
    else:
        print("⚠️  Some tests failed - check the backend server")
        return False

if __name__ == "__main__":
    main()
