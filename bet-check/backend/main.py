"""
Sports Prediction Tool - FastAPI Backend
This service handles game predictions using weighted factors and adaptive learning.

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import numpy as np
from datetime import datetime
from supabase import create_client, Client
import stripe

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
    """Fetch current games from ESPN API - NBA focus"""
    try:
        import requests
        from datetime import timedelta
        
        # ESPN API endpoint - NBA focused
        sport_path = "basketball/nba"
        
        all_games = []
        
        for days_ahead in range(5):  # Next 5 days
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
                                    "game_id": f"nba_{event.get('id')}",
                                    "sport": "nba",
                                    "team_a": competitors[0].get("team", {}).get("displayName", "Unknown"),
                                    "team_b": competitors[1].get("team", {}).get("displayName", "Unknown"),
                                    "scheduled_date": event.get("date", "")[:10],
                                    "result": None
                                })
                        except Exception as e:
                            continue
                    
                    if events:
                        print(f"✓ Loaded {len(events)} NBA games for {date_str}")
            except Exception as e:
                print(f"⚠ Failed to fetch NBA games: {e}")
                continue
        
        print(f"📊 Total games loaded: {len(all_games)}")
        return all_games if all_games else None
    except Exception as e:
        print(f"✗ Error fetching live games: {e}")
        return None

DEMO_GAMES = fetch_live_games() or [
    {"game_id": "nba_demo_1", "sport": "nba", "team_a": "Los Angeles Lakers", "team_b": "Boston Celtics", "scheduled_date": datetime.now().strftime("%Y-%m-%d"), "result": None},
    {"game_id": "nba_demo_2", "sport": "nba", "team_a": "Golden State Warriors", "team_b": "Denver Nuggets", "scheduled_date": datetime.now().strftime("%Y-%m-%d"), "result": None},
]

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
                game["verified"] = True
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

@app.post("/verify_result/{game_id}")
async def verify_result(game_id: str, is_correct: bool):
    """
    Verify that result is accurate
    
    Params:
        game_id: Game ID
        is_correct: True if result is accurate, False if incorrect
    
    Returns:
        Confirmation with adaptive learning status
    """
    try:
        global DEMO_GAMES
        
        # Find game
        game = next((g for g in DEMO_GAMES if g["game_id"] == game_id), None)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        if not game.get("result"):
            raise HTTPException(status_code=400, detail="No result to verify for this game")
        
        # Mark as verified
        game["verified"] = True
        
        # Only trigger learning if result was correct
        if is_correct:
            print(f"✅ Result verified as CORRECT: {game_id}")
            
            # Trigger adaptive learning
            PredictionEngine.update_weights(game_id, game["result"])
            
            if supabase:
                supabase.table("results").insert({
                    "game_id": game_id,
                    "actual_outcome": game["result"],
                    "verification_type": "auto_verified",
                    "created_at": datetime.utcnow().isoformat()
                }).execute()
            
            return {
                "status": "success",
                "message": f"Result verified for {game_id}",
                "weights_updated": True,
                "verification_type": "auto_verified"
            }
        else:
            print(f"❌ Result marked as INCORRECT: {game_id}")
            
            if supabase:
                supabase.table("results").insert({
                    "game_id": game_id,
                    "actual_outcome": game["result"],
                    "verification_type": "auto_rejected",
                    "created_at": datetime.utcnow().isoformat()
                }).execute()
            
            return {
                "status": "rejected",
                "message": f"Result for {game_id} marked as incorrect",
                "weights_updated": False,
                "verification_type": "auto_rejected"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/games/status/{game_id}")
async def get_game_status(game_id: str):
    """
    Get game status including result and verification status
    """
    try:
        # Find game
        game = next((g for g in DEMO_GAMES if g["game_id"] == game_id), None)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        verification_type = None
        if game.get("result"):
            if supabase:
                try:
                    result_response = supabase.table("results").select("verification_type").eq(
                        "game_id", game_id
                    ).order("created_at", desc=True).limit(1).execute()
                    
                    if result_response.data:
                        verification_type = result_response.data[0].get("verification_type", "auto")
                except:
                    verification_type = "auto" if not game.get("verified") else "unknown"
            else:
                verification_type = "auto" if not game.get("verified") else "unknown"
        
        return {
            "game_id": game_id,
            "has_result": game.get("result") is not None,
            "result": game.get("result"),
            "team_a": game.get("team_a"),
            "team_b": game.get("team_b"),
            "score_a": game.get("score_a"),
            "score_b": game.get("score_b"),
            "verified": game.get("verified", False),
            "verification_type": verification_type
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

# ==================== Stripe Webhook ====================

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """
    Stripe webhook handler for subscription payments
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        if event.type == "checkout.session.completed":
            print("Subscription success:", event.data.object.customer)
            # TODO: later → update user premium status in DB
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(400, "Webhook error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

