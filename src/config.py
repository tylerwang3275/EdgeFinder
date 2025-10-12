"""
Configuration management for EdgeFinder.
"""

import os
from typing import List
from dotenv import load_dotenv
from src.core.models import Config

# Load environment variables
load_dotenv()


def load_config() -> Config:
    """Load configuration from environment variables."""
    return Config(
        kalshi_base_url=os.getenv("KALSHI_BASE_URL", "https://api.elections.kalshi.com"),
        odds_api_base_url=os.getenv("ODDS_API_BASE_URL", "https://api.the-odds-api.com/v4").replace("api.theoddsapi.com", "api.the-odds-api.com"),
        odds_api_key=os.getenv("ODDS_API_KEY", ""),
        kalshi_api_key=os.getenv("KALSHI_API_KEY", ""),
        kalshi_api_key_id=os.getenv("KALSHI_API_KEY_ID", ""),
        kalshi_private_key=os.getenv("KALSHI_PRIVATE_KEY", ""),
        timezone=os.getenv("EDGEFINDER_TIMEZONE", "America/Los_Angeles"),
        sports_filter=os.getenv("SPORTS_FILTER", "baseball_mlb,americanfootball_nfl,basketball_nba,icehockey_nhl,soccer_epl").replace("SPORTS_FILTER = ", "").replace("SPORTS_FILTER=", "").split(","),
        lookahead_hours=int(os.getenv("LOOKAHEAD_HOURS", "48")),
        min_volume=int(os.getenv("MIN_VOLUME", "100")),
        top_n=int(os.getenv("TOP_N", "10")),
        use_fixtures=os.getenv("USE_FIXTURES", "false").lower() == "true",
    )
