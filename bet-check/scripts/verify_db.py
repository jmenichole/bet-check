"""
Example database verification script

Copyright (c) 2025 Jamie McNichol
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY not set in .env")
    exit(1)

supabase: Client = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"⚠️  Could not connect to Supabase: {e}")
    supabase = None

def verify_tables():
    """Verify all required tables exist and have data"""
    if supabase is None:
        print("⚠️  Supabase not connected. Demo mode - database verification skipped.")
        return
    
    print("Verifying Supabase database...")
    print()

    tables = {
        "games": "Upcoming games",
        "factors": "Prediction factors",
        "predictions": "Stored predictions",
        "results": "Game results",
        "prediction_factor_contributions": "Factor contributions to predictions"
    }

    for table_name, description in tables.items():
        try:
            response = supabase.table(table_name).select("*").limit(1).execute()
            count_response = supabase.table(table_name).select("*", count="exact").execute()
            count = count_response.count or 0

            status = "✓" if count > 0 else "⚠"
            print(f"{status} {table_name:35} - {count:3d} rows | {description}")

        except Exception as e:
            print(f"✗ {table_name:35} - Error: {str(e)}")

    print()

def verify_factors():
    """Display current factor weights"""
    print("Current Factor Weights:")
    print("-" * 80)

    if supabase is None:
        print("Supabase not connected. Demo mode.")
        print("  • Recent Form: 0.200")
        print("  • Injury Status: 0.180")
        print("  • Offensive Efficiency: 0.220")
        print("  • Defensive Efficiency: 0.200")
        print("  • Home Court Advantage: 0.200")
        return

    try:
        response = supabase.table("factors").select("*").execute()
        factors = response.data

        if not factors:
            print("No factors found. Run: python scripts/seed_factors.py")
            return

        for factor in factors:
            base = factor["base_weight"]
            current = factor["current_weight"]
            change = current - base
            change_pct = (change / base * 100) if base else 0

            print(f"{factor['name']:25} | Base: {base:6.3f} | Current: {current:6.3f} | Change: {change_pct:+6.1f}%")

    except Exception as e:
        print(f"Error fetching factors: {str(e)}")

    print()

def verify_games():
    """Display upcoming games"""
    print("Upcoming Games:")
    print("-" * 80)

    if supabase is None:
        print("Supabase not connected. Demo mode.")
        print("  • Los Angeles Lakers vs Boston Celtics")
        print("  • Golden State Warriors vs Denver Nuggets")
        print("  • Miami Heat vs Milwaukee Bucks")
        print("  • Phoenix Suns vs Memphis Grizzlies")
        return

    try:
        response = supabase.table("games").select("*").limit(5).execute()
        games = response.data

        if not games:
            print("No games found. Run: python scripts/update_games.py")
            return

        for game in games:
            print(f"{game['team_a']:25} vs {game['team_b']:25} | {game['scheduled_date']}")

    except Exception as e:
        print(f"Error fetching games: {str(e)}")

    print()

if __name__ == "__main__":
    print("=" * 80)
    print("Supabase Database Verification")
    print("=" * 80)
    print()

    verify_tables()
    verify_factors()
    verify_games()

    print("=" * 80)
    print("Verification complete!")
    print("=" * 80)
