"""
Newsletter generation utilities.
"""

import csv
from datetime import datetime
from typing import List, Optional
from src.core.models import NewsletterReport, DiscrepancyRanking, MatchedGame
from src.util.time import format_time_for_display


class NewsletterRenderer:
    """Renders newsletter reports to Markdown and CSV."""
    
    def __init__(self, timezone: str = "America/Los_Angeles"):
        self.timezone = timezone
    
    def render_markdown(self, report: NewsletterReport) -> str:
        """Render newsletter report to Markdown."""
        content = []
        
        # Header
        content.append("# EdgeFinder: Robinhood vs Sportsbooks")
        content.append("")
        content.append(f"**Generated:** {format_time_for_display(report.generated_at, self.timezone)}")
        content.append(f"**Timezone:** {report.timezone}")
        content.append("")
        content.append(f"**Summary:** {report.total_games} matched games, {report.total_markets} Robinhood markets, {report.total_books} sportsbook odds")
        content.append("")
        
        # Sections
        for section in report.sections:
            content.append(f"## {section.title}")
            content.append("")
            content.append(section.description)
            content.append("")
            
            if section.rankings:
                content.append(self._render_rankings_table(section.rankings))
            else:
                content.append("*No data available*")
            
            content.append("")
        
        # Seattle Pick
        if report.seattle_pick:
            content.append("## 🏠 Hometown Favorite: Seattle")
            content.append("")
            content.append(self._render_seattle_pick(report.seattle_pick))
            content.append("")
        
        # Footer
        content.append("---")
        content.append("")
        content.append("*EdgeFinder analyzes discrepancies between Robinhood prediction markets and sportsbooks to identify the best betting opportunities on Robinhood.*")
        content.append("")
        content.append("**Disclaimer:** This is for informational purposes only. Sports betting involves risk.")
        
        return "\n".join(content)
    
    def _render_rankings_table(self, rankings: List[DiscrepancyRanking]) -> str:
        """Render rankings as a Markdown table."""
        if not rankings:
            return "*No rankings available*"
        
        # Table header
        table = [
            "| Rank | Sport | Game | Start Time | Pred Prob | Books (min/avg/max) | Discrepancy | Volume | Payout |",
            "|------|-------|------|-------------|-----------|---------------------|-------------|--------|--------|"
        ]
        
        # Table rows
        for ranking in rankings:
            game = ranking.matched_game
            start_time = format_time_for_display(game.game.start_time, self.timezone)
            
            # Format game description
            game_desc = f"{game.game.away_team} @ {game.game.home_team}"
            
            # Format book probabilities
            book_probs = f"{game.min_book_prob:.3f}/{game.avg_book_prob:.3f}/{game.max_book_prob:.3f}"
            
            # Format values
            pred_prob = f"{game.prediction_prob:.3f}"
            discrepancy = f"{game.discrepancy_abs:.3f}"
            volume = f"{game.volume:,}"
            payout = f"{game.payout_ratio:.1f}x"
            
            row = f"| {ranking.rank} | {game.game.sport.upper()} | {game_desc} | {start_time} | {pred_prob} | {book_probs} | {discrepancy} | {volume} | {payout} |"
            table.append(row)
        
        return "\n".join(table)
    
    def _render_seattle_pick(self, seattle_pick: MatchedGame) -> str:
        """Render Seattle pick section."""
        game = seattle_pick.game
        start_time = format_time_for_display(game.start_time, self.timezone)
        
        content = []
        content.append(f"**{game.away_team} @ {game.home_team}**")
        content.append(f"*{start_time}*")
        content.append("")
        content.append(f"- **Prediction Market:** {seattle_pick.prediction_prob:.1%}")
        content.append(f"- **Sportsbook Average:** {seattle_pick.avg_book_prob:.1%}")
        content.append(f"- **Discrepancy:** {seattle_pick.discrepancy_abs:.1%}")
        content.append(f"- **Market Volume:** {seattle_pick.volume:,}")
        content.append(f"- **Payout Ratio:** {seattle_pick.payout_ratio:.1f}x")
        content.append("")
        
        if seattle_pick.discrepancy_vs_best > 0:
            content.append("🎯 **Edge Alert:** Prediction market is more bullish than the best available sportsbook odds!")
        else:
            content.append("📊 **Market View:** Prediction market aligns with or is more conservative than sportsbooks.")
        
        return "\n".join(content)
    
    def render_csv(self, report: NewsletterReport, filename: str) -> None:
        """Render report data to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'rank', 'sport', 'away_team', 'home_team', 'start_time',
                'prediction_prob', 'min_book_prob', 'avg_book_prob', 'max_book_prob',
                'discrepancy_abs', 'discrepancy_vs_best', 'volume', 'payout_ratio',
                'expected_value', 'market_title', 'book_names'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write all matched games
            all_games = []
            for section in report.sections:
                for ranking in section.rankings:
                    game = ranking.matched_game
                    book_names = ', '.join([odds.book_name for odds in game.sportsbook_odds])
                    
                    row = {
                        'rank': ranking.rank,
                        'sport': game.game.sport,
                        'away_team': game.game.away_team,
                        'home_team': game.game.home_team,
                        'start_time': game.game.start_time.isoformat(),
                        'prediction_prob': game.prediction_prob,
                        'min_book_prob': game.min_book_prob,
                        'avg_book_prob': game.avg_book_prob,
                        'max_book_prob': game.max_book_prob,
                        'discrepancy_abs': game.discrepancy_abs,
                        'discrepancy_vs_best': game.discrepancy_vs_best,
                        'volume': game.volume,
                        'payout_ratio': game.payout_ratio,
                        'expected_value': game.expected_value,
                        'market_title': game.kalshi_market.title,
                        'book_names': book_names
                    }
                    all_games.append(row)
            
            # Sort by discrepancy and write
            all_games.sort(key=lambda x: x['discrepancy_abs'], reverse=True)
            for i, row in enumerate(all_games):
                row['rank'] = i + 1
                writer.writerow(row)
    
    def render_seattle_snippet(self, seattle_pick: Optional[MatchedGame]) -> str:
        """Render Seattle pick as a social media snippet."""
        if not seattle_pick:
            return "No Seattle team games found in the current data."
        
        game = seattle_pick.game
        start_time = format_time_for_display(game.start_time, self.timezone)
        
        content = []
        content.append("🏠 **Seattle Hometown Pick**")
        content.append("")
        content.append(f"**{game.away_team} @ {game.home_team}**")
        content.append(f"📅 {start_time}")
        content.append("")
        content.append(f"🎯 Prediction Market: {seattle_pick.prediction_prob:.1%}")
        content.append(f"📊 Sportsbook Avg: {seattle_pick.avg_book_prob:.1%}")
        content.append(f"📈 Edge: {seattle_pick.discrepancy_abs:.1%}")
        content.append(f"💰 Payout: {seattle_pick.payout_ratio:.1f}x")
        content.append("")
        content.append("#SeattleSports #EdgeFinder")
        
        return "\n".join(content)
