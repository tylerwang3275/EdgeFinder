#!/usr/bin/env python3
"""
Test script to debug API issues in deployed environment.
"""

import requests
import json
import os

# Test the deployed application's API endpoints
RENDER_APP_URL = "https://edgefinder-czi3.onrender.com"

def test_deployed_endpoints():
    """Test all deployed endpoints to understand the issue."""
    
    print("🔍 Testing Deployed EdgeFinder Application")
    print("=" * 50)
    
    # Test health
    print("\n1. Health Check:")
    try:
        response = requests.get(f"{RENDER_APP_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test debug info
    print("\n2. Debug Info:")
    try:
        response = requests.get(f"{RENDER_APP_URL}/debug", timeout=10)
        print(f"   Status: {response.status_code}")
        debug_data = response.json()
        print(f"   Use Fixtures: {debug_data.get('use_fixtures')}")
        print(f"   Odds API Key Set: {debug_data.get('odds_api_key_set')}")
        print(f"   Sports Filter: {debug_data.get('sports_filter')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test odds endpoint
    print("\n3. Odds Debug:")
    try:
        response = requests.get(f"{RENDER_APP_URL}/debug/odds", timeout=10)
        print(f"   Status: {response.status_code}")
        odds_data = response.json()
        print(f"   Status: {odds_data.get('status')}")
        print(f"   Odds Count: {odds_data.get('odds_count')}")
        if odds_data.get('sample_odds'):
            sample = odds_data['sample_odds']
            print(f"   Sample Game: {sample.get('away_team')} @ {sample.get('home_team')}")
            print(f"   Game ID: {sample.get('game_id')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Robinhood endpoint
    print("\n4. Robinhood Debug:")
    try:
        response = requests.get(f"{RENDER_APP_URL}/debug/robinhood", timeout=10)
        print(f"   Status: {response.status_code}")
        robinhood_data = response.json()
        print(f"   Status: {robinhood_data.get('status')}")
        print(f"   Markets Count: {robinhood_data.get('markets_count')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test latest report
    print("\n5. Latest Report:")
    try:
        response = requests.get(f"{RENDER_APP_URL}/api/latest", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            lines = content.split('\n')
            for line in lines[:10]:  # First 10 lines
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_deployed_endpoints()
