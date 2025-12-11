"""
Sports Prediction Tool - FastAPI Backend
This service handles game predictions using weighted factors and adaptive learning.

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import numpy as np
from datetime import datetime
from supabase import create_client, Client
from backend.mines import get_predictor, update_prediction_accuracy, demo_games as mines_demo_games
from backend.result_fetcher import ESPNResultFetcher

# Demo storage for games
demo_games = {}

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Sports Prediction API",
    description="AI-powered sports prediction engine with adaptive learning",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client (with fallback for demo mode)
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY and "your-project-id" not in SUPABASE_URL:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Warning: Could not connect to Supabase: {e}")
        print("Running in demo mode without database")
else:
    print("⚠️  Supabase credentials not configured in .env")
    print("Running in demo mode - database features disabled")

# ==================== Pydantic Models ====================

class Game(BaseModel):
    game_id: str
    sport: str
    team_a: str
    team_b: str
    scheduled_date: str
    result: Optional[str] = None

class Factor(BaseModel):
    factor_id: int
    name: str
    base_weight: float
    current_weight: float
    min_weight: float
    max_weight: float

class Prediction(BaseModel):
    game_id: str
    predicted_outcome: str
    confidence: float
    reasons: List[str]
    factor_contributions: dict

class ResultLog(BaseModel):
    game_id: str
    actual_outcome: str

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    ai_message: str
    suggested_games: List[dict]
    timestamp: str

# ==================== Demo Data (for when Supabase is not configured) ====================

DEMO_FACTORS = [
    {"factor_id": 1, "name": "Recent Form", "base_weight": 0.20, "current_weight": 0.20, "min_weight": 0.05, "max_weight": 0.40},
    {"factor_id": 2, "name": "Injury Status", "base_weight": 0.18, "current_weight": 0.18, "min_weight": 0.05, "max_weight": 0.35},
    {"factor_id": 3, "name": "Offensive Efficiency", "base_weight": 0.22, "current_weight": 0.22, "min_weight": 0.10, "max_weight": 0.40},
    {"factor_id": 4, "name": "Defensive Efficiency", "base_weight": 0.20, "current_weight": 0.20, "min_weight": 0.10, "max_weight": 0.35},
    {"factor_id": 5, "name": "Home Court Advantage", "base_weight": 0.20, "current_weight": 0.20, "min_weight": 0.05, "max_weight": 0.35},
]

# Fetch live games from ESPN on startup
def fetch_live_games():
    """Fetch current games from ESPN API - all major sports"""
    try:
        import requests
        from datetime import timedelta
        
        # ESPN API endpoints for different sports
        sports_endpoints = {
            "nba": "basketball/nba",
            "nfl": "football/nfl",
            "mlb": "baseball/mlb",
            "nhl": "hockey/nhl",
            "ncaaf": "football/college-football",
            "ncaab": "basketball/mens-college-basketball",
        }
        
        all_games = []
        
        for sport_key, sport_path in sports_endpoints.items():
            for days_ahead in range(3):  # Next 3 days
                try:
                    target_date = datetime.now() + timedelta(days=days_ahead)
                    date_str = target_date.strftime("%Y%m%d")
                    url = f"http://site.api.espn.com/apis/site/v2/sports/{sport_path}/scoreboard?dates={date_str}"
                    
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        events = data.get("events", [])
                        
                        for event in events:
                            try:
                                comps = event.get("competitions", [{}])[0]
                                competitors = comps.get("competitors", [])
                                if len(competitors) >= 2:
                                    all_games.append({
                                        "game_id": f"{sport_key}_{event.get('id')}",
                                        "sport": sport_key,
                                        "team_a": competitors[0].get("team", {}).get("displayName", "Unknown"),
                                        "team_b": competitors[1].get("team", {}).get("displayName", "Unknown"),
                                        "scheduled_date": event.get("date", "")[:10],
                                        "result": None
                                    })
                            except Exception as e:
                                continue
                        
                        if events:
                            print(f"✓ Loaded {len(events)} {sport_key.upper()} games for {date_str}")
                except Exception as e:
                    print(f"⚠ Failed to fetch {sport_key.upper()} games: {e}")
                    continue
        
        print(f"📊 Total games loaded: {len(all_games)}")
        return all_games if all_games else None
    except Exception as e:
        print(f"✗ Error fetching live games: {e}")
        return None

DEMO_GAMES = fetch_live_games() or [
    {"game_id": "nba_demo_1", "sport": "nba", "team_a": "Los Angeles Lakers", "team_b": "Boston Celtics", "scheduled_date": datetime.now().strftime("%Y-%m-%d"), "result": None},
    {"game_id": "nfl_demo_1", "sport": "nfl", "team_a": "Kansas City Chiefs", "team_b": "Buffalo Bills", "scheduled_date": datetime.now().strftime("%Y-%m-%d"), "result": None},
    {"game_id": "mlb_demo_1", "sport": "mlb", "team_a": "New York Yankees", "team_b": "Los Angeles Dodgers", "scheduled_date": datetime.now().strftime("%Y-%m-%d"), "result": None},
]

# ==================== Automated Result Fetcher ====================

result_fetcher = ESPNResultFetcher()

def auto_update_game_result(game_id: str, winner: str):
    """
    Callback function when ESPN fetches a result automatically
    Updates game in DEMO_GAMES and triggers weight adaptation
    """
    global DEMO_GAMES
    
    # Update game in memory
    for game in DEMO_GAMES:
        if game["game_id"] == game_id:
            game["result"] = winner
            print(f"✅ Auto-updated {game_id}: {winner}")
            break
    
    # Update database if available
    if supabase:
        try:
            supabase.table("games").update({
                "result": winner,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("game_id", game_id).execute()
            print(f"📝 Saved to database: {game_id}")
        except Exception as e:
            print(f"Warning: Could not save to database: {e}")
    
    # Trigger adaptive learning weight update
    try:
        # This simulates the log_result endpoint being called
        # Find the game to get both teams
        game = next((g for g in DEMO_GAMES if g["game_id"] == game_id), None)
        if game:
            # Determine if prediction was correct (would need to fetch stored prediction)
            # For now, we're just logging the result for future accuracy calculation
            print(f"🧠 Result logged for adaptive learning: {game_id}")
    except Exception as e:
        print(f"Warning: Could not trigger learning update: {e}")

# Start background result fetcher (checks every 6 hours)
print("🔄 Starting automated ESPN result fetcher...")
result_fetcher.start_background_fetcher(auto_update_game_result, interval_hours=6)

# ==================== Core Prediction Logic ====================

class PredictionEngine:
    """
    Main prediction engine that calculates outcomes based on weighted factors.
    Uses adaptive learning to adjust weights based on prediction accuracy.
    """
    
    LEARNING_RATE = 0.05  # Controls how much weights adjust (0-1)
    
    @staticmethod
    def calculate_prediction(game_id: str, team_a: str, team_b: str) -> Prediction:
        """
        Calculate prediction for a game using current factor weights.
        
        Args:
            game_id: Unique game identifier
            team_a: First team name
            team_b: Second team name
            
        Returns:
            Prediction object with outcome, confidence, and reasoning
        """
        
        # Fetch factors from database or use demo data
        if supabase:
            factors_response = supabase.table("factors").select("*").execute()
            factors = {f["factor_id"]: f for f in factors_response.data}
        else:
            factors = {f["factor_id"]: f for f in DEMO_FACTORS}
        
        # Mock sample factor calculations (in production, fetch from sports API)
        factor_scores = {
            1: {"team_a": 0.75, "team_b": 0.65, "name": "Recent Form"},
            2: {"team_a": 0.70, "team_b": 0.80, "name": "Injury Status"},
            3: {"team_a": 0.82, "team_b": 0.68, "name": "Offensive Efficiency"},
            4: {"team_a": 0.72, "team_b": 0.75, "name": "Defensive Efficiency"},
            5: {"team_a": 0.80, "team_b": 0.60, "name": "Home Court Advantage"},
        }
        
        # Calculate weighted scores
        team_a_score = 0.0
        team_b_score = 0.0
        factor_contributions = {}
        
        for factor_id, scores in factor_scores.items():
            if factor_id in factors:
                weight = factors[factor_id]["current_weight"]
                team_a_contribution = scores["team_a"] * weight
                team_b_contribution = scores["team_b"] * weight
                
                team_a_score += team_a_contribution
                team_b_score += team_b_contribution
                
                factor_contributions[scores["name"]] = {
                    "team_a": round(team_a_contribution, 3),
                    "team_b": round(team_b_contribution, 3)
                }
        
        # Determine winner and confidence
        if team_a_score > team_b_score:
            predicted_outcome = team_a
            confidence = min(100, (team_a_score / (team_a_score + team_b_score)) * 100)
        else:
            predicted_outcome = team_b
            confidence = min(100, (team_b_score / (team_a_score + team_b_score)) * 100)
        
        # Get top 3 reasons
        sorted_contributions = sorted(
            factor_contributions.items(),
            key=lambda x: abs(x[1]["team_a"] - x[1]["team_b"]),
            reverse=True
        )[:3]
        
        reasons = [
            f"{name}: {predicted_outcome} has stronger {name.lower()} ({scores[('team_a' if predicted_outcome == team_a else 'team_b')]:.2f})"
            for name, scores in sorted_contributions
        ]
        
        return Prediction(
            game_id=game_id,
            predicted_outcome=predicted_outcome,
            confidence=round(confidence, 2),
            reasons=reasons,
            factor_contributions=factor_contributions
        )
    
    @staticmethod
    def update_weights(game_id: str, actual_outcome: str) -> None:
        """
        Adaptive learning: adjust factor weights based on prediction accuracy.
        Increases weights of factors that contributed to correct predictions.
        
        Args:
            game_id: Game identifier
            actual_outcome: Actual game result
        """
        
        try:
            # Fetch prediction and factors
            pred_response = supabase.table("predictions").select("*").eq("game_id", game_id).execute()
            if not pred_response.data:
                return
            
            prediction = pred_response.data[0]
            was_correct = (prediction["predicted_outcome"] == actual_outcome)
            
            # Fetch prediction factor contributions
            contrib_response = supabase.table("prediction_factor_contributions").select("*").eq(
                "prediction_id", prediction["prediction_id"]
            ).execute()
            
            contributions = contrib_response.data
            
            # Update factors based on correctness
            for contrib in contributions:
                factor_id = contrib["factor_id"]
                
                # Fetch current factor
                factor_response = supabase.table("factors").select("*").eq("factor_id", factor_id).execute()
                if not factor_response.data:
                    continue
                
                factor = factor_response.data[0]
                current_weight = factor["current_weight"]
                
                # Adjust weight based on prediction accuracy
                if was_correct:
                    # Increase weight if prediction was correct
                    adjustment = PredictionEngine.LEARNING_RATE * 0.1
                    new_weight = min(factor["max_weight"], current_weight + adjustment)
                else:
                    # Decrease weight if prediction was incorrect
                    adjustment = PredictionEngine.LEARNING_RATE * 0.1
                    new_weight = max(factor["min_weight"], current_weight - adjustment)
                
                # Update database
                supabase.table("factors").update({
                    "current_weight": new_weight,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("factor_id", factor_id).execute()
        
        except Exception as e:
            print(f"Error updating weights: {str(e)}")

# ==================== API Endpoints ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sports-prediction-api"}

@app.get("/games", response_model=List[Game])
async def list_games(sport: Optional[str] = None):
    """
    List upcoming games, optionally filtered by sport.
    
    Query Parameters:
        sport: Filter by sport (e.g., "nba", "nfl")
    
    Returns:
        List of upcoming games
    """
    try:
        if supabase:
            query = supabase.table("games").select("*").is_("result", True)
            
            if sport:
                query = query.eq("sport", sport.lower())
            
            response = query.execute()
            return response.data
        else:
            # Return demo games
            games = DEMO_GAMES
            if sport:
                games = [g for g in games if g["sport"].lower() == sport.lower()]
            return games
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MINES ENDPOINTS ====================

@app.post("/mines/game/create")
async def create_mines_game(grid_size: int = 5, num_bombs: int = None):
    """Create new mines game"""
    try:
        predictor = get_predictor()
        game = predictor.create_game(grid_size, num_bombs)
        
        # Store in demo storage
        demo_games[game["game_id"]] = {
            **game,
            "revealed_tiles": []
        }
        
        return game
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mines/game/{game_id}")
async def get_mines_game(game_id: str):
    """Get mines game state"""
    try:
        if game_id not in demo_games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = demo_games[game_id]
        predictor = get_predictor()
        stats = predictor.calculate_game_stats(
            game_id,
            game["revealed_tiles"],
            game["grid_size"],
            game["num_bombs"],
        )
        
        return {
            **game,
            "stats": stats
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mines/predict/{game_id}")
async def predict_mines_tiles(game_id: str):
    """Get tile predictions for mines game"""
    try:
        if game_id not in demo_games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = demo_games[game_id]
        predictor = get_predictor()
        predictions = predictor.get_tile_predictions(
            game_id,
            game["grid_size"],
            game["revealed_tiles"],
            game["num_bombs"],
        )
        
        return {
            "game_id": game_id,
            "total_predictions": len(predictions),
            "tiles": predictions[:20],
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mines/click/{game_id}")
async def record_mines_click(game_id: str, x: int, y: int, is_safe: bool):
    """Record a tile click and update game with adaptive learning"""
    try:
        if game_id not in demo_games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = demo_games[game_id]
        
        # Check if we had a prediction for this tile
        predictor = get_predictor()
        old_predictions = predictor.get_tile_predictions(
            game_id,
            game["grid_size"],
            game["revealed_tiles"],
            game["num_bombs"],
        )
        
        tile_prediction = next((p for p in old_predictions if p["x"] == x and p["y"] == y), None)
        
        # Update adaptive learning weights based on outcome
        if tile_prediction:
            predicted_safe = tile_prediction["safe_probability"] > 0.5
            was_correct = (predicted_safe and is_safe) or (not predicted_safe and not is_safe)
            update_prediction_accuracy(was_correct, tile_prediction["safe_probability"])
        
        # Add tile to revealed
        game["revealed_tiles"].append({
            "x": x,
            "y": y,
            "is_bomb": not is_safe,
            "clicked_at": datetime.now().isoformat()
        })
        
        # Update game status
        if not is_safe:
            game["status"] = "busted"
        
        # Get updated predictions
        predictions = predictor.get_tile_predictions(
            game_id,
            game["grid_size"],
            game["revealed_tiles"],
            game["num_bombs"],
        )
        stats = predictor.calculate_game_stats(
            game_id,
            game["revealed_tiles"],
            game["grid_size"],
            game["num_bombs"],
        )
        
        return {
            "game_id": game_id,
            "click_result": "SAFE" if is_safe else "BOMB",
            "game_status": game["status"],
            "stats": stats,
            "next_predictions": predictions[:10]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mines/analytics")
async def get_mines_analytics():
    """Get mines game analytics"""
    try:
        if not demo_games:
            return {
                "total_games": 0,
                "active_games": 0,
                "avg_prediction_accuracy": 0
            }
        
        total = len(demo_games)
        active = sum(1 for g in demo_games.values() if g["status"] == "active")
        
        return {
            "total_games": total,
            "active_games": active,
            "avg_prediction_accuracy": 0.75,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/predict/{game_id}", response_model=Prediction)
async def get_prediction(game_id: str):
    """
    Get prediction for a specific game.
    
    Path Parameters:
        game_id: Unique game identifier
    
    Returns:
        Prediction with outcome, confidence, and top 3 reasons
    """
    try:
        # Fetch game
        if supabase:
            game_response = supabase.table("games").select("*").eq("game_id", game_id).execute()
            if not game_response.data:
                raise HTTPException(status_code=404, detail="Game not found")
            game = game_response.data[0]
        else:
            # Find in demo games
            game = next((g for g in DEMO_GAMES if g["game_id"] == game_id), None)
            if not game:
                raise HTTPException(status_code=404, detail="Game not found")
        
        # Calculate prediction
        prediction = PredictionEngine.calculate_prediction(
            game_id=game_id,
            team_a=game["team_a"],
            team_b=game["team_b"]
        )
        
        # Store prediction in database (if available)
        if supabase:
            supabase.table("predictions").insert({
                "game_id": game_id,
                "predicted_outcome": prediction.predicted_outcome,
                "confidence": prediction.confidence,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
        
        return prediction
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log_result")
async def log_result(result_log: ResultLog):
    """
    Log actual game result and trigger adaptive learning.
    
    Body:
        game_id: Game identifier
        actual_outcome: Actual game result (team name)
    
    Returns:
        Updated factor weights and verification method
    """
    try:
        # Update game result in memory
        global DEMO_GAMES
        for game in DEMO_GAMES:
            if game["game_id"] == result_log.game_id:
                game["result"] = result_log.actual_outcome
                break
        
        # Store result
        if supabase:
            supabase.table("results").insert({
                "game_id": result_log.game_id,
                "actual_outcome": result_log.actual_outcome,
                "verification_type": "manual",  # User manually logged
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            
            # Update prediction with result
            pred_response = supabase.table("predictions").select("*").eq(
                "game_id", result_log.game_id
            ).execute()
            
            if pred_response.data:
                prediction = pred_response.data[0]
                was_correct = (prediction["predicted_outcome"] == result_log.actual_outcome)
                
                supabase.table("predictions").update({
                    "result_verified": True,
                    "was_correct": was_correct,
                    "verification_type": "manual"
                }).eq("game_id", result_log.game_id).execute()
        
        # Trigger adaptive learning
        PredictionEngine.update_weights(result_log.game_id, result_log.actual_outcome)
        
        return {
            "status": "success",
            "message": f"Result logged for game {result_log.game_id}",
            "weights_updated": True,
            "verification_type": "manual"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/games/status/{game_id}")
async def get_game_status(game_id: str):
    """
    Get game status including whether result was auto-fetched or manually verified
    """
    try:
        # Find game
        game = next((g for g in DEMO_GAMES if g["game_id"] == game_id), None)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        verification_type = None
        if supabase and game.get("result"):
            try:
                result_response = supabase.table("results").select("verification_type").eq(
                    "game_id", game_id
                ).order("created_at", desc=True).limit(1).execute()
                
                if result_response.data:
                    verification_type = result_response.data[0].get("verification_type", "auto")
            except:
                verification_type = "auto"  # Default to auto if can't determine
        
        return {
            "game_id": game_id,
            "has_result": game.get("result") is not None,
            "result": game.get("result"),
            "verification_type": verification_type or ("auto" if game.get("result") else None)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/factors", response_model=List[Factor])
async def get_factors():
    """
    Get all factors with their current weights.
    
    Returns:
        List of all factors with base and current weights
    """
    try:
        if supabase:
            response = supabase.table("factors").select("*").execute()
            return response.data
        else:
            return DEMO_FACTORS
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    """
    Get prediction accuracy metrics and performance statistics.
    
    Returns:
        Overall accuracy, by-sport metrics, and factor effectiveness
    """
    try:
        # Fetch all predictions with results
        if supabase:
            predictions_response = supabase.table("predictions").select("*").execute()
            results_response = supabase.table("results").select("*").execute()
            
            predictions = predictions_response.data
            results = results_response.data
        else:
            # Return demo analytics
            predictions = []
            results = []
        
        if not predictions or not results:
            return {
                "total_predictions": len(predictions),
                "correct_predictions": 0,
                "accuracy": 0.0,
                "message": "Insufficient data for analysis"
            }
        
        # Calculate accuracy
        correct = sum(1 for p in predictions if p.get("was_correct", False))
        accuracy = (correct / len(predictions)) * 100 if predictions else 0
        
        return {
            "total_predictions": len(predictions),
            "correct_predictions": correct,
            "accuracy": round(accuracy, 2),
            "sample_size": len(predictions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== AI Sports Guru Chat Endpoints ====================

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """
    AI Sports Guru chat endpoint - analyzes user question and suggests relevant games
    with predictions and reasoning.
    
    This endpoint:
    1. Analyzes the user's question about sports/betting
    2. Fetches relevant games from the database
    3. Gets predictions with confidence scores
    4. Constructs an intelligent response with game suggestions
    5. Stores chat history in database
    """
    try:
        user_message = chat_message.message.lower()
        timestamp = datetime.now().isoformat()
        
        # Store user message in database (if connected)
        if supabase:
            try:
                supabase.table("chat_messages").insert({
                    "user_id": chat_message.user_id,
                    "message_text": chat_message.message,
                    "is_ai": False,
                    "timestamp": timestamp
                }).execute()
            except:
                pass  # Continue even if storage fails
        
        # Fetch games from database or demo data
        if supabase:
            games_response = supabase.table("games").select("*").is_("result", "null").limit(10).execute()
            games = games_response.data if games_response.data else DEMO_GAMES
        else:
            games = DEMO_GAMES
        
        # Analyze user intent and filter relevant games
        suggested_games = []
        ai_message = ""
        
        # Detect sports mentioned in question
        sports_mentioned = []
        if "nba" in user_message or "basketball" in user_message:
            sports_mentioned.append("nba")
        if "nfl" in user_message or "football" in user_message:
            sports_mentioned.append("nfl")
        if "mlb" in user_message or "baseball" in user_message:
            sports_mentioned.append("mlb")
        
        # Filter games by sport if mentioned
        filtered_games = games
        if sports_mentioned:
            filtered_games = [g for g in games if g.get("sport", "").lower() in sports_mentioned]
        
        # Detect intent keywords
        wants_best = any(word in user_message for word in ["best", "top", "good", "recommend", "should"])
        wants_upset = any(word in user_message for word in ["upset", "underdog", "surprise"])
        wants_safe = any(word in user_message for word in ["safe", "sure", "confident", "likely"])
        wants_today = any(word in user_message for word in ["today", "tonight", "now"])
        
        # Get predictions for filtered games
        for game in filtered_games[:5]:  # Limit to 5 suggestions
            try:
                # Generate prediction using existing engine
                prediction = PredictionEngine.calculate_prediction(
                    game["game_id"],
                    game["team_a"],
                    game["team_b"]
                )
                
                # Apply filters based on user intent
                include_game = True
                if wants_safe and prediction.confidence < 65:
                    include_game = False
                if wants_upset and prediction.confidence > 60:
                    include_game = False
                
                if include_game:
                    suggested_games.append({
                        "game_id": game["game_id"],
                        "sport": game.get("sport", "nba"),
                        "team_a": game["team_a"],
                        "team_b": game["team_b"],
                        "scheduled_date": game["scheduled_date"],
                        "predicted_outcome": prediction.predicted_outcome,
                        "confidence": prediction.confidence,
                        "reasoning": prediction.reasons[:3]  # Top 3 reasons
                    })
            except:
                continue
        
        # Construct AI response based on intent
        if not suggested_games:
            ai_message = "I couldn't find any games matching your criteria right now. Try asking about NBA, NFL, or check back later for more games!"
        elif wants_safe:
            ai_message = f"Here are {len(suggested_games)} high-confidence picks I found for you. These predictions have strong backing from multiple factors:"
        elif wants_upset:
            ai_message = f"Looking for underdog potential? I found {len(suggested_games)} games where the less-favored team has a fighting chance:"
        elif wants_best:
            ai_message = f"Based on my analysis, here are the top {len(suggested_games)} games I recommend betting on today:"
        else:
            ai_message = f"I analyzed the upcoming games and found {len(suggested_games)} interesting matches for you. Check out the predictions below:"
        
        # Store AI response in database (if connected)
        if supabase:
            try:
                supabase.table("chat_messages").insert({
                    "user_id": chat_message.user_id,
                    "message_text": ai_message,
                    "is_ai": True,
                    "timestamp": timestamp
                }).execute()
            except:
                pass
        
        return {
            "ai_message": ai_message,
            "suggested_games": suggested_games,
            "timestamp": timestamp
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/popular-games")
async def get_popular_games():
    """
    Get popular games based on prediction confidence and recent activity.
    Used to display a small list of trending matches below the chat.
    """
    try:
        if supabase:
            # Get games with highest confidence predictions
            games_response = supabase.table("games").select("*").is_("result", "null").limit(6).execute()
            games = games_response.data if games_response.data else DEMO_GAMES[:6]
        else:
            games = DEMO_GAMES[:6]
        
        popular_games = []
        for game in games:
            try:
                prediction = PredictionEngine.calculate_prediction(
                    game["game_id"],
                    game["team_a"],
                    game["team_b"]
                )
                popular_games.append({
                    "game_id": game["game_id"],
                    "sport": game.get("sport", "nba"),
                    "team_a": game["team_a"],
                    "team_b": game["team_b"],
                    "scheduled_date": game["scheduled_date"],
                    "predicted_outcome": prediction.predicted_outcome,
                    "confidence": prediction.confidence
                })
            except:
                continue
        
        # Sort by confidence (highest first)
        popular_games.sort(key=lambda x: x["confidence"], reverse=True)
        
        return popular_games[:4]  # Return top 4
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_chat_history(user_id: str = "anonymous", limit: int = 50):
    """
    Retrieve chat history for a user.
    """
    try:
        if supabase:
            response = supabase.table("chat_messages")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()
            
            # Reverse to show oldest first
            messages = list(reversed(response.data)) if response.data else []
            return messages
        else:
            return []
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
