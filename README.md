# EdgeFinder: Sports vs Prediction Markets MVP

EdgeFinder compares sportsbook odds to prediction market data (via Kalshi) to identify discrepancies and potential betting edges. It generates newsletter-ready reports with rankings and Seattle hometown picks.

## Features

- **Prediction Market Data**: Fetches data from Kalshi (proxy for Robinhood Predictions)
- **Sportsbook Odds**: Integrates with TheOddsAPI for multiple bookmakers
- **Discrepancy Analysis**: Calculates differences between prediction markets and sportsbooks
- **Rankings**: Generates top discrepancies, most bet games, and payout opportunities
- **Seattle Focus**: Special section for Seattle-area teams (Seahawks, Mariners, Kraken, Sounders, Storm, UW Huskies)
- **Newsletter Output**: Markdown reports ready for email/newsletter platforms
- **CSV Export**: Raw data for further analysis

## Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to project
cd EdgeFinder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your API keys
KALSHI_BASE_URL=https://api.kalshi.com
ODDS_API_BASE_URL=https://api.theoddsapi.com/v4
ODDS_API_KEY=your_odds_api_key_here
EDGEFINDER_TIMEZONE=America/Los_Angeles
SPORTS_FILTER=mlb,nfl,nba,nhl,soccer
LOOKAHEAD_HOURS=48
MIN_VOLUME=100
TOP_N=10
USE_FIXTURES=false
```

### 3. Run Pipeline

```bash
# One-time execution
python -m src.main run

# Start web server (includes web interface)
python -m src.main serve --host 0.0.0.0 --port 8000
```

### 4. Access Web Interface

Open your browser and go to:
- **Web Interface**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/latest
- **CSV Download**: http://localhost:8000/api/csv
- **Health Check**: http://localhost:8000/health

### 5. View Results

Check the `out/` directory for generated files:
- `report.md` - Newsletter-ready Markdown report
- `edges.csv` - Raw data in CSV format
- `seattle.md` - Seattle hometown pick snippet

## Web Interface

EdgeFinder includes a modern web interface with:

- **📊 Dashboard**: Real-time view of discrepancies and rankings
- **🔄 Auto-refresh**: Updates every 5 minutes automatically
- **📱 Responsive**: Works on desktop, tablet, and mobile
- **💾 CSV Download**: One-click data export
- **🏠 Seattle Focus**: Special section for hometown teams

## API Endpoints

When running the web server:

- `GET /` - Web interface (HTML)
- `GET /health` - Health check
- `GET /api/latest` - Get latest report as text
- `GET /api/csv` - Download CSV data
- `POST /refresh` - Refresh report by running pipeline

## Project Structure

```
edgefinder/
├── src/
│   ├── config.py              # Configuration management
│   ├── main.py                # CLI and FastAPI entrypoint
│   ├── core/
│   │   ├── odds_math.py       # Odds conversion utilities
│   │   ├── models.py          # Pydantic data models
│   │   └── pipeline.py        # Main processing pipeline
│   ├── data/
│   │   ├── kalshi_client.py   # Kalshi API client
│   │   ├── odds_client.py     # Sportsbook odds client
│   │   ├── mapping.py         # Team name mapping
│   │   └── cache.py           # Simple caching
│   ├── render/
│   │   └── newsletter.py      # Markdown/CSV rendering
│   └── util/
│       ├── time.py            # Time utilities
│       └── log.py             # Logging setup
├── tests/                     # Test suite
├── scripts/
│   └── run_once.sh           # Cron script
└── out/                      # Generated outputs
```

## How It Works

### 1. Data Collection
- Fetches prediction market data from Kalshi
- Retrieves sportsbook odds from TheOddsAPI
- Filters for games within the next 48 hours (configurable)

### 2. Team Mapping
- Normalizes team names across different data sources
- Maps Kalshi market titles to canonical team names
- Special handling for Seattle teams

### 3. Discrepancy Calculation
- Converts all odds to implied probabilities
- Calculates absolute discrepancies between prediction markets and sportsbooks
- Computes edge vs best available odds

### 4. Ranking & Reporting
- **Biggest Discrepancies**: Games with largest prediction vs book differences
- **Most Bet**: Games with highest prediction market volume
- **Highest Payout**: Long-shot bets with significant volume
- **Seattle Pick**: Best Seattle team opportunity

## Adding Sports/Books

### Adding New Sports
1. Update team aliases in `src/data/mapping.py`
2. Add sport to `SPORTS_FILTER` in configuration
3. Update sport inference logic in `src/core/pipeline.py`

### Adding New Books
The system automatically includes all books available through TheOddsAPI. No code changes needed.

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `KALSHI_BASE_URL` | Kalshi API base URL | `https://api.kalshi.com` |
| `ODDS_API_BASE_URL` | TheOddsAPI base URL | `https://api.theoddsapi.com/v4` |
| `ODDS_API_KEY` | TheOddsAPI key | Required |
| `EDGEFINDER_TIMEZONE` | Display timezone | `America/Los_Angeles` |
| `SPORTS_FILTER` | Comma-separated sports | `mlb,nfl,nba,nhl,soccer` |
| `LOOKAHEAD_HOURS` | Hours to look ahead | `48` |
| `MIN_VOLUME` | Minimum market volume | `100` |
| `TOP_N` | Number of top results | `10` |
| `USE_FIXTURES` | Use test data | `false` |

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_math.py

# Run with coverage
pytest --cov=src tests/
```

## Deployment

### Docker (Recommended)

```bash
# Quick deployment
./scripts/deploy.sh

# Or manually
docker-compose up -d
```

### Cloud Platforms

- **Heroku**: See `DEPLOYMENT.md` for detailed instructions
- **Railway**: Connect GitHub repo and deploy
- **DigitalOcean**: Use App Platform
- **VPS**: Use Docker Compose with Nginx reverse proxy

See `DEPLOYMENT.md` for comprehensive deployment options.

## Cron Setup

For daily execution at 1 PM Pacific (UTC 13:00):

```bash
# Add to crontab
0 13 * * * /path/to/EdgeFinder/scripts/run_once.sh
```

## Known Limitations

1. **Market Semantics**: Kalshi market titles must clearly indicate teams and outcomes
2. **Partial Coverage**: Not all games may have both prediction market and sportsbook data
3. **API Limits**: Respects rate limits but may need adjustment for high-volume usage
4. **Team Mapping**: Manual mapping required for new teams/leagues

## Development

### Adding Tests
- Place test files in `tests/` directory
- Use `pytest` naming conventions
- Include fixtures in `tests/fixtures/`

### Code Style
- Follow PEP 8
- Use type hints
- Document functions and classes

### Dependencies
- Python 3.11+
- FastAPI for API server
- Pandas for data processing
- Pydantic for data validation
- Requests for API calls

## License

This project is for educational and informational purposes only. Sports betting involves risk and may not be legal in all jurisdictions.

## Disclaimer

EdgeFinder is not affiliated with Kalshi, TheOddsAPI, or any sportsbook. This tool is for informational purposes only and does not constitute financial or betting advice. Always gamble responsibly and within your means.
