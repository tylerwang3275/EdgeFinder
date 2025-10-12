#!/usr/bin/env python3
"""
Test script to verify deployment environment and API connectivity.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment variables."""
    print("🔍 Testing Environment Variables:")
    print(f"ODDS_API_KEY: {'✅ Set' if os.getenv('ODDS_API_KEY') else '❌ Missing'}")
    print(f"KALSHI_API_KEY_ID: {'✅ Set' if os.getenv('KALSHI_API_KEY_ID') else '❌ Missing'}")
    print(f"KALSHI_PRIVATE_KEY: {'✅ Set' if os.getenv('KALSHI_PRIVATE_KEY') else '❌ Missing'}")
    print(f"USE_FIXTURES: {os.getenv('USE_FIXTURES', 'false')}")
    print(f"SPORTS_FILTER: {os.getenv('SPORTS_FILTER', 'Not set')}")
    print()

def test_odds_api_direct():
    """Test TheOddsAPI directly."""
    api_key = os.getenv('ODDS_API_KEY')
    if not api_key:
        print("❌ No ODDS_API_KEY found")
        return
    
    print("🔍 Testing TheOddsAPI Direct:")
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {
            'apiKey': api_key,
            'regions': 'us',
            'markets': 'h2h',
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📊 Direct API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Direct API working - Found {len(data)} MLB games")
            if data:
                game = data[0]
                print(f"   Example: {game['away_team']} @ {game['home_team']}")
        else:
            print(f"❌ Direct API error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
    print()

def test_pipeline_locally():
    """Test the pipeline locally."""
    print("🔍 Testing Pipeline Locally:")
    try:
        from src.config import load_config
        from src.data.odds_client import OddsClient
        
        config = load_config()
        print(f"Config loaded - USE_FIXTURES: {config.use_fixtures}")
        print(f"Sports filter: {config.sports_filter}")
        print(f"API key set: {bool(config.odds_api_key)}")
        
        if not config.use_fixtures:
            client = OddsClient(config)
            odds = client.get_odds(["baseball_mlb"])
            print(f"✅ Pipeline test - Found {len(odds)} odds")
        else:
            print("✅ Using fixtures mode")
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
    print()

if __name__ == "__main__":
    test_environment()
    test_odds_api_direct()
    test_pipeline_locally()
    
    print("💡 Next Steps:")
    print("1. Check if environment variables are set correctly")
    print("2. Verify API key is valid")
    print("3. Test pipeline locally vs deployed")
    print("4. Check Render deployment logs")
