# Copilot Instructions for BetCheck

## Project Overview

**BetCheck** is a sports prediction engine that uses adaptive machine learning to forecast game outcomes. The architecture separates concerns into three layers:

- **Backend**: FastAPI service (`backend/main.py`) handling prediction logic, database operations, and adaptive learning
- **Database**: Supabase PostgreSQL storing games, predictions, factors, and results
- **Scripts**: Utility scripts for data seeding and periodic game updates (`scripts/`)

## Architecture & Key Components

### Prediction Pipeline

1. **Factor-Based Weighting**: Predictions rely on five core factors with adjustable weights:
   - Recent Form (0.20 base weight)
   - Injury Status (0.18)
   - Offensive Efficiency (0.22)
   - Defensive Efficiency (0.20)
   - Home Court Advantage (0.20)

2. **PredictionEngine Class** (`backend/main.py`):
   - `calculate_prediction()`: Computes game outcomes using weighted factor scores
   - `update_weights()`: Adaptive learning adjusts factor weights when predictions are verified against actual results
   - Uses **LEARNING_RATE = 0.05** to control weight adjustment magnitude (prevent overfitting)
   - Weights constrained to min/max boundaries (e.g., Recent Form between 0.05–0.40)

3. **Adaptive Learning Workflow**:
   - Store prediction for game → User logs actual result → `log_result()` endpoint calls `update_weights()`
   - Correct predictions slightly increase factor weight; incorrect predictions decrease it
   - Ensures model doesn't converge to poor local optima

### Database Schema

- **games**: game_id, sport, team_a, team_b, scheduled_date, result
- **factors**: factor_id, name, base_weight, current_weight, min_weight, max_weight
- **predictions**: game_id, predicted_outcome, confidence, created_at, was_correct, result_verified
- **results**: game_id, actual_outcome, created_at

Supabase client initialized with `SUPABASE_URL` and `SUPABASE_KEY` from `.env`

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/games` | List games (filter by sport optional) |
| GET | `/predict/{game_id}` | Get prediction for a specific game |
| POST | `/log_result` | Submit actual result; triggers adaptive learning |
| GET | `/factors` | Get all factors with current weights |
| GET | `/analytics` | Return accuracy metrics (total predictions, correct%, sample size) |

## Developer Workflows

### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment (copy from .env.example)
cp .env.example .env
# Edit .env with real Supabase credentials and SPORTS_API_KEY
```

### First-Time Initialization
```bash
# Seed initial factors into database
python scripts/seed_factors.py

# Populate sample games
python scripts/update_games.py
```

### Running the Backend
```bash
# Start development server (port 8000)
python -m uvicorn backend.main:app --reload

# Or from within backend/
cd backend && python main.py
```

### Common Development Tasks

- **Add new factor**: Edit `FACTORS` list in `scripts/seed_factors.py`, then re-run script
- **Adjust learning rate**: Modify `PredictionEngine.LEARNING_RATE` in `backend/main.py` (higher = more aggressive adaptation)
- **Test prediction**: Call `GET /predict/{game_id}` with existing game_id from database
- **Verify learning**: Check `/analytics` before and after calling `/log_result`

## Project-Specific Patterns

### Error Handling
- FastAPI endpoints return `HTTPException` with status_code and detail message
- Supabase errors wrapped in try/except; use `.execute()` after query chains
- Always check response data exists before accessing index (e.g., `if response.data`)

### Naming Conventions
- Game IDs: `{sport}_{year}_{month}_{day}_{team_a_slug}_{team_b_slug}` (e.g., `nba_2025_01_15_lakers_celtics`)
- Factor contributions stored as dict mapping factor names to score contributions

### Data Flow Pattern
Request → Supabase fetch → PredictionEngine calculation → Store result → Return JSON model

## Integration Points

- **Supabase**: Authentication via API key; all data persistence through this single client
- **Sports API**: Currently uses sample games (commented note mentions RapidAPI NBA integration available)
- **Frontend**: CORS enabled for all origins (`allow_origins=["*"]`); expects JSON responses matching Pydantic models

## Testing & Validation

Check prediction accuracy via `/analytics`:
- Requires both predictions AND results logged for accuracy calculation
- Returns 0% accuracy if insufficient data
- Use `was_correct` boolean in predictions table to verify learning effectiveness
