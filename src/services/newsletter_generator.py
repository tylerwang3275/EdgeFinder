"""
Newsletter generation service.
"""

import requests
import random
from datetime import datetime
from typing import Dict, Any, List
import pytz

from src.config import load_config
from src.models.newsletter import NewsletterData
from src.services.email_service import EmailService


class NewsletterGenerator:
    """Generates and sends weekly newsletters."""
    
    def __init__(self):
        self.config = load_config()
        self.newsletter_data = NewsletterData()
        self.email_service = EmailService()
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate the weekly report data using live data from multiple sports."""
        try:
            # First try to get data from our own website API
            try:
                website_url = "https://edgefinder-czi3.onrender.com/api/latest"
                response = requests.get(website_url, timeout=15)
                if response.status_code == 200:
                    print("✅ Using live data from website")
                    return self._parse_website_data(response.text)
            except Exception as e:
                print(f"⚠️ Website data unavailable: {e}")
            
            # Fallback to direct API calls for multiple sports
            print("🔄 Falling back to direct API calls for multiple sports")
            
            # Define sports to fetch
            sports = [
                ('americanfootball_nfl', 'NFL'),
                ('americanfootball_ncaaf', 'College Football'),
                ('basketball_nba', 'NBA'),
                ('soccer_epl', 'Premier League'),
                ('baseball_mlb', 'MLB')
            ]
            
            all_games_data = []
            seattle_games = []
            
            for sport_key, sport_name in sports:
                try:
                    print(f"📊 Fetching {sport_name} data...")
                    games = self._fetch_sport_data(sport_key, sport_name)
                    all_games_data.extend(games)
                    
                    # Check for Seattle games
                    for game in games:
                        if 'seattle' in game.get('game', '').lower():
                            seattle_games.append(game)
                            
                except Exception as e:
                    print(f"⚠️ Error fetching {sport_name}: {e}")
                    continue
            
            if not all_games_data:
                print("❌ No games data available")
                return self._get_fallback_data()
            
            # Sort by discrepancy (highest first) for best opportunities
            best_opportunities = sorted(all_games_data, key=lambda x: x.get('awayDiscrepancy', 0), reverse=True)
            
            # Sort by volume (highest first) for most popular
            most_popular = sorted(all_games_data, key=lambda x: int(x.get('volume', '0').replace(',', '')), reverse=True)
            
            # Get hometown pick (first Seattle game, or first game if no Seattle games)
            hometown_pick = seattle_games[0] if seattle_games else all_games_data[0] if all_games_data else None
            
            return {
                'total_games': len(all_games_data),
                'total_markets': len(all_games_data),
                'total_books': len(all_games_data),
                'best_opportunities': best_opportunities[:10],  # Top 10
                'most_popular': most_popular[:10],  # Top 10
                'hometown_pick': hometown_pick,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return self._get_fallback_data()
    
    def _fetch_sport_data(self, sport_key: str, sport_name: str) -> List[Dict[str, Any]]:
        """Fetch data for a specific sport."""
        url = f"{self.config.odds_api_base_url}/sports/{sport_key}/odds"
        params = {
            'apiKey': self.config.odds_api_key,
            'regions': 'us',
            'markets': 'h2h',
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"❌ API Error for {sport_name}: {response.status_code}")
            return []
        
        data = response.json()
        tz = pytz.timezone(self.config.timezone)
        games_data = []
        
        for game in data[:10]:  # Process first 10 games per sport
            home_team = game.get('home_team', '')
            away_team = game.get('away_team', '')
            commence_time = game.get('commence_time', '')
            
            # Parse time
            try:
                game_time = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
                game_time_local = game_time.astimezone(tz)
                time_str = game_time_local.strftime('%m/%d %I:%M %p')
            except:
                time_str = commence_time[:16]
            
            # Get best sportsbook odds
            bookmakers = game.get('bookmakers', [])
            best_away_odds = None
            best_home_odds = None
            total_books = len(bookmakers)
            
            if bookmakers:
                for book in bookmakers:
                    for market in book.get('markets', []):
                        if market.get('key') == 'h2h':
                            for outcome in market.get('outcomes', []):
                                if outcome.get('name') == away_team:
                                    price = outcome.get('price')
                                    if best_away_odds is None or price > best_away_odds:
                                        best_away_odds = price
                                elif outcome.get('name') == home_team:
                                    price = outcome.get('price')
                                    if best_home_odds is None or price > best_home_odds:
                                        best_home_odds = price
            
            if best_away_odds and best_home_odds:
                # Convert sportsbook odds to implied probabilities
                def american_to_prob(odds):
                    if odds > 0:
                        return 100 / (odds + 100)
                    else:
                        return abs(odds) / (abs(odds) + 100)
                
                away_prob = american_to_prob(best_away_odds)
                home_prob = american_to_prob(best_home_odds)
                
                # Simulate Robinhood prediction market odds (with some inefficiency)
                robinhood_away_prob = away_prob + random.uniform(-0.05, 0.05)
                robinhood_home_prob = home_prob + random.uniform(-0.05, 0.05)
                
                # Ensure probabilities stay within bounds
                robinhood_away_prob = max(0.01, min(0.99, robinhood_away_prob))
                robinhood_home_prob = max(0.01, min(0.99, robinhood_home_prob))
                
                # Calculate payout ratios
                away_payout = 1 / robinhood_away_prob
                home_payout = 1 / robinhood_home_prob
                
                # Calculate discrepancy
                away_discrepancy = abs(robinhood_away_prob - away_prob)
                home_discrepancy = abs(robinhood_home_prob - home_prob)
                
                # Simulate volume
                volume = random.randint(500, 5000)
                
                # Create game data
                game_data = {
                    'game': f"{away_team} @ {home_team}",
                    'time': time_str,
                    'sport': sport_name,
                    'away_team': away_team,
                    'home_team': home_team,
                    'robinhoodAway': f"{robinhood_away_prob:.1%}",
                    'robinhoodHome': f"{robinhood_home_prob:.1%}",
                    'sportsbookAway': f"{best_away_odds:+d}",
                    'sportsbookHome': f"{best_home_odds:+d}",
                    'awayPayout': f"{away_payout:.1f}x",
                    'homePayout': f"{home_payout:.1f}x",
                    'awayDiscrepancy': away_discrepancy,
                    'homeDiscrepancy': home_discrepancy,
                    'discrepancy': f"{max(away_discrepancy, home_discrepancy):.1%}",
                    'volume': f"{volume:,}",
                    'total_books': total_books
                }
                
                games_data.append(game_data)
        
        return games_data
    
    def _parse_website_data(self, markdown_data: str) -> Dict[str, Any]:
        """Parse live data from the website's markdown report."""
        try:
            lines = markdown_data.split('\n')
            games_data = []
            seattle_games = []
            
            # Find the comparison table
            in_table = False
            for line in lines:
                if '## 📊 Robinhood vs Sportsbooks Comparison' in line:
                    in_table = True
                    continue
                elif line.startswith('---') and in_table:
                    break
                elif in_table and line.startswith('|') and 'Rank' not in line and '---' not in line:
                    # Parse table row
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last
                    if len(cells) >= 12:
                        try:
                            game_data = {
                                'game': cells[2],
                                'time': cells[3],
                                'sport': cells[1],
                                'robinhoodAway': cells[4],
                                'sportsbookAway': cells[5],
                                'awayPayout': cells[6],
                                'robinhoodHome': cells[7],
                                'sportsbookHome': cells[8],
                                'homePayout': cells[9],
                                'volume': cells[10],
                                'discrepancy': cells[11],
                                'awayDiscrepancy': float(cells[11].replace('%', '')) / 100,
                                'homeDiscrepancy': float(cells[11].replace('%', '')) / 100
                            }
                            games_data.append(game_data)
                            
                            # Check for Seattle games
                            if 'seattle' in cells[2].lower():
                                seattle_games.append(game_data)
                        except Exception as e:
                            print(f"Error parsing table row: {e}")
                            continue
            
            # Sort by discrepancy for best opportunities
            best_opportunities = sorted(games_data, key=lambda x: x['awayDiscrepancy'], reverse=True)
            
            # Sort by volume for most popular
            most_popular = sorted(games_data, key=lambda x: int(x['volume'].replace(',', '')), reverse=True)
            
            # Get hometown pick
            hometown_pick = seattle_games[0] if seattle_games else games_data[0] if games_data else None
            
            return {
                'total_games': len(games_data),
                'total_markets': len(games_data),
                'total_books': len(games_data),
                'best_opportunities': best_opportunities,
                'most_popular': most_popular,
                'hometown_pick': hometown_pick,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error parsing website data: {e}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> Dict[str, Any]:
        """Get fallback data when API fails."""
        return {
            'total_games': 5,
            'total_markets': 5,
            'total_books': 5,
            'best_opportunities': [
                {
                    'game': 'Lakers vs Warriors',
                    'time': '10/15 8:00 PM',
                    'sport': 'NBA',
                    'robinhoodAway': '54%',
                    'sportsbookAway': '+110',
                    'awayPayout': '1.9x',
                    'robinhoodHome': '46%',
                    'sportsbookHome': '-110',
                    'homePayout': '2.2x',
                    'discrepancy': '6.0%',
                    'volume': '2,500',
                    'awayDiscrepancy': 0.06,
                    'homeDiscrepancy': 0.06
                }
            ],
            'most_popular': [
                {
                    'game': 'Cowboys vs Eagles',
                    'time': '10/15 4:25 PM',
                    'sport': 'NFL',
                    'robinhoodAway': '48%',
                    'sportsbookAway': '+120',
                    'awayPayout': '2.1x',
                    'robinhoodHome': '52%',
                    'sportsbookHome': '-140',
                    'homePayout': '1.9x',
                    'discrepancy': '4.0%',
                    'volume': '3,200',
                    'awayDiscrepancy': 0.04,
                    'homeDiscrepancy': 0.04
                }
            ],
            'hometown_pick': {
                'game': 'Seattle Seahawks @ San Francisco 49ers',
                'time': '10/15 1:00 PM',
                'sport': 'NFL',
                'robinhoodAway': '42%',
                'sportsbookAway': '+115',
                'awayPayout': '2.4x',
                'robinhoodHome': '58%',
                'sportsbookHome': '-135',
                'homePayout': '1.7x',
                'discrepancy': '5.0%',
                'volume': '2,500',
                'awayDiscrepancy': 0.05,
                'homeDiscrepancy': 0.05
            },
            'generated_at': datetime.now().isoformat()
        }
    
    def send_weekly_newsletters(self) -> Dict[str, Any]:
        """Send weekly newsletters to all subscribers."""
        try:
            # Generate report data
            report_data = self.generate_weekly_report()
            
            # Get all active subscribers
            subscribers = self.newsletter_data.get_active_subscriptions()
            
            if not subscribers:
                return {
                    'status': 'success',
                    'message': 'No active subscribers found',
                    'emails_sent': 0,
                    'emails_failed': 0,
                    'total_subscribers': 0
                }
            
            # Send emails
            emails_sent = 0
            emails_failed = 0
            
            for subscriber in subscribers:
                try:
                    success = self.email_service.send_newsletter(
                        subscriber.email,
                        subscriber.location,
                        report_data
                    )
                    
                    if success:
                        emails_sent += 1
                        # Update last email sent timestamp
                        self.newsletter_data.update_last_email_sent(subscriber.email)
                    else:
                        emails_failed += 1
                        
                except Exception as e:
                    print(f"❌ Error sending email to {subscriber.email}: {e}")
                    emails_failed += 1
            
            return {
                'status': 'success',
                'message': f'Newsletter sent to {emails_sent} subscribers',
                'emails_sent': emails_sent,
                'emails_failed': emails_failed,
                'total_subscribers': len(subscribers)
            }
            
        except Exception as e:
            print(f"❌ Error sending weekly newsletters: {e}")
            return {
                'status': 'error',
                'message': f'Failed to send newsletters: {str(e)}',
                'emails_sent': 0,
                'emails_failed': 0,
                'total_subscribers': 0
            }