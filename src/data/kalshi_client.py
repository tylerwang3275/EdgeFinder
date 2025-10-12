"""
Kalshi API client for prediction market data.
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from src.core.models import KalshiMarket, Config
from src.util.time import get_time_window


class KalshiClient:
    """Client for Kalshi prediction market API."""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.kalshi_base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'EdgeFinder/1.0'
        })
        
        # Add authentication if available
        self.api_key = getattr(config, 'kalshi_api_key', None)
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def get_markets(self, lookahead_hours: Optional[int] = None) -> List[KalshiMarket]:
        """
        Fetch prediction markets from Kalshi.
        
        Args:
            lookahead_hours: Hours to look ahead (defaults to config)
            
        Returns:
            List of KalshiMarket objects
        """
        if self.config.use_fixtures:
            return self._get_fixture_markets()
        
        hours = lookahead_hours or self.config.lookahead_hours
        start_time, end_time = get_time_window(hours)
        
        try:
            # Kalshi API endpoint for markets
            url = f"{self.base_url}/markets"
            params = {
                'status': 'open',
                'limit': 1000,  # Adjust based on API limits
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat()
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            markets = []
            
            for market_data in data.get('markets', []):
                try:
                    market = self._parse_market(market_data)
                    if market and market.volume >= self.config.min_volume:
                        markets.append(market)
                except Exception as e:
                    print(f"Error parsing market {market_data.get('id', 'unknown')}: {e}")
                    continue
            
            return markets
            
        except requests.RequestException as e:
            print(f"Error fetching Kalshi markets: {e}")
            # If API fails, fall back to fixtures for demo
            print("Falling back to fixture data for demo purposes")
            return self._get_fixture_markets()
    
    def _parse_market(self, data: Dict[str, Any]) -> Optional[KalshiMarket]:
        """Parse a single market from Kalshi API response."""
        try:
            market_id = data.get('id', '')
            title = data.get('title', '')
            event_time_str = data.get('event_time', '')
            last_price = float(data.get('last_price', 0))
            volume = int(data.get('volume', 0))
            open_interest = data.get('open_interest')
            market_side = data.get('market_side', 'YES')
            outcome_description = data.get('outcome_description', '')
            
            # Parse event time
            event_time = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
            
            return KalshiMarket(
                market_id=market_id,
                title=title,
                event_time=event_time,
                last_price=last_price,
                volume=volume,
                open_interest=open_interest,
                market_side=market_side,
                outcome_description=outcome_description
            )
            
        except (ValueError, KeyError) as e:
            print(f"Error parsing market data: {e}")
            return None
    
    def _get_fixture_markets(self) -> List[KalshiMarket]:
        """Get fixture markets for testing."""
        return [
            KalshiMarket(
                market_id="fixture_1",
                title="Seattle Seahawks vs San Francisco 49ers",
                event_time=datetime.now() + timedelta(hours=24),
                last_price=0.45,
                volume=1500,
                open_interest=5000,
                market_side="YES",
                outcome_description="Seahawks win"
            ),
            KalshiMarket(
                market_id="fixture_2",
                title="Los Angeles Lakers vs Golden State Warriors",
                event_time=datetime.now() + timedelta(hours=36),
                last_price=0.62,
                volume=2000,
                open_interest=8000,
                market_side="YES",
                outcome_description="Lakers win"
            ),
            KalshiMarket(
                market_id="fixture_3",
                title="Seattle Mariners vs Houston Astros",
                event_time=datetime.now() + timedelta(hours=12),
                last_price=0.38,
                volume=800,
                open_interest=3000,
                market_side="YES",
                outcome_description="Mariners win"
            ),
            KalshiMarket(
                market_id="fixture_4",
                title="Seattle Kraken vs Vancouver Canucks",
                event_time=datetime.now() + timedelta(hours=48),
                last_price=0.55,
                volume=1200,
                open_interest=4500,
                market_side="YES",
                outcome_description="Kraken win"
            ),
            KalshiMarket(
                market_id="fixture_5",
                title="Washington Huskies vs Oregon Ducks",
                event_time=datetime.now() + timedelta(hours=30),
                last_price=0.42,
                volume=3000,
                open_interest=12000,
                market_side="YES",
                outcome_description="Huskies win"
            )
        ]
