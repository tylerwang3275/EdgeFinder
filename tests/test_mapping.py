"""
Tests for team mapping utilities.
"""

import pytest
from datetime import datetime, timedelta
from src.data.mapping import (
    normalize_team_name,
    find_team_match,
    is_seattle_team,
    extract_teams_from_kalshi_title,
    create_game_from_market,
    match_games_within_timeframe
)


class TestTeamMapping:
    """Test team mapping functions."""
    
    def test_normalize_team_name(self):
        """Test team name normalization."""
        # Basic normalization
        assert normalize_team_name("Seattle Seahawks", "nfl") == "seattle seahawks"
        assert normalize_team_name("  Los Angeles Lakers  ", "nba") == "los angeles lakers"
        
        # Remove suffixes
        assert normalize_team_name("Seattle Seahawks Football", "nfl") == "seattle seahawks"
        assert normalize_team_name("Lakers Basketball", "nba") == "lakers"
    
    def test_find_team_match(self):
        """Test team matching."""
        # Seattle teams
        assert find_team_match("Seattle Seahawks", "americanfootball_nfl") == "seahawks"
        assert find_team_match("Seahawks", "americanfootball_nfl") == "seahawks"
        assert find_team_match("SEA", "americanfootball_nfl") == "seahawks"
        
        # Other teams
        assert find_team_match("New England Patriots", "americanfootball_nfl") == "patriots"
        assert find_team_match("Patriots", "americanfootball_nfl") == "patriots"
        assert find_team_match("NE", "americanfootball_nfl") == "patriots"
        
        # No match
        assert find_team_match("Random Team Name", "americanfootball_nfl") is None
    
    def test_is_seattle_team(self):
        """Test Seattle team identification."""
        # Seattle teams
        assert is_seattle_team("Seattle Seahawks", "americanfootball_nfl") is True
        assert is_seattle_team("Seahawks", "americanfootball_nfl") is True
        assert is_seattle_team("SEA", "americanfootball_nfl") is True
        
        # Non-Seattle teams
        assert is_seattle_team("New England Patriots", "americanfootball_nfl") is False
        assert is_seattle_team("Patriots", "americanfootball_nfl") is False
    
    def test_extract_teams_from_kalshi_title(self):
        """Test team extraction from Kalshi titles."""
        # Standard vs format
        teams = extract_teams_from_kalshi_title("Seattle Seahawks vs San Francisco 49ers", "americanfootball_nfl")
        assert teams == ("seahawks", "49ers")
        
        # @ format
        teams = extract_teams_from_kalshi_title("Lakers @ Warriors", "basketball_nba")
        assert teams == ("lakers", "warriors")
        
        # No match
        teams = extract_teams_from_kalshi_title("Random Market Title", "americanfootball_nfl")
        assert teams is None
    
    def test_create_game_from_market(self):
        """Test game creation from market."""
        market_title = "Seattle Seahawks vs San Francisco 49ers"
        event_time = datetime.now() + timedelta(hours=24)
        
        game = create_game_from_market(market_title, event_time, "americanfootball_nfl")
        
        assert game is not None
        assert game.sport == "americanfootball_nfl"
        assert game.away_team == "seahawks"
        assert game.home_team == "49ers"
        assert game.start_time == event_time
    
    def test_match_games_within_timeframe(self):
        """Test game matching within timeframe."""
        base_time = datetime.now() + timedelta(hours=24)
        
        kalshi_games = [
            create_game_from_market("Seahawks vs 49ers", base_time, "americanfootball_nfl"),
            create_game_from_market("Lakers vs Warriors", base_time + timedelta(hours=1), "basketball_nba")
        ]
        
        sportsbook_games = [
            create_game_from_market("Seahawks vs 49ers", base_time + timedelta(minutes=30), "americanfootball_nfl"),
            create_game_from_market("Lakers vs Warriors", base_time + timedelta(hours=2), "basketball_nba")
        ]
        
        matches = match_games_within_timeframe(kalshi_games, sportsbook_games, 2)
        
        assert len(matches) == 2
        assert matches[0][0].sport == "americanfootball_nfl"
        assert matches[1][0].sport == "basketball_nba"
