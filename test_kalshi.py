#!/usr/bin/env python3
"""
Test script for Kalshi API connection.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_kalshi_connection():
    """Test Kalshi API connection."""
    api_key = os.getenv('KALSHI_API_KEY', '')
    
    print("🔍 Testing Kalshi API Connection:")
    print(f"API Key Set: {'✅ Yes' if api_key else '❌ No'}")
    
    if not api_key:
        print("❌ No Kalshi API key found in environment variables")
        print("💡 Add KALSHI_API_KEY to your .env file or environment")
        return
    
    # Test different authentication methods
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'EdgeFinder/1.0'
    }
    
    # Try with Bearer prefix
    if not api_key.startswith('Bearer '):
        headers['Authorization'] = f'Bearer {api_key}'
    else:
        headers['Authorization'] = api_key
    
    try:
        # Test basic connection
        url = "https://api.kalshi.com/markets"
        params = {'limit': 1}
        
        print(f"🌐 Testing connection to: {url}")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully connected to Kalshi API!")
            data = response.json()
            print(f"📈 Found {len(data.get('markets', []))} markets")
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API key")
        elif response.status_code == 403:
            print("❌ Access forbidden - API access may not be approved")
        else:
            print(f"⚠️  Unexpected response: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_public_kalshi():
    """Test if we can access any public Kalshi data."""
    print("\n🔍 Testing Public Kalshi Access:")
    
    try:
        # Try without authentication
        url = "https://api.kalshi.com/markets"
        params = {'limit': 1}
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📊 Public Access Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Public access available!")
        else:
            print("❌ Public access not available")
            
    except Exception as e:
        print(f"❌ Public access test failed: {e}")

if __name__ == "__main__":
    test_kalshi_connection()
    test_public_kalshi()
    
    print("\n💡 Next Steps:")
    print("1. Get Kalshi API access at kalshi.com")
    print("2. Add KALSHI_API_KEY to your environment")
    print("3. Set USE_FIXTURES=false on Render")
    print("4. Test your live EdgeFinder site!")
