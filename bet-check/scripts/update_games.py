"""
Fetch live NBA games from ESPN API and update database.
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

# ESPN API (free, no key required)
ESPN_NBA_API = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

supabase: Client = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"⚠️  Could not connect to Supabase: {e}")
    supabase = None

def fetch_nba_games_from_espn():
    """
    Fetch current and upcoming NBA games from ESPN API.
    Returns games for today and next 7 days.
    """
    try:
        all_games = []
        
        # Fetch games for today and next 7 days
        for days_ahead in range(8):
            target_date = datetime.now() + timedelta(days=days_ahead)
            date_str = target_date.strftime("%Y%m%d")
            
            url = f"{ESPN_NBA_API}?dates={date_str}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get("events", [])
                
                for event in events:
                    try:
                        competitions = event.get("competitions", [{}])[0]
                        competitors = competitions.get("competitors", [])
                        
                        if len(competitors) >= 2:
                            # Home team is usually index 0, away is index 1
                            home_team = competitors[0].get("team", {}).get("displayName", "Unknown")
                            away_team = competitors[1].get("team", {}).get("displayName", "Unknown")
                            
                            game_id = f"nba_{event.get('id', '')}_{date_str}"
                            scheduled = event.get("date", target_date.isoformat())
                            
                            all_games.append({
                                "game_id": game_id,
                                "sport": "nba",
                                "team_a": home_team,
                                "team_b": away_team,
                                "scheduled_date": scheduled[:10],  # YYYY-MM-DD format
                                "result": None
                            })
                    except Exception as e:
                        print(f"  Warning: Could not parse event: {e}")
                        continue
                        
                print(f"✓ Fetched {len(events)} games for {target_date.strftime('%Y-%m-%d')}")
            else:
                print(f"⚠ ESPN API returned {response.status_code} for {date_str}")
        
        return all_games
    
    except Exception as e:
        print(f"✗ Error fetching from ESPN API: {str(e)}")
        return []

def update_games():
    """Fetch games from ESPN and update database or display them."""
    try:
        print("Fetching upcoming NBA games from ESPN...")
        games = fetch_nba_games_from_espn()
        
        if not games:
            print("⚠️  No games found")
            return
        
        print(f"\n✓ Found {len(games)} upcoming games")
        
        if supabase is None:
            print("\n⚠️  Supabase not connected. Games retrieved:")
            for i, game in enumerate(games[:10], 1):
                print(f"  {i}. {game['team_a']} vs {game['team_b']} ({game['scheduled_date']})")
            if len(games) > 10:
                print(f"  ... and {len(games) - 10} more")
            return
        
        # Upsert games into database
        success_count = 0
        for game in games:
            try:
                response = supabase.table("games").upsert(game).execute()
                success_count += 1
            except Exception as e:
                print(f"  ✗ Failed to upsert {game['team_a']} vs {game['team_b']}: {e}")
        
        print(f"\n✓ Successfully updated {success_count}/{len(games)} games!")
        
    except Exception as e:
        print(f"✗ Error updating games: {str(e)}")

if __name__ == "__main__":
    update_games()
