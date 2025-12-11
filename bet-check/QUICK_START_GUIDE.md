# 🚀 BetCheck - 5-Minute Quick Start

Get the BetCheck sports prediction engine running in minutes.

---

## ⚡ Option 1: Docker (Easiest)

### Prerequisites
- Docker & Docker Compose installed

### Steps
```bash
# 1. Clone and navigate
cd /Users/fullsail/bet-check

# 2. Copy environment template
cp .env.example .env

# 3. (Optional) Edit .env with your Supabase credentials
# For testing, the demo credentials work fine

# 4. Build and start services
docker-compose up --build

# 5. Wait for services to start
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

**That's it!** Visit http://localhost:3000 in your browser.

---

## ⚙️ Option 2: Local Development (Advanced)

### Prerequisites
- Python 3.9+
- Node.js 18+
- Pip and npm installed

### Backend Setup
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Copy environment file
cp .env.example .env

# 3. Initialize database (one-time)
python scripts/seed_factors.py
python scripts/update_games.py

# 4. Start backend (port 8000)
python -m uvicorn backend.main:app --reload
```

### Frontend Setup (New Terminal)
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start dev server (port 3000)
npm run dev
```

### Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🧪 Testing the API

```bash
# Run all tests
python test_api.py

# Expected output:
# ✓ Health check: returns {"status": "healthy"}
# ✓ Games list: returns array of games
# ✓ Prediction: returns prediction with confidence
# ✓ Factors: returns all factor weights
# ✓ Analytics: returns accuracy metrics
```

---

## 🎮 Using the Application

### 1. **Home Page** (http://localhost:3000)
- View upcoming games
- Filter by sport
- Click game for detailed prediction

### 2. **Game Detail Page** (http://localhost:3000/game/[gameId])
- View detailed prediction
- See factor contributions
- Log actual game result

### 3. **Dashboard** (http://localhost:3000/dashboard)
- View prediction accuracy
- See current factor weights
- Track improvement over time

---

## 📊 Understanding Predictions

Each prediction includes:

1. **Predicted Winner**: Which team is predicted to win
2. **Confidence**: 0-100% certainty in prediction
3. **Factor Contributions**:
   - Recent Form (20%)
   - Injury Status (18%)
   - Offensive Efficiency (22%)
   - Defensive Efficiency (20%)
   - Home Court Advantage (20%)

## 📈 How Adaptive Learning Works

1. **Make Prediction**: Click "Get Prediction"
2. **Watch Game**: Outcome occurs
3. **Log Result**: Submit actual winner
4. **System Learns**: Factors that contributed to correct predictions get higher weights
5. **Improve**: Over time, predictions become more accurate

---

## 🔧 Configuration

Edit `.env` to change:

```env
# Supabase Database
SUPABASE_URL=your-database-url
SUPABASE_KEY=your-api-key

# API Configuration  
SPORTS_API_KEY=your-sports-api-key
BACKEND_PORT=8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📋 Common Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild images
docker-compose up --build --force-recreate

# Check database
python scripts/verify_db.py

# Seed fresh data
python scripts/seed_factors.py

# Update games
python scripts/update_games.py
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clean and reinstall
rm -rf frontend/node_modules package-lock.json
npm install
```

### API connection errors
```bash
# Make sure backend is running
curl http://localhost:8000/health

# Check environment variable
grep NEXT_PUBLIC_API_URL .env
```

### Database connection errors
```bash
# Verify database setup
python scripts/verify_db.py

# Check .env credentials
cat .env | grep SUPABASE
```

---

## 📚 Full Documentation

- **Architecture**: See `/github/copilot-instructions.md`
- **API Reference**: Visit http://localhost:8000/docs (Swagger UI)
- **Project Structure**: See `FILE_STRUCTURE.md`
- **Deployment**: See `LAUNCH_CHECKLIST.md`

---

## 🎯 Next Steps

1. **Test the API**: Run `python test_api.py`
2. **Make a prediction**: Browse to home page
3. **Log a result**: Go to game detail page
4. **Check dashboard**: See analytics improve

---

## ✅ Success!

If you see:
- ✅ Homepage with games list
- ✅ Predictions with confidence scores
- ✅ Dashboard with analytics
- ✅ API responding at /docs

**You're ready to use BetCheck!**

---

**Need Help?**  
- Check terminal output for error messages
- Review application logs
- Run `python test_api.py` to validate setup
- See `LAUNCH_CHECKLIST.md` for detailed setup

**Happy Predicting! 🎯**
