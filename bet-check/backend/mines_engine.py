"""
Mines Predictor Backend - Dynamic Grid Prediction Engine
Predicts safe tiles in Mines games with adaptive learning

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import random
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import numpy as np

class MinesPredictionEngine:
    """
    Predicts safe tiles in Mines games using:
    - Base probability (1 - bombs/total_tiles)
    - Historical adjacency patterns
    - Streak analysis
    - Tile safety history
    """
    
    # Learning parameters
    LEARNING_RATE = 0.05
    ADJACENCY_WEIGHT = 0.3
    STREAK_WEIGHT = 0.25
    HISTORY_WEIGHT = 0.45
    
    def __init__(self, grid_size: int = 5, num_bombs: Optional[int] = None):
        """
        Initialize mines prediction engine.
        
        Args:
            grid_size: Grid dimension (e.g., 5 = 5x5 grid, 25 total tiles)
            num_bombs: Number of bombs in grid (default: ~20% of tiles)
        """
        self.grid_size = grid_size
        self.total_tiles = grid_size * grid_size
        self.num_bombs = num_bombs or max(3, self.total_tiles // 5)  # 20% default
        self.num_safe = self.total_tiles - self.num_bombs
        
        # Base probability all tiles are safe
        self.base_safe_probability = self.num_safe / self.total_tiles
        
        # Historical tracking
        self.tile_click_history = {}  # {(x,y): [(is_safe, timestamp), ...]}
        self.adjacency_patterns = {}   # {(x,y): {neighbor_coords: is_safe_count}}
        self.streak_data = {           # Track consecutive safe/bomb clicks
            'consecutive_safe': 0,
            'consecutive_bombs': 0,
            'total_safe_clicks': 0,
            'total_bomb_clicks': 0
        }
    
    def generate_grid(self) -> Dict[Tuple[int, int], Dict]:
        """
        Generate game grid with bomb positions (random).
        
        Returns:
            Dict mapping (x, y) to {"is_bomb": bool, "predicted_safe": float}
        """
        all_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        bomb_positions = set(random.sample(all_positions, self.num_bombs))
        
        grid = {}
        for x, y in all_positions:
            grid[(x, y)] = {
                "is_bomb": (x, y) in bomb_positions,
                "predicted_safe": self._calculate_tile_probability(x, y),
                "clicked": False,
                "revealed": False
            }
        
        return grid
    
    def _calculate_tile_probability(self, x: int, y: int) -> float:
        """
        Calculate probability a tile is safe based on:
        - Base probability
        - Adjacency patterns
        - Streak data
        - Historical clicks
        
        Args:
            x, y: Tile coordinates
            
        Returns:
            float 0-1: Probability tile is safe
        """
        # Start with base probability
        prob = self.base_safe_probability
        
        # Adjust based on adjacency patterns (safer near previously safe tiles)
        adjacency_bonus = self._get_adjacency_bonus(x, y)
        
        # Adjust based on streaks (recent safe clicks increase confidence)
        streak_bonus = self._get_streak_bonus()
        
        # Adjust based on historical clicks on this tile
        history_bonus = self._get_history_bonus(x, y)
        
        # Weighted combination
        final_prob = (
            prob * (1 - self.ADJACENCY_WEIGHT - self.STREAK_WEIGHT - self.HISTORY_WEIGHT) +
            adjacency_bonus * self.ADJACENCY_WEIGHT +
            streak_bonus * self.STREAK_WEIGHT +
            history_bonus * self.HISTORY_WEIGHT
        )
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, final_prob))
    
    def _get_adjacency_bonus(self, x: int, y: int) -> float:
        """
        Bonus probability if adjacent tiles are safe.
        Safer tiles cluster around safe tiles.
        """
        neighbors = self._get_neighbors(x, y)
        if not neighbors:
            return self.base_safe_probability
        
        # Average safety of neighbors
        neighbor_safety = []
        for nx, ny in neighbors:
            history = self.tile_click_history.get((nx, ny), [])
            if history:
                # Percentage of safe clicks on this neighbor
                safe_count = sum(1 for is_safe, _ in history if is_safe)
                safety_rate = safe_count / len(history)
                neighbor_safety.append(safety_rate)
        
        return sum(neighbor_safety) / len(neighbor_safety) if neighbor_safety else self.base_safe_probability
    
    def _get_streak_bonus(self) -> float:
        """
        Bonus probability if we're in a safe streak.
        Consecutive safe clicks increase confidence for next click.
        """
        # Positive streak bonus (after safe clicks)
        if self.streak_data['consecutive_safe'] > 0:
            # Bonus decreases with streak length (diminishing returns)
            bonus = min(0.2, self.streak_data['consecutive_safe'] * 0.05)
            return self.base_safe_probability + bonus
        
        # Penalty if in bomb streak
        if self.streak_data['consecutive_bombs'] > 0:
            penalty = min(0.15, self.streak_data['consecutive_bombs'] * 0.03)
            return self.base_safe_probability - penalty
        
        return self.base_safe_probability
    
    def _get_history_bonus(self, x: int, y: int) -> float:
        """
        Bonus based on historical clicks on this specific tile.
        If tile has been clicked before, use that history.
        """
        history = self.tile_click_history.get((x, y), [])
        if not history:
            return self.base_safe_probability
        
        safe_count = sum(1 for is_safe, _ in history if is_safe)
        return safe_count / len(history)
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighboring tile coordinates."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    neighbors.append((nx, ny))
        return neighbors
    
    def log_result(self, x: int, y: int, is_safe: bool) -> None:
        """
        Log actual outcome of a tile click for learning.
        
        Args:
            x, y: Tile coordinates
            is_safe: Whether tile was safe (True) or bomb (False)
        """
        # Update click history
        if (x, y) not in self.tile_click_history:
            self.tile_click_history[(x, y)] = []
        self.tile_click_history[(x, y)].append((is_safe, datetime.now()))
        
        # Update streaks
        if is_safe:
            self.streak_data['consecutive_safe'] += 1
            self.streak_data['consecutive_bombs'] = 0
            self.streak_data['total_safe_clicks'] += 1
        else:
            self.streak_data['consecutive_bombs'] += 1
            self.streak_data['consecutive_safe'] = 0
            self.streak_data['total_bomb_clicks'] += 1
        
        # Update adjacency patterns for all neighbors
        neighbors = self._get_neighbors(x, y)
        for nx, ny in neighbors:
            if (nx, ny) not in self.adjacency_patterns:
                self.adjacency_patterns[(nx, ny)] = {}
            if (x, y) not in self.adjacency_patterns[(nx, ny)]:
                self.adjacency_patterns[(nx, ny)][(x, y)] = 0
            if is_safe:
                self.adjacency_patterns[(nx, ny)][(x, y)] += 1
    
    def get_safest_tiles(self, grid: Dict, top_n: int = 3) -> List[Dict]:
        """
        Get predicted safest tiles.
        
        Args:
            grid: Current game grid
            top_n: Number of top tiles to return
            
        Returns:
            List of dicts: {"x": int, "y": int, "confidence": float}
        """
        tiles = []
        for (x, y), tile_data in grid.items():
            if not tile_data['clicked']:
                tiles.append({
                    "x": x,
                    "y": y,
                    "confidence": tile_data['predicted_safe']
                })
        
        # Sort by confidence descending
        tiles.sort(key=lambda t: t['confidence'], reverse=True)
        return tiles[:top_n]
    
    def get_reasoning(self) -> List[str]:
        """
        Generate reasoning bullets explaining predictions.
        
        Returns:
            List of 3 reasoning statements
        """
        reasons = []
        
        # Reason 1: Adjacency patterns
        if self.tile_click_history:
            safe_tiles = sum(1 for clicks in self.tile_click_history.values()
                            if any(is_safe for is_safe, _ in clicks))
            if safe_tiles > 0:
                reasons.append(f"✓ Adjacency patterns: {safe_tiles} tiles historically safe nearby")
        
        # Reason 2: Streaks
        if self.streak_data['consecutive_safe'] > 0:
            reasons.append(f"✓ Hot streak: {self.streak_data['consecutive_safe']} consecutive safe clicks detected")
        elif self.streak_data['consecutive_bombs'] > 0:
            reasons.append(f"⚠ Cold streak: {self.streak_data['consecutive_bombs']} bombs in a row - caution recommended")
        
        # Reason 3: Base probability
        bomb_freq = self.num_bombs / self.total_tiles
        safe_freq = 1 - bomb_freq
        reasons.append(f"✓ Bomb frequency: ~{bomb_freq*100:.0f}% bombs ({safe_freq*100:.0f}% safe)")
        
        return reasons[:3]
