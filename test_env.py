#!/usr/bin/env python3
"""
Test script to verify environment variables and API connectivity.
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
    print(f"USE_FIXTURES: {os.getenv('USE_FIXTURES', 'false')}")
    print(f"SPORTS_FILTER: {os.getenv('SPORTS_FILTER', 'Not set')}")
    print()

def test_odds_api():
    """Test TheOddsAPI connectivity."""
    api_key = os.getenv('ODDS_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return
    
    print("🔍 Testing TheOddsAPI:")
    try:
        # Test with correct sport key
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {
            'apiKey': api_key,
            'regions': 'us',
            'markets': 'h2h',
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API working - Found {len(data)} MLB games")
            if data:
                game = data[0]
                print(f"   Example: {game['away_team']} @ {game['home_team']}")
                print(f"   Time: {game['commence_time']}")
        else:
            print(f"❌ API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ API test failed: {e}")
    print()

def test_kalshi_api():
    """Test Kalshi API connectivity."""
    print("🔍 Testing Kalshi API:")
    try:
        # Test Kalshi API (this will likely fail as it requires authentication)
        url = "https://api.kalshi.com/markets"
        params = {
            'status': 'open',
            'limit': 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ Kalshi API accessible")
        else:
            print(f"⚠️  Kalshi API: {response.status_code} (expected - requires auth)")
    except Exception as e:
        print(f"⚠️  Kalshi API: {e} (expected - requires auth)")
    print()

if __name__ == "__main__":
    test_environment()
    test_odds_api()
    test_kalshi_api()
