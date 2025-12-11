"""
Mines API endpoints - Add to backend/main.py before 'if __name__' block
"""

# Add these imports at the top of backend/main.py:
# from backend.mines import get_predictor, demo_games

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
        stats = predictor.calculate_game_stats(game_id, game["revealed_tiles"])
        
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
            game["revealed_tiles"]
        )
        
        return {
            "game_id": game_id,
            "total_predictions": len(predictions),
            "tiles": predictions[:20],  # Top 20 safest tiles
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mines/click/{game_id}")
async def record_mines_click(game_id: str, x: int, y: int, is_safe: bool):
    """Record a tile click and update game"""
    try:
        if game_id not in demo_games:
            raise HTTPException(status_code=404, detail="Game not found")
        
        game = demo_games[game_id]
        
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
        predictor = get_predictor()
        predictions = predictor.get_tile_predictions(
            game_id,
            game["grid_size"],
            game["revealed_tiles"]
        )
        stats = predictor.calculate_game_stats(game_id, game["revealed_tiles"])
        
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
    """Get mines game analytics across all games"""
    try:
        if not demo_games:
            return {
                "total_games": 0,
                "active_games": 0,
                "completed_games": 0,
                "avg_safe_clicks": 0,
                "avg_prediction_accuracy": 0
            }
        
        total_games = len(demo_games)
        active_games = sum(1 for g in demo_games.values() if g["status"] == "active")
        completed_games = total_games - active_games
        
        all_stats = []
        for game in demo_games.values():
            predictor = get_predictor()
            stats = predictor.calculate_game_stats(game["game_id"], game["revealed_tiles"])
            all_stats.append(stats)
        
        avg_safe_clicks = np.mean([s["safe_clicks"] for s in all_stats]) if all_stats else 0
        avg_accuracy = np.mean([s["win_percentage"] for s in all_stats]) if all_stats else 0
        
        return {
            "total_games": total_games,
            "active_games": active_games,
            "completed_games": completed_games,
            "avg_safe_clicks": round(avg_safe_clicks, 2),
            "avg_prediction_accuracy": round(avg_accuracy, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
