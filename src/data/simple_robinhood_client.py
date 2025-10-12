"""
Simple Robinhood prediction market client for demonstration.
This creates realistic prediction market data based on sportsbook odds.
"""

import random
from typing import List, Optional
from src.core.models import KalshiMarket, Config
from src.data.odds_client import OddsClient


class SimpleRobinhoodClient:
    """Simple client for Robinhood prediction markets."""
    
    def __init__(self, config: Config):
        self.config = config
        self.odds_client = OddsClient(config)
    
    def get_prediction_markets(self, lookahead_hours: Optional[int] = None) -> List[KalshiMarket]:
        """Get Robinhood prediction markets for sports events."""
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
        home_robinhood_prob = self._add_market_inefficiency(home_prob)
        away_robinhood_prob = self._add_market_inefficiency(away_prob)
        
        # Create prediction markets for each team winning
        home_market = KalshiMarket(
            market_id=f"robinhood-{odds.game_id}-home-win",
            title=f"Will {odds.home_team} beat {odds.away_team}?",
            event_time=odds.start_time,
            last_price=home_robinhood_prob,
            volume=random.randint(500, 5000),
            market_side="YES",
            outcome_description=f"{odds.home_team} wins"
        )
        
        away_market = KalshiMarket(
            market_id=f"robinhood-{odds.game_id}-away-win",
            title=f"Will {odds.away_team} beat {odds.home_team}?",
            event_time=odds.start_time,
            last_price=away_robinhood_prob,
            volume=random.randint(500, 5000),
            market_side="YES",
            outcome_description=f"{odds.away_team} wins"
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
        """Add market inefficiency to simulate Robinhood prediction markets."""
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
                "home_robinhood_prob": 0.45,
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
            }
        ]
        
        markets = []
        for fixture in fixtures:
            # Home team market
            home_market = KalshiMarket(
                market_id=f"robinhood-fixture-{fixture['home_team'].lower().replace(' ', '-')}-win",
                title=f"Will {fixture['home_team']} beat {fixture['away_team']}?",
                event_time=fixture['start_time'],
                last_price=fixture['home_robinhood_prob'],
                volume=fixture['volume'],
                market_side="YES",
                outcome_description=f"{fixture['home_team']} wins"
            )
            
            # Away team market
            away_market = KalshiMarket(
                market_id=f"robinhood-fixture-{fixture['away_team'].lower().replace(' ', '-')}-win",
                title=f"Will {fixture['away_team']} beat {fixture['home_team']}?",
                event_time=fixture['start_time'],
                last_price=fixture['away_robinhood_prob'],
                volume=fixture['volume'],
                market_side="YES",
                outcome_description=f"{fixture['away_team']} wins"
            )
            
            markets.extend([home_market, away_market])
        
        return markets
