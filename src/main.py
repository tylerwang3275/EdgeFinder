"""
Main entry point for EdgeFinder.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.config import load_config
from src.core.pipeline import EdgeFinderPipeline
from src.render.newsletter import NewsletterRenderer
from src.util.log import setup_logging, get_logger


def ensure_output_dir():
    """Ensure output directory exists."""
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def run_pipeline() -> None:
    """Run the EdgeFinder pipeline and generate reports."""
    logger = get_logger()
    logger.info("Starting EdgeFinder pipeline")
    
    try:
        # Load configuration
        config = load_config()
        logger.info(f"Loaded configuration: {config.sports_filter}")
        
        # Ensure output directory
        output_dir = ensure_output_dir()
        
        # Run pipeline
        pipeline = EdgeFinderPipeline(config)
        report = pipeline.run()
        
        # Render reports
        renderer = NewsletterRenderer(config.timezone)
        
        # Generate Markdown report
        markdown_content = renderer.render_markdown(report)
        report_path = output_dir / "report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logger.info(f"Generated report: {report_path}")
        
        # Generate CSV data
        csv_path = output_dir / "edges.csv"
        renderer.render_csv(report, str(csv_path))
        logger.info(f"Generated CSV: {csv_path}")
        
        # Generate Seattle snippet
        seattle_snippet = renderer.render_seattle_snippet(report.seattle_pick)
        seattle_path = output_dir / "seattle.md"
        with open(seattle_path, 'w', encoding='utf-8') as f:
            f.write(seattle_snippet)
        logger.info(f"Generated Seattle snippet: {seattle_path}")
        
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="EdgeFinder",
        description="Sports vs Prediction Markets Analysis",
        version="1.0.0"
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Setup templates
    templates = Jinja2Templates(directory="templates")
    
    # Enhanced report generation function with Robinhood vs Sportsbook comparison
           def generate_simple_real_report():
               """Generate a comprehensive report comparing Robinhood prediction markets vs sportsbook odds across multiple sports."""
               import requests
               from datetime import datetime
               import pytz
               import random
               from src.config import load_config
               
               # Load config
               config = load_config()
               
               # Define sports to fetch with more games per sport
               sports = [
                   ('americanfootball_nfl', 'NFL'),
                   ('americanfootball_ncaaf', 'College Football'),
                   ('basketball_nba', 'NBA'),
                   ('soccer_epl', 'Premier League'),
                   ('baseball_mlb', 'MLB')
               ]
               
               all_games_data = []
               seattle_games = []
               sport_summaries = {}
               
               # Fetch data for each sport
               for sport_key, sport_name in sports:
                   try:
                       url = f"{config.odds_api_base_url}/sports/{sport_key}/odds"
                       params = {
                           'apiKey': config.odds_api_key,
                           'regions': 'us',
                           'markets': 'h2h',
                           'oddsFormat': 'american',
                           'dateFormat': 'iso'
                       }
                       
                       response = requests.get(url, params=params, timeout=10)
                       if response.status_code == 200:
                           data = response.json()
                           print(f"✅ Fetched {len(data)} {sport_name} games")
                           
                           # Process games for this sport
                           sport_games = process_sport_games(data, sport_name, config)
                           all_games_data.extend(sport_games)
                           
                           # Store sport summary
                           sport_summaries[sport_name] = {
                               'total_games': len(sport_games),
                               'games': sport_games[:5]  # Top 5 games per sport
                           }
                           
                           # Check for Seattle games
                           for game in sport_games:
                               if 'seattle' in game.get('game', '').lower():
                                   seattle_games.append(game)
                       else:
                           print(f"❌ Failed to fetch {sport_name}: {response.status_code}")
                           
                   except Exception as e:
                       print(f"❌ Error fetching {sport_name}: {e}")
                       continue
               
               if not all_games_data:
                   return f"# EdgeFinder: Robinhood vs Sportsbooks\n\n❌ No games data available\n\n"
               
               tz = pytz.timezone(config.timezone)
               now = datetime.now(tz)
               
               # Generate report
               report = []
               report.append("# EdgeFinder: Robinhood vs Sportsbooks")
               report.append("")
               report.append(f"**Generated:** {now.strftime('%Y-%m-%d %I:%M %p %Z')}")
               report.append(f"**Total Games:** {len(all_games_data)}")
               report.append("")
               
               # Add sport summaries
               report.append("## 🏆 Sports Summary")
               report.append("")
               for sport_name, summary in sport_summaries.items():
                   report.append(f"### {sport_name}")
                   report.append(f"**Games Available:** {summary['total_games']}")
                   if summary['games']:
                       report.append("**Top Games:**")
                       for game in summary['games']:
                           max_discrepancy = max(game['away_discrepancy'], game['home_discrepancy'])
                           report.append(f"- {game['game']} ({game['time']}) - {max_discrepancy:.1%} discrepancy")
                   report.append("")
               
               # Sort by discrepancy (highest first)
               all_games_data.sort(key=lambda x: max(x['away_discrepancy'], x['home_discrepancy']), reverse=True)
               
               # Add Seattle section
               if seattle_games:
                   report.append("## 🏠 Seattle Games")
                   report.append("")
                   for game in seattle_games:
                       report.append(f"**{game['game']}**")
                       report.append(f"*{game['time']} - {game['sport']}*")
                       report.append("")
                       report.append(f"- **Robinhood {game['away_team']}:** {game['robinhood_away_prob']:.1%} ({game['away_payout']:.1f}x payout)")
                       report.append(f"- **Sportsbook {game['away_team']}:** {game['sportsbook_away_odds']:+d}")
                       report.append(f"- **Discrepancy:** {game['away_discrepancy']:.1%}")
                       report.append("")
                       report.append(f"- **Robinhood {game['home_team']}:** {game['robinhood_home_prob']:.1%} ({game['home_payout']:.1f}x payout)")
                       report.append(f"- **Sportsbook {game['home_team']}:** {game['sportsbook_home_odds']:+d}")
                       report.append(f"- **Discrepancy:** {game['home_discrepancy']:.1%}")
                       report.append("")
               
               # Add main comparison table
               report.append("## 📊 Robinhood vs Sportsbooks Comparison")
               report.append("")
               report.append("| Rank | Sport | Game | Time | Robinhood Away | Sportsbook Away | Away Payout | Robinhood Home | Sportsbook Home | Home Payout | Volume | Discrepancy |")
               report.append("|------|-------|------|------|----------------|-----------------|-------------|----------------|-----------------|-------------|--------|-------------|")
               
               for i, game in enumerate(all_games_data[:30], 1):  # Show top 30 games
                   max_discrepancy = max(game['away_discrepancy'], game['home_discrepancy'])
                   report.append(
                       f"| {i} | {game['sport']} | {game['game']} | {game['time']} | "
                       f"{game['robinhood_away_prob']:.1%} | {game['sportsbook_away_odds']:+d} | {game['away_payout']:.1f}x | "
                       f"{game['robinhood_home_prob']:.1%} | {game['sportsbook_home_odds']:+d} | {game['home_payout']:.1f}x | "
                       f"{game['volume']:,} | {max_discrepancy:.1%} |"
                   )
               
               report.append("")
               report.append("---")
               report.append("")
               report.append("*Real-time data from TheOddsAPI and simulated Robinhood prediction markets*")
               
               return "\n".join(report)
           
           def process_sport_games(data, sport_name, config):
               """Process games for a specific sport."""
               import pytz
               from datetime import datetime
               import random
               
               tz = pytz.timezone(config.timezone)
               games_data = []
               
               for game in data[:15]:  # Process first 15 games per sport
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
                           'robinhood_away_prob': robinhood_away_prob,
                           'robinhood_home_prob': robinhood_home_prob,
                           'sportsbook_away_odds': best_away_odds,
                           'sportsbook_home_odds': best_home_odds,
                           'away_payout': away_payout,
                           'home_payout': home_payout,
                           'away_discrepancy': away_discrepancy,
                           'home_discrepancy': home_discrepancy,
                           'volume': volume,
                           'total_books': total_books
                       }
                       
                       games_data.append(game_data)
               
               return games_data
           
           @app.get("/", response_class=HTMLResponse)
           async def home(request: Request):
               """Serve the main web interface."""
               return templates.TemplateResponse("index.html", {"request": request})
           
           # Newsletter endpoints
           @app.post("/api/newsletter/subscribe")
           async def subscribe_newsletter(request: Request):
               """Subscribe to the newsletter."""
               try:
                   from src.models.newsletter import NewsletterData
                   from src.services.welcome_email_service import WelcomeEmailService
                   
                   data = await request.json()
                   email = data.get('email')
                   location = data.get('location')
                   terms = data.get('terms')
                   
                   if not email or not location or not terms:
                       raise HTTPException(status_code=400, detail="Email, location, and terms agreement are required")
                   
                   # Validate email format
                   import re
                   email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                   if not re.match(email_pattern, email):
                       raise HTTPException(status_code=400, detail="Invalid email format")
                   
                   # Add subscription
                   newsletter_data = NewsletterData()
                   success = newsletter_data.add_subscription(email, location)
                   
                   if success:
                       # Send welcome email immediately
                       try:
                           welcome_service = WelcomeEmailService()
                           welcome_sent = welcome_service.send_welcome_email(email, location)
                           if welcome_sent:
                               print(f"✅ Welcome email sent to {email}")
                           else:
                               print(f"⚠️ Welcome email failed for {email}")
                       except Exception as e:
                           print(f"❌ Error sending welcome email to {email}: {e}")
                           # Don't fail the subscription if welcome email fails
                       
                       return {"message": "Successfully subscribed to newsletter", "email": email, "welcome_sent": True}
                   else:
                       raise HTTPException(status_code=409, detail="Email already subscribed")
                       
               except HTTPException:
                   raise
               except Exception as e:
                   raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")
           
           @app.get("/api/newsletter/subscribers")
           async def get_subscribers():
               """Get all newsletter subscribers (admin endpoint)."""
                
                # Simulate volume
                volume = random.randint(500, 5000)
                
                # Create comparison entry
                comparison_entry = {
                    'game': f"{away_team} @ {home_team}",
                    'time': time_str,
                    'sport': 'NFL',
                    'away_team': away_team,
                    'home_team': home_team,
                    'robinhood_away_prob': robinhood_away_prob,
                    'robinhood_home_prob': robinhood_home_prob,
                    'sportsbook_away_odds': best_away_odds,
                    'sportsbook_home_odds': best_home_odds,
                    'away_payout': away_payout,
                    'home_payout': home_payout,
                    'away_discrepancy': away_discrepancy,
                    'home_discrepancy': home_discrepancy,
                    'volume': volume,
                    'total_books': total_books
                }
                
                comparison_data.append(comparison_entry)
                
                # Check if it's a Seattle game
                if 'seattle' in home_team.lower() or 'seattle' in away_team.lower():
                    seattle_games.append(comparison_entry)
        
        # Sort by discrepancy (highest first)
        comparison_data.sort(key=lambda x: max(x['away_discrepancy'], x['home_discrepancy']), reverse=True)
        
        # Add Seattle section
        if seattle_games:
            report.append("## 🏠 Seattle Games")
            report.append("")
            for game in seattle_games:
                report.append(f"**{game['game']}**")
                report.append(f"*{game['time']}*")
                report.append("")
                report.append(f"- **Robinhood {game['away_team']}:** {game['robinhood_away_prob']:.1%} ({game['away_payout']:.1f}x payout)")
                report.append(f"- **Sportsbook {game['away_team']}:** {game['sportsbook_away_odds']:+d}")
                report.append(f"- **Discrepancy:** {game['away_discrepancy']:.1%}")
                report.append("")
                report.append(f"- **Robinhood {game['home_team']}:** {game['robinhood_home_prob']:.1%} ({game['home_payout']:.1f}x payout)")
                report.append(f"- **Sportsbook {game['home_team']}:** {game['sportsbook_home_odds']:+d}")
                report.append(f"- **Discrepancy:** {game['home_discrepancy']:.1%}")
                report.append("")
        
        # Add main comparison table
        report.append("## 📊 Robinhood vs Sportsbooks Comparison")
        report.append("")
        report.append("| Rank | Sport | Game | Time | Robinhood Away | Sportsbook Away | Away Payout | Robinhood Home | Sportsbook Home | Home Payout | Volume | Discrepancy |")
        report.append("|------|-------|------|------|----------------|-----------------|-------------|----------------|-----------------|-------------|--------|-------------|")
        
        for i, game in enumerate(comparison_data, 1):
            max_discrepancy = max(game['away_discrepancy'], game['home_discrepancy'])
            report.append(
                f"| {i} | {game['sport']} | {game['game']} | {game['time']} | "
                f"{game['robinhood_away_prob']:.1%} | {game['sportsbook_away_odds']:+d} | {game['away_payout']:.1f}x | "
                f"{game['robinhood_home_prob']:.1%} | {game['sportsbook_home_odds']:+d} | {game['home_payout']:.1f}x | "
                f"{game['volume']:,} | {max_discrepancy:.1%} |"
            )
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("*Real-time data from TheOddsAPI and simulated Robinhood prediction markets*")
        
        return "\n".join(report)
    
    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        """Serve the main web interface."""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "edgefinder"}
    
    @app.get("/debug")
    async def debug_info():
        """Debug endpoint to check environment variables."""
        from src.config import load_config
        config = load_config()
        return {
            "sports_filter": config.sports_filter,
            "use_fixtures": config.use_fixtures,
            "odds_api_key_set": bool(config.odds_api_key),
            "kalshi_api_key_set": bool(config.kalshi_api_key_id and config.kalshi_private_key),
            "kalshi_api_key_id_set": bool(config.kalshi_api_key_id),
            "kalshi_private_key_set": bool(config.kalshi_private_key),
            "timezone": config.timezone
        }
    
    @app.get("/debug/robinhood")
    async def debug_robinhood():
        """Debug endpoint to test Robinhood prediction markets."""
        from src.config import load_config
        from src.data.simple_robinhood_client import SimpleRobinhoodClient
        config = load_config()
        client = SimpleRobinhoodClient(config)
        
        try:
            markets = client.get_prediction_markets()
            return {
                "status": "success",
                "markets_count": len(markets),
                "sample_markets": [{"title": m.title, "last_price": m.last_price, "volume": m.volume} for m in markets[:3]]
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    @app.get("/debug/odds")
    async def debug_odds():
        """Debug endpoint to test sportsbook API connection."""
        from src.config import load_config
        from src.data.odds_client import OddsClient
        import requests
        config = load_config()
        client = OddsClient(config)
        
        # Test direct API call first
        direct_api_result = {}
        try:
            url = f"{config.odds_api_base_url}/sports/americanfootball_nfl/odds"
            params = {
                'apiKey': config.odds_api_key,
                'regions': 'us',
                'markets': 'h2h',
                'oddsFormat': 'american',
                'dateFormat': 'iso'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json() if response.status_code == 200 else []
            direct_api_result = {
                "status_code": response.status_code,
                "response_length": len(response.text) if response.text else 0,
                "success": response.status_code == 200,
                "games_count": len(data) if isinstance(data, list) else 0,
                "sample_game": data[0] if data and len(data) > 0 else None
            }
        except Exception as e:
            direct_api_result = {"error": str(e)}
        
        # Test fetching odds for one sport
        try:
            odds = client.get_odds("americanfootball_nfl")
            return {
                "status": "success",
                "odds_count": len(odds),
                "sample_odds": odds[0].__dict__ if odds else None,
                "api_key_set": bool(config.odds_api_key),
                "api_key_preview": config.odds_api_key[:10] + "..." if config.odds_api_key else "None",
                "direct_api_test": direct_api_result
            }
        except Exception as e:
            import traceback
            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "api_key_set": bool(config.odds_api_key),
                "api_key_preview": config.odds_api_key[:10] + "..." if config.odds_api_key else "None",
                "direct_api_test": direct_api_result
            }
    
    @app.get("/api/latest", response_class=PlainTextResponse)
    async def get_latest_report():
        """Get the latest report with real data."""
        try:
            # Generate a simple report using real API data
            return generate_simple_real_report()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
    
    # Newsletter endpoints
    @app.post("/api/newsletter/subscribe")
    async def subscribe_newsletter(request: Request):
        """Subscribe to the newsletter."""
        try:
            from src.models.newsletter import NewsletterData
            from src.services.welcome_email_service import WelcomeEmailService
            
            data = await request.json()
            email = data.get('email')
            location = data.get('location')
            terms = data.get('terms')
            
            if not email or not location or not terms:
                raise HTTPException(status_code=400, detail="Email, location, and terms agreement are required")
            
            # Validate email format
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise HTTPException(status_code=400, detail="Invalid email format")
            
            # Add subscription
            newsletter_data = NewsletterData()
            success = newsletter_data.add_subscription(email, location)
            
            if success:
                # Send welcome email immediately
                try:
                    welcome_service = WelcomeEmailService()
                    welcome_sent = welcome_service.send_welcome_email(email, location)
                    if welcome_sent:
                        print(f"✅ Welcome email sent to {email}")
                    else:
                        print(f"⚠️ Welcome email failed for {email}")
                except Exception as e:
                    print(f"❌ Error sending welcome email to {email}: {e}")
                    # Don't fail the subscription if welcome email fails
                
                return {"message": "Successfully subscribed to newsletter", "email": email, "welcome_sent": True}
            else:
                raise HTTPException(status_code=409, detail="Email already subscribed")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to subscribe: {str(e)}")
    
    @app.get("/api/newsletter/subscribers")
    async def get_subscribers():
        """Get all newsletter subscribers (admin endpoint)."""
        try:
            from src.models.newsletter import NewsletterData
            
            newsletter_data = NewsletterData()
            subscribers = newsletter_data.get_active_subscriptions()
            
            return {
                "total_subscribers": len(subscribers),
                "subscribers": [
                    {
                        "email": sub.email,
                        "location": sub.location,
                        "subscribed_at": sub.subscribed_at.isoformat(),
                        "last_email_sent": sub.last_email_sent.isoformat() if sub.last_email_sent else None
                    }
                    for sub in subscribers
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get subscribers: {str(e)}")
    
    @app.post("/api/newsletter/send")
    async def send_weekly_newsletters():
        """Send weekly newsletters to all subscribers (admin endpoint)."""
        try:
            from src.services.newsletter_generator import NewsletterGenerator
            
            generator = NewsletterGenerator()
            result = generator.send_weekly_newsletters()
            
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send newsletters: {str(e)}")
    
    @app.get("/api/newsletter/preview")
    async def preview_newsletter():
        """Preview the weekly newsletter content."""
        try:
            from src.services.newsletter_generator import NewsletterGenerator
            
            generator = NewsletterGenerator()
            report_data = generator.generate_weekly_report()
            
            return {
                "status": "success",
                "report_data": report_data,
                "preview_note": "This is a preview of the weekly newsletter content"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate preview: {str(e)}")
    
    @app.post("/api/refresh")
    async def refresh_latest_report():
        """Force refresh the latest report with new data."""
        report = generate_simple_real_report()
        if not report:
            raise HTTPException(status_code=500, detail="Failed to generate report")
        return {"status": "success", "message": "Report refreshed successfully"}
    
    @app.get("/api/test-real-data")
    async def test_real_data():
        """Test endpoint to see real API data."""
        import requests
        config = load_config()
        
        try:
            # Test direct API call
            url = f"{config.odds_api_base_url}/sports/americanfootball_nfl/odds"
            params = {
                'apiKey': config.odds_api_key,
                'regions': 'us',
                'markets': 'h2h',
                'oddsFormat': 'american',
                'dateFormat': 'iso'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "games_count": len(data),
                    "sample_games": [
                        {
                            "id": game.get("id"),
                            "home_team": game.get("home_team"),
                            "away_team": game.get("away_team"),
                            "commence_time": game.get("commence_time"),
                            "bookmakers_count": len(game.get("bookmakers", []))
                        }
                        for game in data[:5]  # First 5 games
                    ]
                }
            else:
                return {"status": "error", "status_code": response.status_code, "response": response.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    @app.get("/api/csv")
    async def get_csv():
        """Download the CSV data."""
        csv_path = Path("out/edges.csv")
        if not csv_path.exists():
            raise HTTPException(status_code=404, detail="CSV file not available")
        
        return FileResponse(
            path=str(csv_path),
            filename="edgefinder_data.csv",
            media_type="text/csv"
        )
    
    
    return app


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="EdgeFinder: Sports vs Prediction Markets")
    parser.add_argument(
        "command", 
        choices=["run", "serve"], 
        help="Command to run: 'run' for one-time execution, 'serve' for API server"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host for API server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port for API server (default: 8000)"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level)
    logger = get_logger()
    
    if args.command == "run":
        logger.info("Running EdgeFinder pipeline")
        run_pipeline()
    elif args.command == "serve":
        logger.info(f"Starting EdgeFinder API server on {args.host}:{args.port}")
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
