"""
ESPN Scoreboard Fetcher & DB Updater
Fetches upcoming & recent games from public ESPN API (no key required)
Updates games table in Supabase
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

SPORTS = {
    "nba": "basketball/nba",
    "nfl": "football/nfl",
    # add more later
}

def fetch_games(sport: str = "nba", days_ahead: int = 5) -> List[Dict]:
    base_url = "https://site.api.espn.com/apis/site/v2/sports/"
    today = datetime.utcnow().strftime("%Y%m%d")
    end_date = (datetime.utcnow() + timedelta(days=days_ahead)).strftime("%Y%m%d")
    dates_param = f"dates={today}-{end_date}"

    url = f"{base_url}{SPORTS[sport]}/scoreboard?{dates_param}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        games = []
        for event in data.get("events", []):
            comp = event["competitions"][0]
            teams = comp["competitors"]

            # Determine home/away
            home = next(t for t in teams if t["homeAway"] == "home")
            away = next(t for t in teams if t["homeAway"] == "away")

            game = {
                "game_id": event["id"],
                "sport": sport.upper(),
                "team_a": f"{away['team']['location']} {away['team']['name']}".strip(),  # away first
                "team_b": f"{home['team']['location']} {home['team']['name']}".strip(),  # home second
                "scheduled_date": event["date"],  # ISO UTC
                "result": None,
            }

            # If game completed, set winner
            if comp["status"]["type"]["completed"]:
                winner = next((t["team"]["displayName"] for t in teams if t.get("winner")), None)
                game["result"] = winner

            games.append(game)

        print(f"Fetched {len(games)} {sport.upper()} games")
        return games

    except Exception as e:
        print(f"ESPN fetch failed ({sport}): {str(e)}")
        return []


def upsert_games(games: List[Dict]):
    if not games:
        return
    success = 0
    for g in games:
        try:
            supabase.table("games").upsert(g, on_conflict="game_id").execute()
            success += 1
        except Exception as e:
            print(f"Upsert failed {g['team_a']} vs {g['team_b']}: {e}")
    print(f"Updated {success}/{len(games)} games")


if __name__ == "__main__":
    games = fetch_games("nba")
    upsert_games(games)

