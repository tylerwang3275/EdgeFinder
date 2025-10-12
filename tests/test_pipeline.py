"""
Tests for the main pipeline.
"""

import pytest
from datetime import datetime, timedelta
from src.core.models import Config, KalshiMarket, SportsbookOdds, Game
from src.core.pipeline import EdgeFinderPipeline


class TestPipeline:
    """Test pipeline functionality."""
    
    @pytest.fixture
    def config(self):
        """Test configuration."""
        return Config(
            kalshi_base_url="https://api.kalshi.com",
            odds_api_base_url="https://api.theoddsapi.com/v4",
            odds_api_key="test_key",
            timezone="America/Los_Angeles",
            sports_filter=["nfl", "nba"],
            lookahead_hours=48,
            min_volume=100,
            top_n=5,
            use_fixtures=True
        )
    
    @pytest.fixture
    def sample_kalshi_markets(self):
        """Sample Kalshi markets for testing."""
        base_time = datetime.now() + timedelta(hours=24)
        
        return [
            KalshiMarket(
                market_id="test_1",
                title="Seattle Seahawks vs San Francisco 49ers",
                event_time=base_time,
                last_price=0.45,
                volume=1500,
                open_interest=5000,
                market_side="YES",
                outcome_description="Seahawks win"
            ),
            KalshiMarket(
                market_id="test_2",
                title="Los Angeles Lakers vs Golden State Warriors",
                event_time=base_time + timedelta(hours=12),
                last_price=0.62,
                volume=2000,
                open_interest=8000,
                market_side="YES",
                outcome_description="Lakers win"
            )
        ]
    
    @pytest.fixture
    def sample_sportsbook_odds(self):
        """Sample sportsbook odds for testing."""
        base_time = datetime.now() + timedelta(hours=24)
        
        return [
            SportsbookOdds(
                game_id="test_1",
                sport="americanfootball_nfl",
                away_team="Seattle Seahawks",
                home_team="San Francisco 49ers",
                start_time=base_time,
                book_name="DraftKings",
                moneyline_away=120,
                moneyline_home=-140
            ),
            SportsbookOdds(
                game_id="test_1",
                sport="americanfootball_nfl",
                away_team="Seattle Seahawks",
                home_team="San Francisco 49ers",
                start_time=base_time,
                book_name="FanDuel",
                moneyline_away=115,
                moneyline_home=-135
            ),
            SportsbookOdds(
                game_id="test_2",
                sport="basketball_nba",
                away_team="Los Angeles Lakers",
                home_team="Golden State Warriors",
                start_time=base_time + timedelta(hours=12),
                book_name="DraftKings",
                moneyline_away=-110,
                moneyline_home=-110
            )
        ]
    
    def test_pipeline_initialization(self, config):
        """Test pipeline initialization."""
        pipeline = EdgeFinderPipeline(config)
        assert pipeline.config == config
        assert pipeline.kalshi_client is not None
        assert pipeline.odds_client is not None
    
    def test_infer_sport_from_market(self, config):
        """Test sport inference from market."""
        pipeline = EdgeFinderPipeline(config)
        
        market_nfl = KalshiMarket(
            market_id="test",
            title="Seahawks vs 49ers",
            event_time=datetime.now(),
            last_price=0.5,
            volume=1000,
            market_side="YES",
            outcome_description="test"
        )
        
        market_nba = KalshiMarket(
            market_id="test",
            title="Lakers vs Warriors",
            event_time=datetime.now(),
            last_price=0.5,
            volume=1000,
            market_side="YES",
            outcome_description="test"
        )
        
        assert pipeline._infer_sport_from_market(market_nfl) == "americanfootball_nfl"
        assert pipeline._infer_sport_from_market(market_nba) == "basketball_nba"
    
    def test_find_matching_odds(self, config, sample_sportsbook_odds):
        """Test finding matching odds."""
        pipeline = EdgeFinderPipeline(config)
        
        game = Game(
            sport="americanfootball_nfl",
            away_team="Seattle Seahawks",
            home_team="San Francisco 49ers",
            start_time=datetime.now() + timedelta(hours=24)
        )
        
        odds_by_game = {}
        for odds in sample_sportsbook_odds:
            if odds.game_id not in odds_by_game:
                odds_by_game[odds.game_id] = []
            odds_by_game[odds.game_id].append(odds)
        
        matching_odds = pipeline._find_matching_odds(game, odds_by_game)
        
        assert len(matching_odds) == 1  # Only one odds entry in fixture
        assert all(odds.sport == "americanfootball_nfl" for odds in matching_odds)
    
    def test_process_match(self, config, sample_kalshi_markets, sample_sportsbook_odds):
        """Test processing a match."""
        pipeline = EdgeFinderPipeline(config)
        
        game = Game(
            sport="americanfootball_nfl",
            away_team="Seattle Seahawks",
            home_team="San Francisco 49ers",
            start_time=datetime.now() + timedelta(hours=24)
        )
        
        market = sample_kalshi_markets[0]
        odds_list = [odds for odds in sample_sportsbook_odds if odds.game_id == "test_1"]
        
        matched_game = pipeline._process_match(game, market, odds_list)
        
        assert matched_game is not None
        assert matched_game.prediction_prob == 0.45
        assert matched_game.volume == 1500
        assert len(matched_game.book_probs) > 0
        assert matched_game.discrepancy_abs >= 0
    
    def test_generate_rankings(self, config):
        """Test ranking generation."""
        pipeline = EdgeFinderPipeline(config)
        
        # Create mock matched games
        matched_games = []
        for i in range(3):
            game = Game(
                sport="nfl",
                away_team=f"Team{i}A",
                home_team=f"Team{i}B",
                start_time=datetime.now()
            )
            
            market = KalshiMarket(
                market_id=f"market_{i}",
                title=f"Game {i}",
                event_time=datetime.now(),
                last_price=0.5,
                volume=1000 + i * 100,
                market_side="YES",
                outcome_description="test"
            )
            
            # Mock matched game
            from src.core.models import MatchedGame
            matched_game = MatchedGame(
                game=game,
                kalshi_market=market,
                sportsbook_odds=[],
                prediction_prob=0.5,
                book_probs=[0.4, 0.6],
                min_book_prob=0.4,
                avg_book_prob=0.5,
                max_book_prob=0.6,
                discrepancy_abs=0.1 + i * 0.05,
                discrepancy_vs_best=0.05,
                volume=1000 + i * 100,
                payout_ratio=1.0,
                expected_value=0.0
            )
            matched_games.append(matched_game)
        
        rankings = pipeline._generate_rankings(matched_games)
        
        assert len(rankings) == 3
        assert rankings[0].rank == 1
        assert rankings[0].discrepancy_score >= rankings[1].discrepancy_score
        assert rankings[1].discrepancy_score >= rankings[2].discrepancy_score
