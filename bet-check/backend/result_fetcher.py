"""
Automated ESPN Result Fetcher
Periodically fetches game results from ESPN API and updates predictions
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
import threading
import time

class ESPNResultFetcher:
    """Fetches completed game results from ESPN and updates accuracy"""
    
    def __init__(self):
        self.sports_endpoints = {
            "nba": "basketball/nba",
            "nfl": "football/nfl",
            "mlb": "baseball/mlb",
            "nhl": "hockey/nhl",
            "ncaaf": "football/college-football",
            "ncaab": "basketball/mens-college-basketball",
        }
        self.processed_games = set()  # Track already processed results
        self.running = False
    
    def fetch_game_result(self, sport: str, game_id: str) -> Optional[str]:
        """
        Fetch specific game result from ESPN API
        Returns winner name or None if game not found/not completed
        """
        try:
            if sport not in self.sports_endpoints:
                return None
            
            sport_path = self.sports_endpoints[sport]
            # ESPN game ID is the numeric part after sport_
            espn_id = game_id.split("_", 1)[1] if "_" in game_id else game_id
            
            url = f"http://site.api.espn.com/apis/site/v2/sports/{sport_path}/summary?id={espn_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                competition = data.get("competitions", [{}])[0]
                
                # Check if game is complete
                status = competition.get("status", {})
                if status.get("type", {}).get("completed", False):
                    # Find winner
                    competitors = competition.get("competitors", [])
                    if len(competitors) >= 2:
                        # Winner is competitor with higher score
                        if competitors[0].get("winner"):
                            return competitors[0].get("team", {}).get("displayName", "Unknown")
                        elif competitors[1].get("winner"):
                            return competitors[1].get("team", {}).get("displayName", "Unknown")
                    
                    return None
            
            return None
        except Exception as e:
            print(f"Error fetching result for {game_id}: {e}")
            return None
    
    def fetch_daily_results(self, lookback_days: int = 2) -> Dict[str, str]:
        """
        Fetch all completed games from last N days
        Returns dict of {game_id: winning_team}
        """
        results = {}
        
        try:
            for sport_key, sport_path in self.sports_endpoints.items():
                for days_back in range(lookback_days + 1):  # Include today
                    try:
                        target_date = datetime.now() - timedelta(days=days_back)
                        date_str = target_date.strftime("%Y%m%d")
                        url = f"http://site.api.espn.com/apis/site/v2/sports/{sport_path}/scoreboard?dates={date_str}"
                        
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            events = data.get("events", [])
                            
                            for event in events:
                                try:
                                    comps = event.get("competitions", [{}])[0]
                                    
                                    # Check if game is complete
                                    status = comps.get("status", {})
                                    if status.get("type", {}).get("completed", False):
                                        competitors = comps.get("competitors", [])
                                        if len(competitors) >= 2:
                                            game_id = f"{sport_key}_{event.get('id')}"
                                            
                                            # Find winner
                                            if competitors[0].get("winner"):
                                                winner = competitors[0].get("team", {}).get("displayName", "Unknown")
                                            elif competitors[1].get("winner"):
                                                winner = competitors[1].get("team", {}).get("displayName", "Unknown")
                                            else:
                                                continue
                                            
                                            # Only process if not already processed
                                            if game_id not in self.processed_games:
                                                results[game_id] = winner
                                                self.processed_games.add(game_id)
                                except Exception as e:
                                    continue
                    except Exception as e:
                        print(f"Error fetching {sport_key} results for {date_str}: {e}")
                        continue
        except Exception as e:
            print(f"Error in fetch_daily_results: {e}")
        
        return results
    
    def start_background_fetcher(self, update_callback, interval_hours: int = 6):
        """
        Start background thread to periodically fetch results
        update_callback: function to call when results found (game_id, winner)
        """
        def fetcher_loop():
            print(f"🔄 ESPN Result Fetcher started (checking every {interval_hours} hours)")
            while self.running:
                try:
                    results = self.fetch_daily_results(lookback_days=3)
                    
                    if results:
                        print(f"📊 Found {len(results)} new game results")
                        for game_id, winner in results.items():
                            print(f"  ✓ {game_id}: {winner}")
                            update_callback(game_id, winner)
                    
                    # Wait before next check
                    time.sleep(interval_hours * 3600)
                except Exception as e:
                    print(f"Error in result fetcher loop: {e}")
                    time.sleep(300)  # Wait 5 min before retry
        
        self.running = True
        thread = threading.Thread(target=fetcher_loop, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        """Stop the background fetcher"""
        self.running = False
