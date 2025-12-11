"""
Test AI Sports Guru Chat Endpoints
Verifies all 3 new chat endpoints work correctly

Copyright (c) 2025 Jmenichole
Licensed under CC BY-NC 4.0
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_" + datetime.now().strftime("%Y%m%d_%H%M%S")

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Verify backend is running"""
    print_section("Testing Backend Health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print(f"   Make sure backend is running at {BASE_URL}")
        return False

def test_chat_endpoint():
    """Test POST /chat with various queries"""
    print_section("Testing Chat Endpoint")
    
    test_queries = [
        "Show me the best NBA picks",
        "What are safe bets?",
        "Any NFL upsets?",
        "Today's games"
    ]
    
    all_passed = True
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query, "user_id": TEST_USER_ID},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"   AI Response: {data['ai_message'][:80]}...")
                print(f"   Suggested Games: {len(data['suggested_games'])} games")
                
                if data['suggested_games']:
                    first_game = data['suggested_games'][0]
                    print(f"   Example Game: {first_game['team_a']} vs {first_game['team_b']}")
                    print(f"   Confidence: {first_game['confidence']}%")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Response: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            all_passed = False
    
    return all_passed

def test_popular_games():
    """Test GET /chat/popular-games"""
    print_section("Testing Popular Games Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/chat/popular-games")
        
        if response.status_code == 200:
            games = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Returned {len(games)} popular games")
            
            if games:
                print("\n   Top Games:")
                for i, game in enumerate(games, 1):
                    print(f"   {i}. {game['team_a']} vs {game['team_b']} ({game['sport']})")
                    print(f"      Confidence: {game['confidence']}% | {game['predicted_outcome']}")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_history():
    """Test GET /chat/history"""
    print_section("Testing Chat History Endpoint")
    
    try:
        response = requests.get(
            f"{BASE_URL}/chat/history",
            params={"user_id": TEST_USER_ID}
        )
        
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Retrieved {len(history)} messages")
            
            if history:
                print("\n   Recent Messages:")
                for msg in history[-3:]:  # Show last 3
                    sender = "🤖 AI" if msg['is_ai'] else "👤 User"
                    print(f"   {sender}: {msg['message_text'][:60]}...")
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n🚀 AI Sports Guru Endpoint Test Suite")
    print(f"Testing: {BASE_URL}")
    print(f"User ID: {TEST_USER_ID}")
    
    results = {
        "Backend Health": test_health(),
        "Chat Endpoint": test_chat_endpoint(),
        "Popular Games": test_popular_games(),
        "Chat History": test_chat_history()
    }
    
    # Summary
    print_section("Test Results Summary")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AI Sports Guru is ready to use.")
        print(f"\nNext steps:")
        print(f"1. Start frontend: cd frontend && npm run dev")
        print(f"2. Open http://localhost:3000/guru")
        print(f"3. Apply database migration: schema_chat.sql")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
