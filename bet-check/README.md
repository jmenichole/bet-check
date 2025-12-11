# Sports Prediction Tool - Bet Check

A full-stack AI-powered sports prediction tool built with **FastAPI** (backend), **Next.js** (frontend), and **Supabase/PostgreSQL** (database). The system automatically learns and adapts its prediction models based on outcomes.

## Features

✅ **Intelligent Predictions**: Predicts game outcomes using weighted factors (recent form, injuries, efficiency, home court advantage)  
✅ **Adaptive Learning**: Automatically adjusts factor weights based on prediction accuracy (0-100%)  
✅ **Confidence Scores**: Each prediction includes confidence percentage and top 3 reasons  
✅ **Real-time Dashboard**: Monitor accuracy metrics and factor effectiveness  
✅ **RESTful API**: Clean endpoints for games, predictions, and results  
✅ **Responsive Design**: Mobile-friendly UI built with Tailwind CSS  
✅ **Self-Learning**: Fully automatic weight adjustment with no manual intervention  

## Architecture

```
bet-check/
├── backend/                    # FastAPI Python backend
│   ├── main.py                # Core prediction engine & API
│   └── requirements.txt        # Python dependencies
├── frontend/                   # Next.js React frontend
│   ├── pages/
│   │   ├── index.tsx          # Home page (upcoming games list)
│   │   ├── game/[gameId].tsx  # Game prediction details
│   │   └── dashboard.tsx      # Analytics & factor weights
│   ├── styles/
│   │   └── globals.css        # Tailwind styling
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
├── scripts/                    # Utility scripts
│   ├── seed_factors.py        # Initialize factor weights
│   └── update_games.py        # Fetch upcoming games from API
├── schema.sql                  # Database schema (run in Supabase)
├── .env.example               # Environment variable template
└── README.md                  # This file
```

## Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Supabase account** (free tier works fine)
- **Git** for version control

## Setup Instructions

### 1. Clone the Repository

```bash
cd bet-check
```

### 2. Set Up Database (Supabase)

**Sign up for free at [supabase.com](https://supabase.com)**

1. Create a new Supabase project
2. Go to **SQL Editor** in the dashboard
3. Copy and paste all SQL from `schema.sql`
4. Click **Run** to create tables and seed sample data

Get your credentials:
- Go to **Project Settings → API**
- Copy **Project URL** → `SUPABASE_URL`
- Copy **anon key** → `SUPABASE_KEY`

### 3. Set Up Environment Variables

Create `.env` file in root directory:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Sports API (optional - uses free API by default)
SPORTS_API_KEY=your-rapidapi-key

# Backend
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Set Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Run backend server
python main.py
```

✅ Backend running at: **http://localhost:8000**  
📚 API Docs at: **http://localhost:8000/docs** (interactive Swagger UI)

### 5. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

### 6. Seed Initial Data

In a new terminal (backend venv still active):

```bash
cd scripts

# Populate factors table
python seed_factors.py

# Fetch upcoming games
python update_games.py
```

✅ Open http://localhost:3000 - you should see upcoming games!

## API Endpoints

### Games
- **GET** `/games?sport=nba` - List upcoming games

### Predictions
- **GET** `/predict/{game_id}` - Get prediction with confidence and reasons
- **POST** `/log_result` - Record actual outcome and trigger learning
- **GET** `/analytics` - View accuracy metrics

### Factors
- **GET** `/factors` - Get all factors with current weights

### Health
- **GET** `/health` - Service status check

### API Documentation
- **GET** `/docs` - Interactive Swagger UI (FastAPI)

## How Adaptive Learning Works

The prediction engine uses **5 core factors**:

1. **Recent Form** (20% base weight)
   - How well team performed in last 5 games
   - Weight range: 5% - 40%

2. **Injury Status** (18% base weight)
   - Impact of key player injuries
   - Weight range: 5% - 35%

3. **Offensive Efficiency** (22% base weight)
   - Points per possession and shooting metrics
   - Weight range: 10% - 40%

4. **Defensive Efficiency** (20% base weight)
   - Points allowed per possession
   - Weight range: 10% - 40%

5. **Home Court Advantage** (20% base weight)
   - Home vs away performance differential
   - Weight range: 5% - 30%

### Learning Algorithm

```
For each prediction result logged:
  if prediction was CORRECT:
    increase factor_weight += (LEARNING_RATE × 0.1)
  else:
    decrease factor_weight -= (LEARNING_RATE × 0.1)
  
  clamp weight between [min_weight, max_weight]
```

**Learning Rate**: 0.05 (5% adjustment per result) - adjust in `main.py`

### Example Flow

1. **First game**: Lakers vs Celtics
   - Engine predicts Lakers with 75% confidence
   - Uses all 5 factors with base weights

2. **Game result**: Celtics wins
   - Prediction was **incorrect**
   - All factors decrease slightly (e.g., 0.20 → 0.19)
   - Less reliable factors may drop further

3. **Second game**: Same teams again
   - Weights are now updated
   - Factors that were wrong before have less influence
   - New prediction uses adjusted weights

4. **Over time**: After 50+ games
   - Weights converge to most predictive factors
   - Model accuracy stabilizes or improves

## Usage Examples

### Get Upcoming Games

```bash
curl http://localhost:8000/games?sport=nba
```

Response:
```json
[
  {
    "game_id": "nba_2025_01_15_lakers_celtics",
    "sport": "nba",
    "team_a": "Los Angeles Lakers",
    "team_b": "Boston Celtics",
    "scheduled_date": "2025-01-15T20:00:00"
  }
]
```

### Get Prediction for a Game

```bash
curl http://localhost:8000/predict/nba_2025_01_15_lakers_celtics
```

Response:
```json
{
  "game_id": "nba_2025_01_15_lakers_celtics",
  "predicted_outcome": "Los Angeles Lakers",
  "confidence": 75.5,
  "reasons": [
    "Recent Form: Los Angeles Lakers has stronger recent form (0.82)",
    "Offensive Efficiency: Los Angeles Lakers has stronger offensive efficiency (0.79)",
    "Home Court Advantage: Los Angeles Lakers has stronger home court advantage (0.88)"
  ],
  "factor_contributions": {
    "Recent Form": {"team_a": 0.164, "team_b": 0.133},
    ...
  }
}
```

### Log a Game Result

```bash
curl -X POST http://localhost:8000/log_result \
  -H "Content-Type: application/json" \
  -d '{
    "game_id": "nba_2025_01_15_lakers_celtics",
    "actual_outcome": "Los Angeles Lakers"
  }'
```

Response:
```json
{
  "status": "success",
  "message": "Result logged for game nba_2025_01_15_lakers_celtics",
  "weights_updated": true
}
```

## Running with Docker (Optional)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Development Tips

### Adding New Factors

1. Open `scripts/seed_factors.py`
2. Add new factor to `FACTORS` list:
   ```python
   {
       "factor_id": 6,
       "name": "Player Fatigue",
       "base_weight": 0.15,
       "current_weight": 0.15,
       "min_weight": 0.05,
       "max_weight": 0.30,
   }
   ```
3. Update prediction logic in `backend/main.py` to calculate this factor

### Adjusting Learning Rate

In `backend/main.py`:
```python
class PredictionEngine:
    LEARNING_RATE = 0.05  # Change this value (0.01 = 1%, 0.1 = 10%)
```

Higher = faster learning (may overshoot)  
Lower = slower learning (more stable)

### Adding New Sports

In `scripts/update_games.py`:
1. Add API call for new sport
2. Format data to match `games` table schema
3. Update frontend to display new sport

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt

# Check port 8000 is free
lsof -i :8000
```

### Database connection error
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check Supabase dashboard for active tables
- Run `schema.sql` again if tables missing

### Frontend can't reach backend
- Ensure backend is running (`python main.py`)
- Check `NEXT_PUBLIC_API_URL` in `.env`
- Check browser console for CORS errors

### No games displaying
- Run `python scripts/update_games.py`
- Check Supabase `games` table for data
- Verify API response at `http://localhost:8000/games`

## Performance Notes

- **Initial predictions**: Fast (<100ms)
- **Learning update**: Fast (<200ms) per result
- **Dashboard load**: 1-2 seconds with 100+ predictions
- **Recommended**: Cache predictions for 1-2 hours for same-day games

## Security Considerations

⚠️ **This is a demo app - for production:**

1. Use environment variables for all secrets (✅ already done)
2. Enable Supabase Row Level Security (RLS) policies
3. Add API authentication (JWT tokens)
4. Rate limit API endpoints
5. Validate all user inputs
6. Use HTTPS in production
7. Keep dependencies updated

## Future Enhancements

🔄 **Potential features:**
- [ ] Support for NFL, MLB, NHL sports
- [ ] Real-time game updates
- [ ] User authentication & personal predictions
- [ ] Factor importance visualization
- [ ] Model versioning & rollback
- [ ] Batch predictions
- [ ] WebSocket for live updates
- [ ] Machine learning models (XGBoost, etc.)
- [ ] Historical performance analytics
- [ ] Betting line integration

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API docs at `http://localhost:8000/docs`
3. Check backend logs in terminal
4. Check browser console for frontend errors

---

**Built with ❤️ | FastAPI + Next.js + Supabase**
