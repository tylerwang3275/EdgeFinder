"""
Sportsbook odds API client.
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from src.core.models import SportsbookOdds, Config
from src.util.time import get_time_window


class OddsClient:
    """Client for sportsbook odds API (TheOddsAPI)."""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.odds_api_base_url
        self.api_key = config.odds_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EdgeFinder/1.0'
        })
    
    def get_odds(self, sports: Optional[List[str]] = None, lookahead_hours: Optional[int] = None) -> List[SportsbookOdds]:
        """
        Fetch odds from sportsbook API.
        
        Args:
            sports: List of sports to fetch (defaults to config)
            lookahead_hours: Hours to look ahead (defaults to config)
            
        Returns:
            List of SportsbookOdds objects
        """
        if self.config.use_fixtures:
            return self._get_fixture_odds()
        
        sports_list = sports or self.config.sports_filter
        hours = lookahead_hours or self.config.lookahead_hours
        
        all_odds = []
        
        for sport in sports_list:
            try:
                print(f"Fetching odds for sport: {sport}")
                odds = self._fetch_sport_odds(sport, hours)
                print(f"Successfully fetched {len(odds)} odds for {sport}")
                all_odds.extend(odds)
            except Exception as e:
                print(f"❌ Error fetching odds for {sport}: {e}")
                import traceback
                traceback.print_exc()
                # Continue with other sports, but log the error
                continue
        
        # If we got no odds at all, fall back to fixtures for demo
        if not all_odds and not self.config.use_fixtures:
            print("⚠️ No odds fetched from API, falling back to fixtures for demo")
            return self._get_fixture_odds()
        
        return all_odds
    
    def _fetch_sport_odds(self, sport: str, hours: int) -> List[SportsbookOdds]:
        """Fetch odds for a specific sport."""
        url = f"{self.base_url}/sports/{sport}/odds"
        params = {
            'apiKey': self.api_key,
            'regions': 'us',
            'markets': 'h2h,spreads,totals',
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        print(f"Making request to: {url}")
        print(f"With params: {params}")
        
        response = self.session.get(url, params=params, timeout=30)
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            print(f"   URL: {url}")
            print(f"   Params: {params}")
            raise Exception(f"API returned {response.status_code}: {response.text}")
        
        data = response.json()
        print(f"Received {len(data)} games for {sport}")
        odds_list = []
        
        for game_data in data:
            try:
                odds = self._parse_game_odds(game_data)
                if odds:
                    odds_list.append(odds)
            except Exception as e:
                print(f"Error parsing odds for game: {e}")
                continue
        
        return odds_list
    
    def _parse_game_odds(self, data: Dict[str, Any]) -> Optional[SportsbookOdds]:
        """Parse odds for a single game."""
        try:
            game_id = data.get('id', '')
            sport = data.get('sport_key', '')
            home_team = data.get('home_team', '')
            away_team = data.get('away_team', '')
            commence_time = data.get('commence_time', '')
            
            # Parse commence time
            commence_time_dt = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
            
            # Parse bookmaker odds
            bookmakers = data.get('bookmakers', [])
            odds_list = []
            
            for bookmaker in bookmakers:
                book_name = bookmaker.get('title', '')
                markets = bookmaker.get('markets', [])
                
                # Extract moneyline odds
                moneyline_away = None
                moneyline_home = None
                spread_away = None
                spread_home = None
                total_over = None
                total_under = None
                
                for market in markets:
                    if market.get('key') == 'h2h':
                        outcomes = market.get('outcomes', [])
                        for outcome in outcomes:
                            if outcome.get('name') == away_team:
                                moneyline_away = outcome.get('price')
                            elif outcome.get('name') == home_team:
                                moneyline_home = outcome.get('price')
                    
                    elif market.get('key') == 'spreads':
                        outcomes = market.get('outcomes', [])
                        for outcome in outcomes:
                            if outcome.get('name') == away_team:
                                spread_away = outcome.get('point')
                            elif outcome.get('name') == home_team:
                                spread_home = outcome.get('point')
                    
                    elif market.get('key') == 'totals':
                        outcomes = market.get('outcomes', [])
                        for outcome in outcomes:
                            if outcome.get('name') == 'Over':
                                total_over = outcome.get('point')
                            elif outcome.get('name') == 'Under':
                                total_under = outcome.get('point')
                
                if moneyline_away is not None or moneyline_home is not None:
                    odds = SportsbookOdds(
                        game_id=game_id,
                        sport=sport,
                        away_team=away_team,
                        home_team=home_team,
                        start_time=commence_time_dt,
                        book_name=book_name,
                        moneyline_away=moneyline_away,
                        moneyline_home=moneyline_home,
                        spread_away=spread_away,
                        spread_home=spread_home,
                        total_over=total_over,
                        total_under=total_under
                    )
                    odds_list.append(odds)
            
            return odds_list[0] if odds_list else None
            
        except (ValueError, KeyError) as e:
            print(f"Error parsing odds data: {e}")
            return None
    
    def _get_fixture_odds(self) -> List[SportsbookOdds]:
        """Get fixture odds for testing."""
        base_time = datetime.now() + timedelta(hours=24)
        
        return [
            SportsbookOdds(
                game_id="fixture_1",
                sport="americanfootball_nfl",
                away_team="Seattle Seahawks",
                home_team="San Francisco 49ers",
                start_time=base_time,
                book_name="DraftKings",
                moneyline_away=120,
                moneyline_home=-140,
                spread_away=2.5,
                spread_home=-2.5,
                total_over=45.5,
                total_under=45.5
            ),
            SportsbookOdds(
                game_id="fixture_1",
                sport="americanfootball_nfl",
                away_team="Seattle Seahawks",
                home_team="San Francisco 49ers",
                start_time=base_time,
                book_name="FanDuel",
                moneyline_away=115,
                moneyline_home=-135,
                spread_away=2.5,
                spread_home=-2.5,
                total_over=45.5,
                total_under=45.5
            ),
            SportsbookOdds(
                game_id="fixture_2",
                sport="basketball_nba",
                away_team="Los Angeles Lakers",
                home_team="Golden State Warriors",
                start_time=base_time + timedelta(hours=12),
                book_name="DraftKings",
                moneyline_away=-110,
                moneyline_home=-110,
                spread_away=-1.5,
                spread_home=1.5,
                total_over=220.5,
                total_under=220.5
            ),
            SportsbookOdds(
                game_id="fixture_3",
                sport="baseball_mlb",
                away_team="Seattle Mariners",
                home_team="Houston Astros",
                start_time=base_time - timedelta(hours=12),
                book_name="DraftKings",
                moneyline_away=150,
                moneyline_home=-180,
                spread_away=1.5,
                spread_home=-1.5,
                total_over=8.5,
                total_under=8.5
            ),
            SportsbookOdds(
                game_id="fixture_4",
                sport="icehockey_nhl",
                away_team="Seattle Kraken",
                home_team="Vancouver Canucks",
                start_time=base_time + timedelta(hours=24),
                book_name="DraftKings",
                moneyline_away=-105,
                moneyline_home=-115,
                spread_away=0.5,
                spread_home=-0.5,
                total_over=6.5,
                total_under=6.5
            ),
            SportsbookOdds(
                game_id="fixture_5",
                sport="americanfootball_ncaaf",
                away_team="Washington Huskies",
                home_team="Oregon Ducks",
                start_time=base_time + timedelta(hours=6),
                book_name="DraftKings",
                moneyline_away=130,
                moneyline_home=-150,
                spread_away=3.5,
                spread_home=-3.5,
                total_over=65.5,
                total_under=65.5
            )
        ]
