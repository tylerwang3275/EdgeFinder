#!/usr/bin/env python3
"""
Debug script to identify deployment issues with the sportsbook API.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sportsbook_api_direct():
    """Test the sportsbook API directly with the same parameters as the deployed app."""
    print("🔍 Testing Sportsbook API Direct:")
    
    api_key = "d98557c1e7c0485b02c4a0389890d6db"
    base_url = "https://api.the-odds-api.com/v4"
    
    # Test each sport that should be in the deployed environment
    sports = [
        "baseball_mlb",
        "americanfootball_nfl", 
        "basketball_nba",
        "icehockey_nhl",
        "soccer_epl"
    ]
    
    total_games = 0
    
    for sport in sports:
        try:
            url = f"{base_url}/sports/{sport}/odds"
            params = {
                'apiKey': api_key,
                'regions': 'us',
                'markets': 'h2h,spreads,totals',
                'oddsFormat': 'american',
                'dateFormat': 'iso'
            }
            
            print(f"\n📊 Testing {sport}:")
            print(f"   URL: {url}")
            print(f"   Params: {params}")
            
            response = requests.get(url, params=params, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                game_count = len(data)
                total_games += game_count
                print(f"   ✅ Found {game_count} games")
                
                if data:
                    # Show first game details
                    first_game = data[0]
                    print(f"   📅 Example: {first_game['away_team']} @ {first_game['home_team']}")
                    print(f"   🕐 Start: {first_game['commence_time']}")
                    print(f"   📚 Books: {len(first_game.get('bookmakers', []))}")
            else:
                print(f"   ❌ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"\n📊 Total games found: {total_games}")
    return total_games

def test_deployed_endpoints():
    """Test the deployed endpoints to see what's happening."""
    print("\n🔍 Testing Deployed Endpoints:")
    
    base_url = "https://edgefinder-czi3.onrender.com"
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
    
    # Test debug
    try:
        response = requests.get(f"{base_url}/debug", timeout=10)
        print(f"✅ Debug: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Debug failed: {e}")
    
    # Test odds debug
    try:
        response = requests.get(f"{base_url}/debug/odds", timeout=10)
        print(f"✅ Odds Debug: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Odds Debug failed: {e}")
    
    # Test Robinhood debug
    try:
        response = requests.get(f"{base_url}/debug/robinhood", timeout=10)
        print(f"✅ Robinhood Debug: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Robinhood Debug failed: {e}")

def test_environment_variables():
    """Test what environment variables are available."""
    print("\n🔍 Testing Environment Variables:")
    
    # Check local environment
    print("Local Environment:")
    print(f"   ODDS_API_KEY: {'✅ Set' if os.getenv('ODDS_API_KEY') else '❌ Missing'}")
    print(f"   USE_FIXTURES: {os.getenv('USE_FIXTURES', 'Not set')}")
    print(f"   SPORTS_FILTER: {os.getenv('SPORTS_FILTER', 'Not set')}")
    
    # Check if we can access the deployed environment
    print("\nDeployed Environment (from debug endpoint):")
    try:
        response = requests.get("https://edgefinder-czi3.onrender.com/debug", timeout=10)
        if response.status_code == 200:
            debug_data = response.json()
            print(f"   Sports Filter: {debug_data.get('sports_filter', 'Not set')}")
            print(f"   Use Fixtures: {debug_data.get('use_fixtures', 'Not set')}")
            print(f"   Odds API Key Set: {debug_data.get('odds_api_key_set', 'Not set')}")
        else:
            print(f"   ❌ Could not get debug info: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Could not get debug info: {e}")

if __name__ == "__main__":
    print("🚀 EdgeFinder Deployment Debug")
    print("=" * 50)
    
    test_environment_variables()
    test_sportsbook_api_direct()
    test_deployed_endpoints()
    
    print("\n💡 Next Steps:")
    print("1. If direct API works but deployed doesn't, check environment variables")
    print("2. If environment variables are wrong, update them on Render")
    print("3. If API key is invalid, check the key on TheOddsAPI website")
    print("4. If all else fails, temporarily enable fixtures mode for demo")
