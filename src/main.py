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
    
    # Global variables for caching
    last_report: Optional[str] = None
    last_report_time: Optional[str] = None
    
    def load_cached_report():
        """Load report from cache or file."""
        nonlocal last_report, last_report_time
        if not last_report:
            # Try to read existing report
            report_path = Path("out/report.md")
            if report_path.exists():
                try:
                    with open(report_path, 'r', encoding='utf-8') as f:
                        last_report = f.read()
                        last_report_time = str(report_path.stat().st_mtime)
                except Exception as e:
                    print(f"Error reading report: {e}")
                    return None
            else:
                return None
        return last_report
    
    def refresh_report():
        """Generate a new report."""
        nonlocal last_report, last_report_time
        try:
            # Run the pipeline to generate a new report
            pipeline = EdgeFinderPipeline(config)
            report = pipeline.run()
            
            # Render the report
            renderer = NewsletterRenderer(config.timezone)
            markdown_content = renderer.render_markdown(report)
            
            # Update cache
            last_report = markdown_content
            last_report_time = str(datetime.utcnow())
            
            # Save to file
            output_dir = Path("out")
            output_dir.mkdir(exist_ok=True)
            report_path = output_dir / "report.md"
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return markdown_content
        except Exception as e:
            print(f"Error generating report: {e}")
            return None
    
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
    
    def generate_simple_real_report():
        """Generate a simple report using real API data."""
        import requests
        from datetime import datetime
        import pytz
        from src.config import load_config
        
        # Load config
        config = load_config()
        
        # Get real NFL data
        url = f"{config.odds_api_base_url}/sports/americanfootball_nfl/odds"
        params = {
            'apiKey': config.odds_api_key,
            'regions': 'us',
            'markets': 'h2h',
            'oddsFormat': 'american',
            'dateFormat': 'iso'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return f"# EdgeFinder: Real-Time NFL Data\n\n❌ API Error: {response.status_code}\n\n"
        
        data = response.json()
        tz = pytz.timezone(config.timezone)
        now = datetime.now(tz)
        
        # Generate report
        report = []
        report.append("# EdgeFinder: Real-Time NFL Data")
        report.append("")
        report.append(f"**Generated:** {now.strftime('%Y-%m-%d %I:%M %p %Z')}")
        report.append(f"**Total Games:** {len(data)}")
        report.append("")
        
        # Find Seattle games
        seattle_games = []
        for game in data:
            if 'seattle' in game.get('home_team', '').lower() or 'seattle' in game.get('away_team', '').lower():
                seattle_games.append(game)
        
        if seattle_games:
            report.append("## 🏠 Seattle Games")
            report.append("")
            for game in seattle_games:
                home_team = game.get('home_team', '')
                away_team = game.get('away_team', '')
                commence_time = game.get('commence_time', '')
                
                # Parse time
                try:
                    game_time = datetime.fromisoformat(commence_time.replace('Z', '+00:00'))
                    game_time_local = game_time.astimezone(tz)
                    time_str = game_time_local.strftime('%Y-%m-%d %I:%M %p %Z')
                except:
                    time_str = commence_time
                
                report.append(f"**{away_team} @ {home_team}**")
                report.append(f"*{time_str}*")
                
                # Get best odds
                bookmakers = game.get('bookmakers', [])
                if bookmakers:
                    best_away = None
                    best_home = None
                    for book in bookmakers:
                        for market in book.get('markets', []):
                            if market.get('key') == 'h2h':
                                for outcome in market.get('outcomes', []):
                                    if outcome.get('name') == away_team:
                                        if best_away is None or outcome.get('price', 0) > best_away:
                                            best_away = outcome.get('price')
                                    elif outcome.get('name') == home_team:
                                        if best_home is None or outcome.get('price', 0) > best_home:
                                            best_home = outcome.get('price')
                    
                    if best_away and best_home:
                        report.append(f"- **{away_team}:** +{best_away}")
                        report.append(f"- **{home_team}:** {best_home}")
                
                report.append("")
        
        # Show all games
        report.append("## 📊 All NFL Games")
        report.append("")
        report.append("| Away Team | Home Team | Start Time | Best Away Odds | Best Home Odds |")
        report.append("|-----------|-----------|------------|----------------|----------------|")
        
        for game in data[:10]:  # Show first 10 games
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
            
            # Get best odds
            bookmakers = game.get('bookmakers', [])
            best_away = "N/A"
            best_home = "N/A"
            
            if bookmakers:
                for book in bookmakers:
                    for market in book.get('markets', []):
                        if market.get('key') == 'h2h':
                            for outcome in market.get('outcomes', []):
                                if outcome.get('name') == away_team:
                                    price = outcome.get('price')
                                    if price and (best_away == "N/A" or price > int(best_away.replace('+', ''))):
                                        best_away = f"+{price}" if price > 0 else str(price)
                                elif outcome.get('name') == home_team:
                                    price = outcome.get('price')
                                    if price and (best_home == "N/A" or price > int(best_home.replace('+', ''))):
                                        best_home = f"+{price}" if price > 0 else str(price)
            
            report.append(f"| {away_team} | {home_team} | {time_str} | {best_away} | {best_home} |")
        
        report.append("")
        report.append("---")
        report.append("")
        report.append("*Real-time data from TheOddsAPI*")
        
        return "\n".join(report)
    
    @app.post("/api/refresh")
    async def refresh_latest_report():
        """Force refresh the latest report with new data."""
        report = refresh_report()
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
    
    @app.post("/refresh")
    async def refresh_report():
        """Refresh the report by running the pipeline."""
        nonlocal last_report, last_report_time
        
        try:
            run_pipeline()
            
            # Read the new report
            report_path = Path("out/report.md")
            if report_path.exists():
                with open(report_path, 'r', encoding='utf-8') as f:
                    last_report = f.read()
                    last_report_time = str(report_path.stat().st_mtime)
                
                return {"status": "success", "message": "Report refreshed"}
            else:
                raise HTTPException(status_code=500, detail="Report generation failed")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")
    
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
