#!/usr/bin/env python3
"""
Test script to verify real-time data sources.
"""

import requests
import json
from datetime import datetime

def test_sportsbook_realtime():
    """Test sportsbook API for real-time data."""
    print("🔍 Testing Sportsbook API for Real-Time Data:")
    
    api_key = "d98557c1e7c0485b02c4a0389890d6db"
    
    # Test MLB
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
        if response.status_code == 200:
            data = response.json()
            print(f"✅ MLB: Found {len(data)} games")
            for game in data[:3]:  # Show first 3 games
                start_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                print(f"   📅 {game['away_team']} @ {game['home_team']} - {start_time.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            print(f"❌ MLB API error: {response.status_code}")
    except Exception as e:
        print(f"❌ MLB test failed: {e}")
    
    # Test NFL
    try:
        url = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
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
            print(f"✅ NFL: Found {len(data)} games")
            for game in data[:3]:  # Show first 3 games
                start_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                print(f"   📅 {game['away_team']} @ {game['home_team']} - {start_time.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            print(f"❌ NFL API error: {response.status_code}")
    except Exception as e:
        print(f"❌ NFL test failed: {e}")
    
    # Test NBA
    try:
        url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
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
            print(f"✅ NBA: Found {len(data)} games")
            for game in data[:3]:  # Show first 3 games
                start_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
                print(f"   📅 {game['away_team']} @ {game['home_team']} - {start_time.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            print(f"❌ NBA API error: {response.status_code}")
    except Exception as e:
        print(f"❌ NBA test failed: {e}")
    
    print()

def test_kalshi_realtime():
    """Test Kalshi API for real-time data."""
    print("🔍 Testing Kalshi API for Real-Time Data:")
    
    # Test without authentication first
    try:
        url = "https://api.elections.kalshi.com/markets"
        params = {'limit': 5}
        
        response = requests.get(url, params=params, timeout=10)
        print(f"📊 Kalshi Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            markets = data.get('markets', [])
            print(f"✅ Kalshi: Found {len(markets)} markets")
            for market in markets[:3]:
                print(f"   📊 {market.get('title', 'Unknown')} - Volume: {market.get('volume', 0)}")
        else:
            print(f"❌ Kalshi error: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Kalshi test failed: {e}")
    
    print()

def check_current_games():
    """Check what games are actually happening today."""
    print("🔍 Checking Current Games:")
    print(f"📅 Today's date: {datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    # MLB Season typically ends in October, playoffs in October
    print("📊 MLB Status: Post-season/Playoffs (October)")
    print("📊 NFL Status: Regular season (October)")
    print("📊 NBA Status: Pre-season (October)")
    print("📊 NHL Status: Regular season (October)")
    print()

if __name__ == "__main__":
    check_current_games()
    test_sportsbook_realtime()
    test_kalshi_realtime()
    
    print("💡 Analysis:")
    print("1. Check if the games shown are actually upcoming")
    print("2. Verify Kalshi has prediction markets for these games")
    print("3. Check if the pipeline is using real data or fixtures")
