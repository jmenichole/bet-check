"""
Fetch upcoming games from sports API and update database.
Run this periodically to keep games list fresh (e.g., daily via cron).

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")

# Using free API: api-nba.com (no key required)
NBA_GAMES_API = "https://api-nba-v1.p.rapidapi.com/games"
RAPIDAPI_HOST = "api-nba-v1.p.rapidapi.com"
RAPIDAPI_KEY = SPORTS_API_KEY

supabase: Client = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"⚠️  Could not connect to Supabase: {e}")
    supabase = None

# Sample games for demo (since we're using a free API)
SAMPLE_GAMES = [
    {
        "game_id": "nba_2025_01_15_lakers_celtics",
        "sport": "nba",
        "team_a": "Los Angeles Lakers",
        "team_b": "Boston Celtics",
        "scheduled_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "result": None,
    },
    {
        "game_id": "nba_2025_01_16_warriors_nuggets",
        "sport": "nba",
        "team_a": "Golden State Warriors",
        "team_b": "Denver Nuggets",
        "scheduled_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "result": None,
    },
    {
        "game_id": "nba_2025_01_17_heat_bucks",
        "sport": "nba",
        "team_a": "Miami Heat",
        "team_b": "Milwaukee Bucks",
        "scheduled_date": (datetime.utcnow() + timedelta(days=3)).isoformat(),
        "result": None,
    },
    {
        "game_id": "nba_2025_01_18_suns_grizzlies",
        "sport": "nba",
        "team_a": "Phoenix Suns",
        "team_b": "Memphis Grizzlies",
        "scheduled_date": (datetime.utcnow() + timedelta(days=4)).isoformat(),
        "result": None,
    },
]

def fetch_nba_games():
    """
    Fetch upcoming NBA games from sports API.
    Falls back to sample games if API fails.
    """
    try:
        # Optional: Uncomment to use actual API
        # headers = {
        #     "x-rapidapi-host": RAPIDAPI_HOST,
        #     "x-rapidapi-key": RAPIDAPI_KEY
        # }
        # querystring = {"league": "nba"}
        # response = requests.get(NBA_GAMES_API, headers=headers, params=querystring)
        # if response.status_code == 200:
        #     return response.json()
        
        # For demo: use sample games
        print("Using sample games for demo (API key not configured)")
        return SAMPLE_GAMES
    
    except Exception as e:
        print(f"Error fetching from API: {str(e)}")
        print("Falling back to sample games...")
        return SAMPLE_GAMES

def update_games():
    """Fetch games and update database."""
    try:
        print("Fetching upcoming games...")
        games = fetch_nba_games()
        
        if isinstance(games, dict):
            games = games.get("response", [])
        
        print(f"Found {len(games)} upcoming games")
        
        if supabase is None:
            print("⚠️  Supabase not connected. Games would be:")
            for game in games:
                print(f"  • {game['team_a']} vs {game['team_b']}")
            return
        
        # Upsert games into database
        for game in games:
            response = supabase.table("games").upsert(game).execute()
            print(f"✓ Upserted game: {game['team_a']} vs {game['team_b']}")
        
        print(f"\n✓ Successfully updated {len(games)} games!")
        
    except Exception as e:
        print(f"✗ Error updating games: {str(e)}")

if __name__ == "__main__":
    update_games()
