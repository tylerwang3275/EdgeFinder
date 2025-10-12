"""
Robinhood prediction market client.
Since Robinhood uses Kalshi as the exchange, we'll simulate Robinhood prediction market data
based on sportsbook odds with some market inefficiencies.
"""

import random
from typing import List, Optional, Dict, Any
from src.core.models import KalshiMarket, Config
from src.data.odds_client import OddsClient


class RobinhoodClient:
    """Client for Robinhood prediction markets (via Kalshi)."""
    
    def __init__(self, config: Config):
        self.config = config
        self.odds_client = OddsClient(config)
    
    def get_prediction_markets(self, lookahead_hours: Optional[int] = None) -> List[KalshiMarket]:
        """
        Get Robinhood prediction markets for sports events.
        
        Since we can't access Kalshi's sports markets directly, we'll simulate
        Robinhood prediction market data based on sportsbook odds with some
        market inefficiencies that create opportunities.
        """
        if self.config.use_fixtures:
            return self._get_fixture_markets()
        
        # Get real sportsbook odds
        sportsbook_odds = self.odds_client.get_odds()
        
        # Convert sportsbook odds to Robinhood prediction markets
        prediction_markets = []
        
        for odds in sportsbook_odds:
            # Create prediction markets for each team
            markets = self._create_prediction_markets_from_odds(odds)
            prediction_markets.extend(markets)
        
        return prediction_markets
    
    def _create_prediction_markets_from_odds(self, odds) -> List[KalshiMarket]:
        """Create Robinhood prediction markets from sportsbook odds."""
        markets = []
        
        # Calculate implied probabilities from sportsbook odds
        home_prob = self._american_to_probability(odds.moneyline_home)
        away_prob = self._american_to_probability(odds.moneyline_away)
        
        # Add some market inefficiencies to simulate Robinhood prediction markets
        # Robinhood markets often have different pricing due to:
        # 1. Different user base (retail vs professional)
        # 2. Market timing differences
        # 3. Information asymmetry
        
        # Simulate Robinhood market inefficiencies
        home_robinhood_prob = self._add_market_inefficiency(home_prob)
        away_robinhood_prob = self._add_market_inefficiency(away_prob)
        
        # Create prediction markets for each team winning
        home_market = KalshiMarket(
            id=f"robinhood-{odds.game_id}-home-win",
            title=f"Will {odds.home_team} beat {odds.away_team}?",
            description=f"Prediction market for {odds.home_team} vs {odds.away_team}",
            yes_price=home_robinhood_prob,
            no_price=1.0 - home_robinhood_prob,
            volume=random.randint(500, 5000),  # Simulate volume
            status="open",
            close_time=odds.start_time,
            sport=odds.sport,
            home_team=odds.home_team,
            away_team=odds.away_team,
            start_time=odds.start_time
        )
        
        away_market = KalshiMarket(
            id=f"robinhood-{odds.game_id}-away-win",
            title=f"Will {odds.away_team} beat {odds.home_team}?",
            description=f"Prediction market for {odds.away_team} vs {odds.home_team}",
            yes_price=away_robinhood_prob,
            no_price=1.0 - away_robinhood_prob,
            volume=random.randint(500, 5000),  # Simulate volume
            status="open",
            close_time=odds.start_time,
            sport=odds.sport,
            home_team=odds.home_team,
            away_team=odds.away_team,
            start_time=odds.start_time
        )
        
        markets.extend([home_market, away_market])
        
        return markets
    
    def _american_to_probability(self, american_odds: int) -> float:
        """Convert American odds to probability."""
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)
    
    def _add_market_inefficiency(self, true_prob: float) -> float:
        """
        Add market inefficiency to simulate Robinhood prediction markets.
        
        Robinhood markets often have different pricing due to:
        - Retail investor behavior
        - Market timing differences
        - Information asymmetry
        - Different risk preferences
        """
        # Add random inefficiency between -10% and +10%
        inefficiency = random.uniform(-0.1, 0.1)
        adjusted_prob = true_prob + inefficiency
        
        # Ensure probability stays between 0.01 and 0.99
        return max(0.01, min(0.99, adjusted_prob))
    
    def _get_fixture_markets(self) -> List[KalshiMarket]:
        """Get fixture prediction markets for testing."""
        from datetime import datetime, timedelta
        import pytz
        
        tz = pytz.timezone(self.config.timezone)
        now = datetime.now(tz)
        
        # Create some realistic fixture markets
        fixtures = [
            {
                "home_team": "Seattle Seahawks",
                "away_team": "Jacksonville Jaguars",
                "sport": "americanfootball_nfl",
                "start_time": now + timedelta(hours=2),
                "home_robinhood_prob": 0.45,  # Slightly different from sportsbooks
                "away_robinhood_prob": 0.55,
                "volume": 2500
            },
            {
                "home_team": "Seattle Mariners",
                "away_team": "Toronto Blue Jays",
                "sport": "baseball_mlb",
                "start_time": now + timedelta(hours=12),
                "home_robinhood_prob": 0.38,
                "away_robinhood_prob": 0.62,
                "volume": 1800
            },
            {
                "home_team": "Los Angeles Lakers",
                "away_team": "Denver Nuggets",
                "sport": "basketball_nba",
                "start_time": now + timedelta(hours=24),
                "home_robinhood_prob": 0.65,  # Different from sportsbooks
                "away_robinhood_prob": 0.35,
                "volume": 3200
            }
        ]
        
        markets = []
        for fixture in fixtures:
            # Home team market
            home_market = KalshiMarket(
                id=f"robinhood-fixture-{fixture['home_team'].lower().replace(' ', '-')}-win",
                title=f"Will {fixture['home_team']} beat {fixture['away_team']}?",
                description=f"Robinhood prediction market for {fixture['home_team']} vs {fixture['away_team']}",
                yes_price=fixture['home_robinhood_prob'],
                no_price=1.0 - fixture['home_robinhood_prob'],
                volume=fixture['volume'],
                status="open",
                close_time=fixture['start_time'],
                sport=fixture['sport'],
                home_team=fixture['home_team'],
                away_team=fixture['away_team'],
                start_time=fixture['start_time']
            )
            
            # Away team market
            away_market = KalshiMarket(
                id=f"robinhood-fixture-{fixture['away_team'].lower().replace(' ', '-')}-win",
                title=f"Will {fixture['away_team']} beat {fixture['home_team']}?",
                description=f"Robinhood prediction market for {fixture['away_team']} vs {fixture['home_team']}",
                yes_price=fixture['away_robinhood_prob'],
                no_price=1.0 - fixture['away_robinhood_prob'],
                volume=fixture['volume'],
                status="open",
                close_time=fixture['start_time'],
                sport=fixture['sport'],
                home_team=fixture['home_team'],
                away_team=fixture['away_team'],
                start_time=fixture['start_time']
            )
            
            markets.extend([home_market, away_market])
        
        return markets
