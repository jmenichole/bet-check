"""
Seed initial factors into the Supabase database.
Run this once to populate the factors table with base weights.

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"⚠️  Could not connect to Supabase: {e}")
    supabase = None

# Define initial factors with weights
FACTORS = [
    {
        "factor_id": 1,
        "name": "Recent Form",
        "description": "Team performance in last 5 games",
        "base_weight": 0.20,
        "current_weight": 0.20,
        "min_weight": 0.05,
        "max_weight": 0.40,
    },
    {
        "factor_id": 2,
        "name": "Injury Status",
        "description": "Impact of key player injuries",
        "base_weight": 0.18,
        "current_weight": 0.18,
        "min_weight": 0.05,
        "max_weight": 0.35,
    },
    {
        "factor_id": 3,
        "name": "Offensive Efficiency",
        "description": "Points per possession and shooting metrics",
        "base_weight": 0.22,
        "current_weight": 0.22,
        "min_weight": 0.10,
        "max_weight": 0.40,
    },
    {
        "factor_id": 4,
        "name": "Defensive Efficiency",
        "description": "Points allowed per possession",
        "base_weight": 0.20,
        "current_weight": 0.20,
        "min_weight": 0.10,
        "max_weight": 0.40,
    },
    {
        "factor_id": 5,
        "name": "Home Court Advantage",
        "description": "Performance differential at home vs away",
        "base_weight": 0.20,
        "current_weight": 0.20,
        "min_weight": 0.05,
        "max_weight": 0.30,
    },
]

def seed_factors():
    """Populate factors table with initial data."""
    if supabase is None:
        print("⚠️  Supabase not connected. Using demo mode.")
        print("Factors would be:")
        for factor in FACTORS:
            print(f"  • {factor['name']}: {factor['current_weight']}")
        return
    
    try:
        print("Seeding factors into Supabase...")
        
        for factor in FACTORS:
            response = supabase.table("factors").upsert(factor).execute()
            print(f"✓ Seeded factor: {factor['name']}")
        
        print("\n✓ Factors seeded successfully!")
        
    except Exception as e:
        print(f"✗ Error seeding factors: {str(e)}")

if __name__ == "__main__":
    seed_factors()
