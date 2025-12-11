"""
Limbo/Crash Predictor Backend - Multiplier Crash Point Prediction
Predicts crash points in Limbo/Crash games with pattern analysis

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import random
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np
from statistics import mean, stdev

class LimboCrashPredictionEngine:
    """
    Predicts crash multipliers in Limbo/Crash games using:
    - Historical crash point analysis
    - Volatility patterns
    - Win/loss streaks
    - Bankroll patterns
    """
    
    # Learning parameters
    HISTORY_WEIGHT = 0.4
    VOLATILITY_WEIGHT = 0.25
    STREAK_WEIGHT = 0.2
    PATTERN_WEIGHT = 0.15
    
    def __init__(self, game_type: str = "crash"):
        """
        Initialize Limbo/Crash prediction engine.
        
        Args:
            game_type: "limbo" or "crash"
        """
        self.game_type = game_type  # limbo or crash
        self.min_multiplier = 1.01
        self.max_multiplier = 100.0
        
        # Historical tracking
        self.crash_history = []  # List of [crash_point, timestamp, duration_ms]
        self.prediction_accuracy = {
            'correct_direction': 0,
            'total_predictions': 0,
            'close_calls': 0  # Within 20% of actual
        }
        self.streak_data = {
            'consecutive_wins': 0,
            'consecutive_losses': 0,
            'win_streak_max': 0,
            'loss_streak_max': 0
        }
        self.volatility_history = []  # Recent crashes to detect volatility
    
    def generate_round(self) -> Dict:
        """
        Generate a new Limbo/Crash round with actual crash point.
        Uses weighted randomness based on history.
        
        Returns:
            Dict: {"crash_point": float, "game_id": str, "started_at": timestamp}
        """
        # Base crash point influenced by history
        if self.crash_history:
            historical_mean = mean([c[0] for c in self.crash_history[-20:]])  # Last 20
            # Crash point tends toward mean but with variance
            crash_point = max(self.min_multiplier, 
                            historical_mean + random.gauss(0, historical_mean * 0.3))
        else:
            # First game - random between 1.5x and 5x
            crash_point = random.uniform(1.5, 5.0)
        
        # Cap to max
        crash_point = min(self.max_multiplier, crash_point)
        
        return {
            "game_id": f"limbo_{datetime.now().timestamp()}",
            "crash_point": round(crash_point, 2),
            "started_at": datetime.now().isoformat(),
            "game_type": self.game_type
        }
    
    def predict_crash_point(self) -> Dict:
        """
        Predict where the crash will happen.
        
        Returns:
            Dict: {
                "predicted_crash": float,
                "confidence": float 0-1,
                "recommended_exit": float (safe exit point),
                "reasoning": List[str]
            }
        """
        if not self.crash_history:
            # No history - use neutral prediction
            return {
                "predicted_crash": 3.0,
                "confidence": 0.3,
                "recommended_exit": 2.0,
                "reasoning": [
                    "No historical data yet",
                    "Recommended: Start with conservative 2x exit",
                    "Build data for better predictions"
                ]
            }
        
        # Get historical stats
        recent_crashes = [c[0] for c in self.crash_history[-50:]]  # Last 50 games
        historical_mean = mean(recent_crashes)
        historical_std = stdev(recent_crashes) if len(recent_crashes) > 1 else 0.5
        
        # Calculate volatility
        volatility = historical_std / historical_mean if historical_mean > 0 else 0.5
        
        # Predicted crash influenced by history
        predicted_crash = self._apply_prediction_adjustments(
            historical_mean, volatility, historical_std
        )
        
        # Confidence based on historical consistency
        confidence = self._calculate_confidence(volatility, len(recent_crashes))
        
        # Recommended exit (slightly below predicted, for safety)
        recommended_exit = max(self.min_multiplier, predicted_crash * 0.85)
        
        reasoning = self._get_reasoning(
            predicted_crash, confidence, volatility, recent_crashes
        )
        
        return {
            "predicted_crash": round(predicted_crash, 2),
            "confidence": round(confidence, 3),
            "recommended_exit": round(recommended_exit, 2),
            "reasoning": reasoning
        }
    
    def _apply_prediction_adjustments(self, mean: float, volatility: float, std: float) -> float:
        """
        Apply adjustments to base prediction.
        - High volatility → predict higher (more volatile)
        - High streak → adjust up (hot games)
        - Recent pattern → trend toward pattern
        """
        prediction = mean
        
        # Streak adjustment
        if self.streak_data['consecutive_wins'] > 2:
            # In a win streak - games might be running longer
            prediction *= (1 + 0.1 * min(self.streak_data['consecutive_wins'], 5) / 5)
        elif self.streak_data['consecutive_losses'] > 2:
            # In a loss streak - expect shorter runs
            prediction *= (1 - 0.15 * min(self.streak_data['consecutive_losses'], 5) / 5)
        
        # Volatility adjustment
        if volatility > 1.0:  # High volatility
            # Add upside potential
            prediction *= (1 + volatility * 0.2)
        
        return max(self.min_multiplier, min(self.max_multiplier, prediction))
    
    def _calculate_confidence(self, volatility: float, history_size: int) -> float:
        """
        Calculate confidence in prediction.
        - Consistency (low volatility) = high confidence
        - Sample size matters
        - Recent accuracy helps
        """
        # Base confidence on volatility (lower = more consistent = higher confidence)
        volatility_confidence = max(0.1, 1.0 - volatility)
        
        # Boost confidence with history size
        history_boost = min(0.3, history_size / 100)
        
        # Accuracy track record
        if self.prediction_accuracy['total_predictions'] > 0:
            accuracy_rate = (
                self.prediction_accuracy['correct_direction'] / 
                self.prediction_accuracy['total_predictions']
            )
            accuracy_boost = accuracy_rate * 0.2
        else:
            accuracy_boost = 0
        
        confidence = (volatility_confidence * 0.6 + 
                     history_boost + accuracy_boost)
        
        return max(0.0, min(1.0, confidence))
    
    def _get_reasoning(self, predicted: float, confidence: float, 
                      volatility: float, history: List[float]) -> List[str]:
        """Generate reasoning bullets."""
        reasons = []
        
        # Reason 1: Historical average
        hist_mean = mean(history)
        reasons.append(f"✓ Historical average: {hist_mean:.2f}x (from {len(history)} games)")
        
        # Reason 2: Volatility
        if volatility > 1.0:
            reasons.append(f"⚠ High volatility detected: ±{volatility:.1f}x swings expected")
        else:
            reasons.append(f"✓ Stable pattern: Consistent crashes around {hist_mean:.2f}x")
        
        # Reason 3: Streak/Pattern
        if self.streak_data['consecutive_wins'] > 2:
            reasons.append(f"📈 Hot streak: {self.streak_data['consecutive_wins']} wins - extended runs likely")
        elif self.streak_data['consecutive_losses'] > 2:
            reasons.append(f"📉 Cold streak: {self.streak_data['consecutive_losses']} losses - shorter runs expected")
        else:
            reasons.append(f"Confidence: {confidence*100:.0f}% in {predicted:.2f}x prediction")
        
        return reasons[:3]
    
    def log_result(self, crash_point: float, user_exit: Optional[float] = None, 
                   user_won: Optional[bool] = None) -> None:
        """
        Log actual crash point and user outcome for learning.
        
        Args:
            crash_point: Where game actually crashed
            user_exit: Where user exited (None if cashout failed)
            user_won: Whether user profited (True) or lost (False)
        """
        # Store crash point
        self.crash_history.append([crash_point, datetime.now(), 0])
        self.volatility_history.append(crash_point)
        
        # Keep only recent volatility history (last 50)
        if len(self.volatility_history) > 50:
            self.volatility_history = self.volatility_history[-50:]
        
        # Update streak
        if user_won:
            self.streak_data['consecutive_wins'] += 1
            self.streak_data['consecutive_losses'] = 0
            self.streak_data['win_streak_max'] = max(
                self.streak_data['win_streak_max'],
                self.streak_data['consecutive_wins']
            )
        else:
            self.streak_data['consecutive_losses'] += 1
            self.streak_data['consecutive_wins'] = 0
            self.streak_data['loss_streak_max'] = max(
                self.streak_data['loss_streak_max'],
                self.streak_data['consecutive_losses']
            )
        
        # Track prediction accuracy if we made one
        self.prediction_accuracy['total_predictions'] += 1
    
    def get_volatility_analysis(self) -> Dict:
        """
        Analyze volatility patterns.
        
        Returns:
            Dict with volatility metrics
        """
        if not self.crash_history:
            return {"volatility": 0, "trend": "neutral", "message": "No data yet"}
        
        recent = [c[0] for c in self.crash_history[-20:]]
        avg = mean(recent)
        std = stdev(recent) if len(recent) > 1 else 0
        volatility = std / avg if avg > 0 else 0
        
        # Determine trend
        if len(recent) >= 3:
            trend_data = recent[-3:]
            if mean(trend_data) > avg:
                trend = "increasing"
            elif mean(trend_data) < avg:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "neutral"
        
        return {
            "volatility": round(volatility, 3),
            "average_crash": round(avg, 2),
            "std_dev": round(std, 2),
            "trend": trend,
            "games_analyzed": len(recent)
        }
