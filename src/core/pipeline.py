"""
Main pipeline for processing prediction market and sportsbook data.
"""

from datetime import datetime
from typing import List, Optional, Tuple
from src.core.models import (
    Config, KalshiMarket, SportsbookOdds, MatchedGame, 
    DiscrepancyRanking, NewsletterReport, NewsletterSection, Game
)
from src.core.odds_math import (
    american_to_implied_probability, calculate_discrepancy,
    calculate_edge_vs_best, calculate_payout_ratio, calculate_expected_value
)
from src.data.simple_robinhood_client import SimpleRobinhoodClient
from src.data.odds_client import OddsClient
from src.data.mapping import (
    create_game_from_market, match_games_within_timeframe,
    is_seattle_team, find_team_match
)
from src.util.log import get_logger


class EdgeFinderPipeline:
    """Main pipeline for processing and comparing prediction markets vs sportsbooks."""
    
    def __init__(self, config: Config):
        self.config = config
        self.robinhood_client = SimpleRobinhoodClient(config)
        self.odds_client = OddsClient(config)
        self.logger = get_logger()
    
    def run(self) -> NewsletterReport:
        """
        Run the complete pipeline.
        
        Returns:
            NewsletterReport with all processed data
        """
        self.logger.info("Starting EdgeFinder pipeline")
        
        # Fetch data
        robinhood_markets = self.robinhood_client.get_prediction_markets()
        sportsbook_odds = self.odds_client.get_odds()
        
        self.logger.info(f"Fetched {len(robinhood_markets)} Robinhood prediction markets and {len(sportsbook_odds)} sportsbook odds")
        
        # Process and match data
        matched_games = self._match_and_process_data(robinhood_markets, sportsbook_odds)
        
        self.logger.info(f"Matched {len(matched_games)} games")
        
        # Generate rankings
        rankings = self._generate_rankings(matched_games)
        
        # Find Seattle pick
        seattle_pick = self._find_seattle_pick(matched_games)
        
        # Create report
        report = NewsletterReport(
            generated_at=datetime.utcnow(),
            timezone=self.config.timezone,
            sections=self._create_sections(rankings),
            seattle_pick=seattle_pick,
            total_games=len(matched_games),
            total_markets=len(robinhood_markets),
            total_books=len(sportsbook_odds)
        )
        
        self.logger.info("Pipeline completed successfully")
        return report
    
    def _match_and_process_data(
        self, 
        robinhood_markets: List[KalshiMarket], 
        sportsbook_odds: List[SportsbookOdds]
    ) -> List[MatchedGame]:
        """Match Robinhood prediction markets with sportsbook odds and process."""
        matched_games = []
        
        # Group sportsbook odds by game
        odds_by_game = {}
        for odds in sportsbook_odds:
            if odds.game_id not in odds_by_game:
                odds_by_game[odds.game_id] = []
            odds_by_game[odds.game_id].append(odds)
        
        # Process each Robinhood prediction market
        for market in robinhood_markets:
            try:
                # Create game from market
                sport = self._infer_sport_from_market(market)
                self.logger.info(f"Processing market: {market.title}, inferred sport: {sport}")
                
                game = create_game_from_market(
                    market.title, 
                    market.event_time, 
                    sport
                )
                
                if not game:
                    self.logger.warning(f"Could not create game from market: {market.title}")
                    continue
                
                self.logger.info(f"Created game: {game.away_team} @ {game.home_team} ({game.sport})")
                
                # Find matching sportsbook odds
                matching_odds = self._find_matching_odds(game, odds_by_game)
                
                if not matching_odds:
                    self.logger.warning(f"No matching odds found for game: {game.away_team} @ {game.home_team}")
                    continue
                
                self.logger.info(f"Found {len(matching_odds)} matching odds")
                
                # Process the match
                matched_game = self._process_match(game, market, matching_odds)
                if matched_game:
                    matched_games.append(matched_game)
                    
            except Exception as e:
                self.logger.warning(f"Error processing market {market.market_id}: {e}")
                continue
        
        return matched_games
    
    def _infer_sport_from_market(self, market: KalshiMarket) -> str:
        """Infer sport from market title."""
        title_lower = market.title.lower()
        
        if any(word in title_lower for word in ['seahawks', '49ers', 'nfl', 'football']):
            return 'americanfootball_nfl'
        elif any(word in title_lower for word in ['mariners', 'astros', 'mlb', 'baseball']):
            return 'baseball_mlb'
        elif any(word in title_lower for word in ['lakers', 'warriors', 'nba', 'basketball']):
            return 'basketball_nba'
        elif any(word in title_lower for word in ['kraken', 'canucks', 'nhl', 'hockey']):
            return 'icehockey_nhl'
        elif any(word in title_lower for word in ['huskies', 'ducks', 'ncaa', 'college']):
            return 'americanfootball_ncaaf'
        else:
            return 'unknown'
    
    def _find_matching_odds(self, game: Game, odds_by_game: dict) -> List[SportsbookOdds]:
        """Find matching sportsbook odds for a game."""
        matching_odds = []
        
        for game_id, odds_list in odds_by_game.items():
            for odds in odds_list:
                # Check if sport matches
                if odds.sport != game.sport:
                    continue
                
                # Check if teams match using flexible matching
                away_match = (find_team_match(odds.away_team, game.sport) == game.away_team or
                             find_team_match(game.away_team, game.sport) == find_team_match(odds.away_team, game.sport))
                home_match = (find_team_match(odds.home_team, game.sport) == game.home_team or
                             find_team_match(game.home_team, game.sport) == find_team_match(odds.home_team, game.sport))
                
                # Check both directions (away/home and home/away)
                if ((away_match and home_match) or
                    (find_team_match(odds.away_team, game.sport) == game.home_team and
                     find_team_match(odds.home_team, game.sport) == game.away_team)):
                    matching_odds.append(odds)
                    break
        
        return matching_odds
    
    def _process_match(
        self, 
        game: Game, 
        market: KalshiMarket, 
        odds_list: List[SportsbookOdds]
    ) -> Optional[MatchedGame]:
        """Process a matched game and calculate discrepancies."""
        try:
            # Get prediction probability from Kalshi
            prediction_prob = market.last_price
            
            # Convert sportsbook odds to probabilities
            book_probs = []
            for odds in odds_list:
                if odds.moneyline_away is not None:
                    prob_away = american_to_implied_probability(odds.moneyline_away)
                    book_probs.append(prob_away)
                if odds.moneyline_home is not None:
                    prob_home = american_to_implied_probability(odds.moneyline_home)
                    book_probs.append(prob_home)
            
            if not book_probs:
                return None
            
            # Calculate statistics
            min_book_prob = min(book_probs)
            max_book_prob = max(book_probs)
            avg_book_prob = sum(book_probs) / len(book_probs)
            
            # Calculate discrepancies
            discrepancy_abs = calculate_discrepancy(prediction_prob, avg_book_prob)
            discrepancy_vs_best = prediction_prob - min_book_prob
            
            # Calculate payout ratio
            payout_ratio = calculate_payout_ratio(prediction_prob)
            
            # Calculate expected value
            expected_value = calculate_expected_value(prediction_prob, avg_book_prob)
            
            return MatchedGame(
                game=game,
                kalshi_market=market,  # This is actually a Robinhood market now
                sportsbook_odds=odds_list,
                prediction_prob=prediction_prob,
                book_probs=book_probs,
                min_book_prob=min_book_prob,
                avg_book_prob=avg_book_prob,
                max_book_prob=max_book_prob,
                discrepancy_abs=discrepancy_abs,
                discrepancy_vs_best=discrepancy_vs_best,
                volume=market.volume,
                payout_ratio=payout_ratio,
                expected_value=expected_value
            )
            
        except Exception as e:
            self.logger.warning(f"Error processing match: {e}")
            return None
    
    def _generate_rankings(self, matched_games: List[MatchedGame]) -> List[DiscrepancyRanking]:
        """Generate rankings from matched games."""
        rankings = []
        
        for i, game in enumerate(matched_games):
            ranking = DiscrepancyRanking(
                rank=i + 1,
                matched_game=game,
                discrepancy_score=game.discrepancy_abs
            )
            rankings.append(ranking)
        
        # Sort by discrepancy (descending)
        rankings.sort(key=lambda x: x.discrepancy_score, reverse=True)
        
        # Update ranks
        for i, ranking in enumerate(rankings):
            ranking.rank = i + 1
        
        return rankings
    
    def _find_seattle_pick(self, matched_games: List[MatchedGame]) -> Optional[MatchedGame]:
        """Find the best Seattle team pick."""
        seattle_games = []
        
        for game in matched_games:
            if (is_seattle_team(game.game.away_team, game.game.sport) or
                is_seattle_team(game.game.home_team, game.game.sport)):
                seattle_games.append(game)
        
        if not seattle_games:
            return None
        
        # Return the one with highest volume or biggest discrepancy
        return max(seattle_games, key=lambda g: g.volume * g.discrepancy_abs)
    
    def _create_sections(self, rankings: List[DiscrepancyRanking]) -> List[NewsletterSection]:
        """Create newsletter sections."""
        sections = []
        
        # Best Robinhood Opportunities
        biggest_discrepancies = rankings[:self.config.top_n]
        sections.append(NewsletterSection(
            title='Best Robinhood Opportunities',
            description='Games where Robinhood prediction markets differ most from sportsbooks',
            rankings=biggest_discrepancies
        ))
        
        # Most Popular on Robinhood
        volume_rankings = sorted(rankings, key=lambda x: x.matched_game.volume, reverse=True)
        most_bet = volume_rankings[:self.config.top_n]
        sections.append(NewsletterSection(
            title='Most Popular on Robinhood',
            description='Games with the highest Robinhood prediction market volume',
            rankings=most_bet
        ))
        
        # Highest Payout Potential on Robinhood
        payout_rankings = [
            r for r in rankings 
            if r.matched_game.payout_ratio >= 2.0  # Lower threshold for more opportunities
        ]
        payout_rankings.sort(key=lambda x: x.matched_game.volume, reverse=True)
        highest_payout = payout_rankings[:self.config.top_n]
        sections.append(NewsletterSection(
            title='Highest Payout Potential on Robinhood',
            description='Robinhood prediction markets with the best payout ratios',
            rankings=highest_payout
        ))
        
        return sections
