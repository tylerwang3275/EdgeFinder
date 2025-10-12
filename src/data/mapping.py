"""
Team and market mapping utilities.
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from src.core.models import Team, Game


# Seattle team aliases
SEATTLE_TEAMS = {
    "americanfootball_nfl": {
        "seahawks": ["seattle seahawks", "seahawks", "sea", "seattle"],
        "abbreviation": "SEA"
    },
    "baseball_mlb": {
        "mariners": ["seattle mariners", "mariners", "sea", "seattle"],
        "abbreviation": "SEA"
    },
    "icehockey_nhl": {
        "kraken": ["seattle kraken", "kraken", "sea", "seattle"],
        "abbreviation": "SEA"
    },
    "soccer": {
        "sounders": ["seattle sounders", "sounders", "sea", "seattle"],
        "abbreviation": "SEA"
    },
    "wnba": {
        "storm": ["seattle storm", "storm", "sea", "seattle"],
        "abbreviation": "SEA"
    },
    "americanfootball_ncaaf": {
        "huskies": ["washington huskies", "uw huskies", "huskies", "washington", "uw"],
        "abbreviation": "UW"
    }
}

# General team aliases for major sports
TEAM_ALIASES = {
    "americanfootball_nfl": {
        "patriots": ["new england patriots", "ne patriots", "ne", "new england", "patriots"],
        "bills": ["buffalo bills", "buf", "buffalo"],
        "dolphins": ["miami dolphins", "mia", "miami"],
        "jets": ["new york jets", "ny jets", "nyj", "jets"],
        "steelers": ["pittsburgh steelers", "pit", "pittsburgh"],
        "ravens": ["baltimore ravens", "bal", "baltimore"],
        "browns": ["cleveland browns", "cle", "cleveland"],
        "bengals": ["cincinnati bengals", "cin", "cincinnati"],
        "texans": ["houston texans", "hou", "houston"],
        "colts": ["indianapolis colts", "ind", "indianapolis"],
        "jaguars": ["jacksonville jaguars", "jax", "jacksonville"],
        "titans": ["tennessee titans", "ten", "tennessee"],
        "chiefs": ["kansas city chiefs", "kc", "kansas city"],
        "raiders": ["las vegas raiders", "lv", "las vegas", "oakland raiders"],
        "chargers": ["los angeles chargers", "lac", "la chargers"],
        "broncos": ["denver broncos", "den", "denver"],
        "cowboys": ["dallas cowboys", "dal", "dallas"],
        "giants": ["new york giants", "ny giants", "nyg", "giants"],
        "eagles": ["philadelphia eagles", "phi", "philadelphia"],
        "commanders": ["washington commanders", "was", "washington", "wft"],
        "packers": ["green bay packers", "gb", "green bay"],
        "lions": ["detroit lions", "det", "detroit"],
        "bears": ["chicago bears", "chi", "chicago"],
        "vikings": ["minnesota vikings", "min", "minnesota"],
        "falcons": ["atlanta falcons", "atl", "atlanta"],
        "panthers": ["carolina panthers", "car", "carolina"],
        "saints": ["new orleans saints", "no", "new orleans"],
        "buccaneers": ["tampa bay buccaneers", "tb", "tampa bay", "tampa"],
        "cardinals": ["arizona cardinals", "ari", "arizona"],
        "rams": ["los angeles rams", "lar", "la rams"],
        "49ers": ["san francisco 49ers", "sf", "san francisco"],
    },
    "baseball_mlb": {
        "yankees": ["new york yankees", "ny yankees", "nyy", "yankees"],
        "red sox": ["boston red sox", "bos", "boston"],
        "blue jays": ["toronto blue jays", "tor", "toronto"],
        "orioles": ["baltimore orioles", "bal", "baltimore"],
        "rays": ["tampa bay rays", "tb", "tampa bay", "tampa"],
        "astros": ["houston astros", "hou", "houston"],
        "angels": ["los angeles angels", "laa", "la angels", "anaheim angels"],
        "athletics": ["oakland athletics", "oak", "oakland", "a's"],
        "rangers": ["texas rangers", "tex", "texas"],
        "twins": ["minnesota twins", "min", "minnesota"],
        "royals": ["kansas city royals", "kc", "kansas city"],
        "tigers": ["detroit tigers", "det", "detroit"],
        "indians": ["cleveland indians", "cle", "cleveland", "guardians"],
        "white sox": ["chicago white sox", "cws", "chicago"],
        "guardians": ["cleveland guardians", "cle", "cleveland"],
        "braves": ["atlanta braves", "atl", "atlanta"],
        "marlins": ["miami marlins", "mia", "miami"],
        "mets": ["new york mets", "ny mets", "nym", "mets"],
        "phillies": ["philadelphia phillies", "phi", "philadelphia"],
        "nationals": ["washington nationals", "was", "washington"],
        "cubs": ["chicago cubs", "chc", "chicago"],
        "reds": ["cincinnati reds", "cin", "cincinnati"],
        "brewers": ["milwaukee brewers", "mil", "milwaukee"],
        "pirates": ["pittsburgh pirates", "pit", "pittsburgh"],
        "cardinals": ["st. louis cardinals", "stl", "st louis"],
        "diamondbacks": ["arizona diamondbacks", "ari", "arizona"],
        "dodgers": ["los angeles dodgers", "lad", "la dodgers"],
        "giants": ["san francisco giants", "sf", "san francisco"],
        "padres": ["san diego padres", "sd", "san diego"],
        "rockies": ["colorado rockies", "col", "colorado"],
    },
    "basketball_nba": {
        "celtics": ["boston celtics", "bos", "boston"],
        "nets": ["brooklyn nets", "bkn", "brooklyn"],
        "knicks": ["new york knicks", "nyk", "knicks"],
        "76ers": ["philadelphia 76ers", "phi", "philadelphia", "sixers"],
        "raptors": ["toronto raptors", "tor", "toronto"],
        "bulls": ["chicago bulls", "chi", "chicago"],
        "cavaliers": ["cleveland cavaliers", "cle", "cleveland", "cavs"],
        "pistons": ["detroit pistons", "det", "detroit"],
        "pacers": ["indiana pacers", "ind", "indiana"],
        "bucks": ["milwaukee bucks", "mil", "milwaukee"],
        "hawks": ["atlanta hawks", "atl", "atlanta"],
        "hornets": ["charlotte hornets", "cha", "charlotte"],
        "heat": ["miami heat", "mia", "miami"],
        "magic": ["orlando magic", "orl", "orlando"],
        "wizards": ["washington wizards", "was", "washington"],
        "nuggets": ["denver nuggets", "den", "denver"],
        "timberwolves": ["minnesota timberwolves", "min", "minnesota"],
        "thunder": ["oklahoma city thunder", "okc", "oklahoma city"],
        "trail blazers": ["portland trail blazers", "por", "portland", "blazers"],
        "jazz": ["utah jazz", "uta", "utah"],
        "warriors": ["golden state warriors", "gsw", "golden state", "gs"],
        "clippers": ["los angeles clippers", "lac", "la clippers"],
        "lakers": ["los angeles lakers", "lal", "la lakers"],
        "suns": ["phoenix suns", "phx", "phoenix"],
        "kings": ["sacramento kings", "sac", "sacramento"],
        "mavericks": ["dallas mavericks", "dal", "dallas"],
        "rockets": ["houston rockets", "hou", "houston"],
        "grizzlies": ["memphis grizzlies", "mem", "memphis"],
        "pelicans": ["new orleans pelicans", "no", "new orleans"],
        "spurs": ["san antonio spurs", "sa", "san antonio"],
        "warriors": ["golden state warriors", "gsw", "golden state", "gs"],
    },
    "icehockey_nhl": {
        "bruins": ["boston bruins", "bos", "boston"],
        "sabres": ["buffalo sabres", "buf", "buffalo"],
        "red wings": ["detroit red wings", "det", "detroit"],
        "panthers": ["florida panthers", "fla", "florida"],
        "canadiens": ["montreal canadiens", "mtl", "montreal", "habs"],
        "senators": ["ottawa senators", "ott", "ottawa"],
        "lightning": ["tampa bay lightning", "tb", "tampa bay", "tampa"],
        "leafs": ["toronto maple leafs", "tor", "toronto", "maple leafs"],
        "hurricanes": ["carolina hurricanes", "car", "carolina"],
        "blue jackets": ["columbus blue jackets", "cbj", "columbus"],
        "devils": ["new jersey devils", "nj", "new jersey"],
        "islanders": ["new york islanders", "nyi", "islanders"],
        "rangers": ["new york rangers", "nyr", "rangers"],
        "flyers": ["philadelphia flyers", "phi", "philadelphia"],
        "penguins": ["pittsburgh penguins", "pit", "pittsburgh"],
        "capitals": ["washington capitals", "was", "washington", "caps"],
        "blackhawks": ["chicago blackhawks", "chi", "chicago"],
        "avalanche": ["colorado avalanche", "col", "colorado"],
        "stars": ["dallas stars", "dal", "dallas"],
        "wild": ["minnesota wild", "min", "minnesota"],
        "predators": ["nashville predators", "nsh", "nashville"],
        "blues": ["st. louis blues", "stl", "st louis"],
        "jets": ["winnipeg jets", "wpg", "winnipeg"],
        "flames": ["calgary flames", "cgy", "calgary"],
        "oilers": ["edmonton oilers", "edm", "edmonton"],
        "kings": ["los angeles kings", "lak", "la kings"],
        "ducks": ["anaheim ducks", "ana", "anaheim"],
        "coyotes": ["arizona coyotes", "ari", "arizona"],
        "sharks": ["san jose sharks", "sjs", "san jose"],
        "golden knights": ["vegas golden knights", "vgk", "vegas", "knights"],
    }
}


def normalize_team_name(name: str, sport: str) -> str:
    """
    Normalize a team name for consistent matching.
    
    Args:
        name: Raw team name
        sport: Sport abbreviation
        
    Returns:
        Normalized team name
    """
    # Convert to lowercase and remove extra spaces
    normalized = re.sub(r'\s+', ' ', name.lower().strip())
    
    # Remove common suffixes
    suffixes_to_remove = [
        ' fc', ' football club', ' soccer club', ' sc',
        ' basketball', ' baseball', ' hockey', ' football',
        ' university', ' college', ' state', ' tech'
    ]
    
    for suffix in suffixes_to_remove:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)].strip()
    
    return normalized


def find_team_match(name: str, sport: str) -> Optional[str]:
    """
    Find a matching team name from aliases.
    
    Args:
        name: Team name to match
        sport: Sport abbreviation
        
    Returns:
        Canonical team name if found, None otherwise
    """
    normalized_name = normalize_team_name(name, sport)
    
    # Check sport-specific aliases
    sport_aliases = TEAM_ALIASES.get(sport, {})
    for canonical, aliases in sport_aliases.items():
        if normalized_name in aliases or any(alias in normalized_name for alias in aliases):
            return canonical
    
    # Check Seattle teams
    seattle_teams = SEATTLE_TEAMS.get(sport, {})
    for team_name, aliases in seattle_teams.items():
        if team_name != "abbreviation" and normalized_name in aliases:
            return team_name
    
    return None


def is_seattle_team(team_name: str, sport: str) -> bool:
    """
    Check if a team is a Seattle team.
    
    Args:
        team_name: Team name
        sport: Sport abbreviation
        
    Returns:
        True if Seattle team, False otherwise
    """
    normalized_name = normalize_team_name(team_name, sport)
    seattle_teams = SEATTLE_TEAMS.get(sport, {})
    
    for team_key, aliases in seattle_teams.items():
        if team_key != "abbreviation" and normalized_name in aliases:
            return True
    
    return False


def extract_teams_from_kalshi_title(title: str, sport: str) -> Optional[Tuple[str, str]]:
    """
    Extract team names from a Kalshi market title.
    
    Args:
        title: Kalshi market title
        sport: Sport abbreviation
        
    Returns:
        Tuple of (team1, team2) if found, None otherwise
    """
    # Common patterns for team extraction
    patterns = [
        r'(.+?)\s+vs\.?\s+(.+)',
        r'(.+?)\s+@\s+(.+)',
        r'(.+?)\s+at\s+(.+)',
        r'(.+?)\s+over\s+(.+)',
        r'(.+?)\s+beats?\s+(.+)',
        r'(.+?)\s+defeats?\s+(.+)',
        r'(.+?)\s+wins?\s+against\s+(.+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            team1 = match.group(1).strip()
            team2 = match.group(2).strip()
            
            # Try to match both teams
            team1_match = find_team_match(team1, sport)
            team2_match = find_team_match(team2, sport)
            
            if team1_match and team2_match:
                return team1_match, team2_match
    
    return None


def create_game_from_market(market_title: str, event_time: datetime, sport: str) -> Optional[Game]:
    """
    Create a Game object from a Kalshi market.
    
    Args:
        market_title: Kalshi market title
        event_time: Event start time
        sport: Sport abbreviation
        
    Returns:
        Game object if teams can be extracted, None otherwise
    """
    teams = extract_teams_from_kalshi_title(market_title, sport)
    if not teams:
        return None
    
    team1, team2 = teams
    
    # Determine home/away (simple heuristic: second team is usually home)
    return Game(
        sport=sport,
        away_team=team1,
        home_team=team2,
        start_time=event_time
    )


def match_games_within_timeframe(
    kalshi_games: List[Game], 
    sportsbook_games: List[Game], 
    time_tolerance_hours: int = 2
) -> List[Tuple[Game, Game]]:
    """
    Match Kalshi games with sportsbook games within a time tolerance.
    
    Args:
        kalshi_games: List of Kalshi games
        sportsbook_games: List of sportsbook games
        time_tolerance_hours: Time tolerance in hours
        
    Returns:
        List of matched (kalshi_game, sportsbook_game) tuples
    """
    matches = []
    time_tolerance = timedelta(hours=time_tolerance_hours)
    
    for kalshi_game in kalshi_games:
        for sportsbook_game in sportsbook_games:
            # Check if games are the same sport
            if kalshi_game.sport != sportsbook_game.sport:
                continue
            
            # Check if teams match (either direction)
            teams_match = (
                (kalshi_game.away_team == sportsbook_game.away_team and 
                 kalshi_game.home_team == sportsbook_game.home_team) or
                (kalshi_game.away_team == sportsbook_game.home_team and 
                 kalshi_game.home_team == sportsbook_game.away_team)
            )
            
            # Check if times are within tolerance
            time_diff = abs(kalshi_game.start_time - sportsbook_game.start_time)
            time_match = time_diff <= time_tolerance
            
            if teams_match and time_match:
                matches.append((kalshi_game, sportsbook_game))
                break  # Found a match, move to next Kalshi game
    
    return matches
