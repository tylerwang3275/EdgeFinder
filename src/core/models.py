"""
Pydantic models for data structures.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Team(BaseModel):
    """Represents a sports team."""
    name: str
    city: str
    abbreviation: str
    sport: str


class Game(BaseModel):
    """Represents a sports game."""
    sport: str
    away_team: str
    home_team: str
    start_time: datetime
    game_id: Optional[str] = None


class KalshiMarket(BaseModel):
    """Represents a Kalshi prediction market."""
    market_id: str
    title: str
    event_time: datetime
    last_price: float = Field(ge=0.01, le=0.99)
    volume: int
    open_interest: Optional[int] = None
    market_side: str  # "YES" or "NO"
    outcome_description: str


class SportsbookOdds(BaseModel):
    """Represents sportsbook odds for a game."""
    game_id: str
    sport: str
    away_team: str
    home_team: str
    start_time: datetime
    book_name: str
    moneyline_away: Optional[int] = None
    moneyline_home: Optional[int] = None
    spread_away: Optional[float] = None
    spread_home: Optional[float] = None
    total_over: Optional[float] = None
    total_under: Optional[float] = None


class MatchedGame(BaseModel):
    """Represents a matched game between Kalshi and sportsbook data."""
    game: Game
    kalshi_market: KalshiMarket
    sportsbook_odds: List[SportsbookOdds]
    
    # Computed fields
    prediction_prob: float
    book_probs: List[float]
    min_book_prob: float
    avg_book_prob: float
    max_book_prob: float
    discrepancy_abs: float
    discrepancy_vs_best: float
    volume: int
    payout_ratio: float
    expected_value: float


class DiscrepancyRanking(BaseModel):
    """Represents a ranked discrepancy."""
    rank: int
    matched_game: MatchedGame
    discrepancy_score: float


class NewsletterSection(BaseModel):
    """Represents a section of the newsletter."""
    title: str
    description: str
    rankings: List[DiscrepancyRanking]


class NewsletterReport(BaseModel):
    """Represents the complete newsletter report."""
    generated_at: datetime
    timezone: str
    sections: List[NewsletterSection]
    seattle_pick: Optional[MatchedGame] = None
    total_games: int
    total_markets: int
    total_books: int


class Config(BaseModel):
    """Application configuration."""
    kalshi_base_url: str
    odds_api_base_url: str
    odds_api_key: str
    kalshi_api_key: str = ""
    kalshi_api_key_id: str = ""
    kalshi_private_key: str = ""
    timezone: str
    sports_filter: List[str]
    lookahead_hours: int
    min_volume: int
    top_n: int
    use_fixtures: bool
