"""
Mines Game Predictor - Tile safety prediction and game analysis
Uses probability models to predict safe vs bomb tiles

Copyright (c) 2025 Jmenichole
Licensed under MIT License
"""

import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime
import uuid

class MinesPredictor:
    """Predicts tile safety in mines game with adaptive learning"""
    
    def __init__(self):
        # Grid presets with sane bomb ranges so users can customize difficulty
        self.grid_configs = {
            5: {"tiles": 25, "default_bombs": 3, "min_bombs": 1, "max_bombs": 10},
            6: {"tiles": 36, "default_bombs": 5, "min_bombs": 2, "max_bombs": 14},
            8: {"tiles": 64, "default_bombs": 8, "min_bombs": 4, "max_bombs": 26},
            10: {"tiles": 100, "default_bombs": 15, "min_bombs": 6, "max_bombs": 40},
        }
        
        # Adaptive learning weights (adjust based on prediction accuracy)
        self.adjacency_weight = 0.15  # Weight for adjacency bonus
        self.base_confidence = 0.7    # Base confidence level
        self.prediction_history = []  # Track predictions vs outcomes
    
    def create_game(self, grid_size: int, num_bombs: int = None):
        """Create new mines game with configurable bomb count"""
        if grid_size not in self.grid_configs:
            raise ValueError(f"Invalid grid size: {grid_size}")

        config = self.grid_configs[grid_size]
        total_tiles = config["tiles"]
        min_bombs = max(1, config.get("min_bombs", 1))
        max_bombs = min(config.get("max_bombs", total_tiles - 1), total_tiles - 1)

        if num_bombs is None:
            num_bombs = config["default_bombs"]

        if num_bombs < min_bombs or num_bombs > max_bombs:
            raise ValueError(
                f"Bombs must be between {min_bombs} and {max_bombs} for a {grid_size}x{grid_size} grid"
            )
        
        game_id = f"mines_{grid_size}_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        
        # Initialize grid with random bomb placement
        grid = np.zeros((grid_size, grid_size), dtype=int)
        bomb_positions = np.random.choice(total_tiles, num_bombs, replace=False)
        for pos in bomb_positions:
            row, col = divmod(pos, grid_size)
            grid[row, col] = 1  # 1 = bomb
        
        return {
            "game_id": game_id,
            "grid_size": grid_size,
            "num_bombs": num_bombs,
            "total_tiles": total_tiles,
            "num_safe": total_tiles - num_bombs,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "min_bombs": min_bombs,
            "max_bombs": max_bombs,
        }
    
    def get_tile_predictions(self, game_id: str, grid_size: int, revealed_tiles: List[Dict], num_bombs: int) -> List[Dict]:
        """
        Predict safety probability for unrevealed tiles
        
        Uses adjacency patterns and statistical inference
        """
        total_tiles = grid_size * grid_size
        safe_tiles = sum(1 for t in revealed_tiles if not t.get("is_bomb"))
        bomb_tiles = sum(1 for t in revealed_tiles if t.get("is_bomb"))
        unrevealed = total_tiles - len(revealed_tiles)
        
        # Base probability derived from remaining bombs instead of a fixed constant
        remaining_bombs = max(num_bombs - bomb_tiles, 0)
        base_safe_prob = (unrevealed - remaining_bombs) / unrevealed if unrevealed > 0 else 0.5
        
        predictions = []
        for row in range(grid_size):
            for col in range(grid_size):
                # Skip if already revealed
                if any(t["x"] == col and t["y"] == row for t in revealed_tiles):
                    continue
                
                # Calculate adjacency bonus (tiles near safe tiles are more likely safe)
                adjacent_safe = 0
                adjacent_total = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < grid_size and 0 <= nc < grid_size:
                            adjacent_total += 1
                            if any(t["x"] == nc and t["y"] == nr and not t.get("is_bomb") for t in revealed_tiles):
                                adjacent_safe += 1
                # Boost probability if adjacent to safe tiles (using adaptive weight)
                adjacency_bonus = (adjacent_safe / adjacent_total) * self.adjacency_weight if adjacent_total > 0 else 0
                safe_prob = min(0.95, max(0.05, base_safe_prob + adjacency_bonus))
                confidence = self.base_confidence + (adjacency_bonus * 0.2)  # Higher confidence if near safe tiles
                
                predictions.append({
                    "x": col,
                    "y": row,
                    "safe_probability": round(safe_prob, 3),
                    "confidence": round(confidence, 2),
                    "adjacent_safe_count": adjacent_safe,
                    "recommendation": "SAFE" if safe_prob > 0.7 else "RISKY" if safe_prob < 0.4 else "NEUTRAL"
                })
        
        # Sort by safety probability (safest first)
        predictions.sort(key=lambda x: x["safe_probability"], reverse=True)
        return predictions
    
    def calculate_game_stats(self, game_id: str, revealed_tiles: List[Dict], grid_size: int, num_bombs: int) -> Dict:
        """Calculate game statistics and performance metrics"""
        total_tiles = grid_size * grid_size
        safe_tiles_total = total_tiles - num_bombs

        if not revealed_tiles:
            return {
                "total_clicks": 0,
                "safe_clicks": 0,
                "bombs_hit": 0,
                "win_percentage": 0,
                "streak": 0,
                "bombs_remaining": num_bombs,
                "remaining_safe": safe_tiles_total,
            }
        
        safe_clicks = sum(1 for t in revealed_tiles if not t.get("is_bomb"))
        bomb_hits = sum(1 for t in revealed_tiles if t.get("is_bomb"))
        bombs_remaining = max(num_bombs - bomb_hits, 0)
        remaining_safe = max(safe_tiles_total - safe_clicks, 0)
        
        return {
            "total_clicks": len(revealed_tiles),
            "safe_clicks": safe_clicks,
            "bombs_hit": bomb_hits,
            "win_percentage": (safe_clicks / len(revealed_tiles) * 100) if revealed_tiles else 0,
            "streak": safe_clicks,  # Current streak until first bomb
            "bombs_remaining": bombs_remaining,
            "remaining_safe": remaining_safe,
        }


# Demo game storage
demo_games = {}

# Global predictor instance for persistent learning
_predictor_instance = None

def get_predictor():
    """Get mines predictor instance (singleton for learning persistence)"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = MinesPredictor()
    return _predictor_instance

def update_prediction_accuracy(was_correct: bool, predicted_prob: float):
    """Update predictor weights based on outcome"""
    predictor = get_predictor()
    predictor.prediction_history.append({"correct": was_correct, "prob": predicted_prob})
    
    # Adaptive learning: adjust weights every 20 predictions
    if len(predictor.prediction_history) >= 20:
        recent = predictor.prediction_history[-20:]
        accuracy = sum(1 for r in recent if r["correct"]) / len(recent)
        
        # If accuracy is low, reduce adjacency weight (be more conservative)
        if accuracy < 0.6:
            predictor.adjacency_weight = max(0.05, predictor.adjacency_weight * 0.95)
            predictor.base_confidence = max(0.5, predictor.base_confidence * 0.98)
        # If accuracy is high, slightly increase weights
        elif accuracy > 0.8:
            predictor.adjacency_weight = min(0.25, predictor.adjacency_weight * 1.02)
            predictor.base_confidence = min(0.85, predictor.base_confidence * 1.01)
