# Score Verification Workflow

## Overview
BetCheck now uses a simplified binary verification workflow where:
1. **ESPN Fetcher** automatically pulls game scores every 6 hours
2. **User Verification** confirms if the fetched score is accurate
3. **Adaptive Learning** updates factor weights only on correct verifications

## Workflow Flow

```
Game Scheduled
    ↓
Match Time Passes
    ↓
ESPN Fetcher (Background Thread)
    ├─ Checks ESPN API every 6 hours
    ├─ Fetches score: "Team A 95 - 87 Team B"
    └─ Saves to database with verified=False
    ↓
User Sees Completed Game
    ├─ Clicks "Verify Result" button
    └─ Modal shows: "ESPN says: Team A 95 - Team B 87"
    ↓
User Clicks ✓ Verify or ✗ Incorrect
    ├─ If ✓ Verify (is_correct=true)
    │   ├─ POST /verify_result/{game_id}?is_correct=true
    │   ├─ Triggers PredictionEngine.update_weights()
    │   ├─ Factor weights adjust based on prediction accuracy
    │   └─ Sets verification_type: "auto_verified"
    │
    └─ If ✗ Incorrect (is_correct=false)
        ├─ POST /verify_result/{game_id}?is_correct=false
        ├─ No weight update
        └─ Sets verification_type: "auto_rejected"
    ↓
Past Games Page
    ├─ Shows completed games with verification badges
    ├─ Displays overall accuracy %
    └─ Tracks verification sources (auto, manual, etc)
```

## Key Endpoints

### Frontend Triggers
- **Button**: "Verify Result" in game detail modal
- **Modal**: Shows ESPN-fetched score with two action buttons
- **No manual data entry**: User only confirms yes/no

### Backend API

#### POST `/verify_result/{game_id}`
```bash
# Verify ESPN result as correct
curl -X POST "http://localhost:8000/verify_result/nba_2025_01_15_lakers_celtics?is_correct=true"

# Mark ESPN result as incorrect
curl -X POST "http://localhost:8000/verify_result/nba_2025_01_15_lakers_celtics?is_correct=false"
```

#### GET `/games/status/{game_id}`
Returns score data and verification status:
```json
{
  "game_id": "nba_2025_01_15_lakers_celtics",
  "has_result": true,
  "result": "Lakers 95 - 87 Celtics",
  "team_a": "Lakers",
  "team_b": "Celtics",
  "score_a": 95,
  "score_b": 87,
  "verified": true,
  "verification_type": "auto_verified"
}
```

#### POST `/log_result` (Fallback)
Manual result logging if ESPN fails:
```json
{
  "game_id": "nba_2025_01_15_lakers_celtics",
  "actual_outcome": "Lakers"
}
```

## Learning Mechanism

### Factor Weight Updates
When user verifies ESPN result as correct (`is_correct=true`):

1. **Calculate Prediction Error**: Did prediction match actual result?
2. **Adjust Factor Weights**: 
   - Correct prediction → increase factor weight by LEARNING_RATE * 0.05
   - Incorrect prediction → decrease factor weight by LEARNING_RATE * 0.05
3. **Enforce Boundaries**: Keep weights within min/max constraints

### Example
```python
# If prediction was correct and Recent Form factor had score 0.75
recent_form_weight = 0.20  # Base weight
recent_form_weight += 0.20 * 0.05 * 0.05  # +0.0005 (increase)

# If prediction was wrong and same factor
recent_form_weight -= 0.20 * 0.05 * 0.05  # -0.0005 (decrease)
```

## Database Changes

### Games Table
- `result`: "Team A 95 - 87 Team B"
- `verified`: Boolean flag (true after verification)
- `verification_type`: "auto" | "manual" | "auto_verified" | "auto_rejected"

### Results Table
- `game_id`: Foreign key
- `actual_outcome`: Result string
- `verification_type`: How result was confirmed
- `created_at`: Timestamp

## Frontend Components

### Game Detail Page (`/game/[gameId]`)
1. **Prediction Card**: Shows prediction and confidence
2. **Result Section**: 
   - If no result: "Verify Result" button
   - If result verified: Shows accuracy (✓ or ✗) with badge
3. **Verify Modal**:
   - Shows ESPN score in large display
   - Two action buttons: "✓ Verify" | "✗ Incorrect"
   - Loading state while processing

### Past Games Page (`/past-games`)
1. **Sport Filter Tabs**: Filter by NBA, NFL, MLB, etc
2. **Game Cards**: Show game outcome, score, and verification status
3. **Accuracy Meter**: Overall correctness %
4. **Verification Badges**:
   - 🤖 Auto-Verified (blue)
   - 👤 Manual (purple)
   - ❌ Auto-Rejected (gray)

## Testing the Workflow

### Manual Test Steps
1. Start backend: `python -m uvicorn backend.main:app --reload`
2. Navigate to a completed game in frontend
3. Click "Verify Result"
4. See ESPN score displayed in modal
5. Click "✓ Verify" to trigger learning
6. Check `/analytics` endpoint to see weights updated
7. Check past-games page to see accuracy %

### Automated Testing
The ESPN fetcher runs every 6 hours in a background thread:
```python
# Fetches games that completed in last 48 hours
result_fetcher.fetch_daily_results(lookback_days=2)

# Returns dict with scores
# {
#   "game_id": {
#     "winner": "Lakers",
#     "team_a": "Lakers",
#     "team_b": "Celtics", 
#     "score_a": 95,
#     "score_b": 87,
#     "status": "completed"
#   }
# }
```

## Error Handling

### No Result Found
- **User sees**: "Loading score..." in modal
- **Action**: Wait for next fetcher cycle or use Manual Log Result fallback

### ESPN API Down
- **Fallback**: User can manually log result via `/log_result` endpoint
- **Flag**: Will be marked as `verification_type: "manual"`

### Invalid Game ID
- **Response**: 404 error
- **Frontend**: Displays error message and back button

## Verification Badges

| Badge | Color | Meaning |
|-------|-------|---------|
| 🤖 | Blue | Auto-Verified (ESPN score confirmed by user) |
| ✓ | Green | Prediction was correct |
| ✗ | Red | Prediction was incorrect |
| 👤 | Purple | Manually verified (user entered score) |
| ❌ | Gray | Auto-Rejected (ESPN score marked incorrect) |

## Future Enhancements

1. **Confidence Adjustment**: Reduce confidence score for incorrect ESPN data sources
2. **Multi-Source Verification**: Compare ESPN vs official league APIs
3. **Batch Verification**: Verify multiple games at once
4. **Notification System**: Alert user when new games have results ready
5. **Verification Analytics**: Track ESPN accuracy over time

## Configuration

### Interval Settings (in `backend/main.py`)
```python
# How often ESPN fetcher checks for new results
FETCHER_INTERVAL_HOURS = 6  # Check every 6 hours

# How many days back to look for completed games
LOOKBACK_DAYS = 2  # Check last 48 hours
```

### Learning Settings
```python
# How aggressively weights adapt to prediction accuracy
LEARNING_RATE = 0.05  # 5% adjustment per verification

# Weight boundaries (prevent overfitting)
MIN_WEIGHT = 0.05   # Floor for any factor
MAX_WEIGHT = 0.40   # Ceiling for any factor
```

## Troubleshooting

### Modal Won't Open
- Check browser console for errors
- Verify `API_URL` is correctly set in `.env.local`
- Ensure game has `result` data

### Verification Not Triggering
- Check network tab: POST to `/verify_result` should return 200
- Verify game_id format matches database
- Check backend logs for error messages

### Weights Not Updating
- Ensure `is_correct=true` in POST request
- Check that prediction exists (required for learning)
- Verify `supabase` is connected or DEMO_MODE is active

### ESPN Score Not Showing
- Fetcher may not have run yet (runs every 6 hours)
- Manually trigger: Check `/games/status/{game_id}` endpoint
- Use Manual Log Result as fallback
