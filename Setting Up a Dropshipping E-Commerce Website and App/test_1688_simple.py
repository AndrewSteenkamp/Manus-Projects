#!/usr/bin/env python3
"""
Simple 1688.com connectivity test
"""

import requests
from urllib.parse import quote
import time

def test_1688_connection():
    """Test basic connection to 1688.com"""
    print("🔍 Testing 1688.com connectivity...")
    
    # Test basic connection
    try:
        response = requests.get("https://www.1688.com", timeout=10)
        print(f"✅ 1688.com connection: {response.status_code}")
    except Exception as e:
        print(f"❌ 1688.com connection failed: {e}")
        return False
    
    # Test search functionality
    try:
        search_term = "手机壳"  # Phone case in Chinese
        encoded_term = quote(search_term)
        search_url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_term}"
        
        print(f"🔍 Testing search for: {search_term}")
        print(f"🔗 Search URL: {search_url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        print(f"✅ Search response: {response.status_code}")
        print(f"📄 Response length: {len(response.content)} bytes")
        
        # Check if we got actual content
        if len(response.content) > 1000:
            print("✅ Received substantial content from 1688.com")
            
            # Save a sample for inspection
            with open('/home/ubuntu/alpapies-complete-project/1688_sample.html', 'w', encoding='utf-8') as f:
                f.write(response.text[:5000])  # First 5000 characters
            print("📁 Sample saved to: 1688_sample.html")
            
            return True
        else:
            print("❌ Received minimal content - possible blocking")
            return False
            
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def test_product_search():
    """Test searching for specific products"""
    products = [
        ("iPhone手机壳", "iPhone case"),
        ("无线充电器", "Wireless charger"),
        ("钢化膜", "Screen protector")
    ]
    
    print("\n🛍️ Testing product searches...")
    
    for chinese, english in products:
        try:
            print(f"\n🔍 Searching for: {english} ({chinese})")
            
            encoded_term = quote(chinese)
            search_url = f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded_term}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {english}: {response.status_code} - {len(response.content)} bytes")
                
                # Look for product indicators in the response
                content = response.text.lower()
                if any(indicator in content for indicator in ['offer', 'product', 'price', '价格', '产品']):
                    print(f"✅ Found product indicators for {english}")
                else:
                    print(f"⚠️ No clear product indicators for {english}")
            else:
                print(f"❌ {english}: {response.status_code}")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error searching for {english}: {e}")

def main():
    print("🚀 1688.com Real Connectivity Test")
    print("=" * 40)
    
    # Test basic connection
    if test_1688_connection():
        print("\n✅ Basic connectivity successful!")
        
        # Test product searches
        test_product_search()
        
        print("\n🎯 Test completed! Check the results above.")
        print("📁 Sample HTML saved for inspection.")
    else:
        print("\n❌ Basic connectivity failed!")
        print("🔧 This might be due to:")
        print("   - Network restrictions")
        print("   - 1688.com blocking automated requests")
        print("   - Geographic restrictions")
        print("   - Rate limiting")

if __name__ == "__main__":
    main()

