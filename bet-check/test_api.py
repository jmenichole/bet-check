"""
Example API usage and testing
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_health():
    """Test health check"""
    print("Testing health check...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_get_games():
    """Test getting games list"""
    print("Fetching games...")
    response = requests.get(f"{API_BASE}/games?sport=nba")
    print(f"Status: {response.status_code}")
    print(f"Games found: {len(response.json())}")
    if response.json():
        print("First game:")
        print(json.dumps(response.json()[0], indent=2))
    print()

def test_get_prediction(game_id: str):
    """Test getting prediction"""
    print(f"Getting prediction for {game_id}...")
    response = requests.get(f"{API_BASE}/predict/{game_id}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_log_result(game_id: str, actual_outcome: str):
    """Test logging result"""
    print(f"Logging result for {game_id}...")
    payload = {
        "game_id": game_id,
        "actual_outcome": actual_outcome
    }
    response = requests.post(
        f"{API_BASE}/log_result",
        json=payload
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_get_factors():
    """Test getting factors"""
    print("Fetching factors...")
    response = requests.get(f"{API_BASE}/factors")
    print(f"Status: {response.status_code}")
    print(f"Factors found: {len(response.json())}")
    for factor in response.json():
        print(f"  - {factor['name']}: {factor['current_weight']} (base: {factor['base_weight']})")
    print()

def test_get_analytics():
    """Test getting analytics"""
    print("Fetching analytics...")
    response = requests.get(f"{API_BASE}/analytics")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Bet Check - API Testing")
    print("=" * 60)
    print()

    try:
        # Test basic endpoints
        test_health()
        test_get_factors()
        test_get_games()
        test_get_analytics()

        # Get first game and test prediction
        games_response = requests.get(f"{API_BASE}/games?sport=nba")
        if games_response.json():
            game = games_response.json()[0]
            test_get_prediction(game["game_id"])

            # Example: log a result
            # test_log_result(game["game_id"], game["team_a"])

        print("=" * 60)
        print("✓ All tests completed!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        print("Make sure the backend is running: python backend/main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
