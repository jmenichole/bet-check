# Quick Start Guide

Follow these steps to launch Bet Check locally. **Time required: 10-15 minutes**

## Prerequisites Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node -v`)
- [ ] npm installed (`npm -v`)
- [ ] Supabase account (free) - https://supabase.com/sign-up

---

## Step 1: Set Up Supabase Database (5 minutes)

### 1.1 Create Supabase Project

1. Go to https://supabase.com and sign in
2. Click **New Project**
3. Choose a project name and database password
4. Click **Create new project** (wait ~2 minutes for database to be ready)

### 1.2 Get Your Credentials

1. Click **Settings** (bottom left of dashboard)
2. Go to **API** tab
3. Copy the following and save them:
   - **Project URL** → will paste as `SUPABASE_URL`
   - **anon public key** → will paste as `SUPABASE_KEY`

### 1.3 Create Database Schema

1. Click **SQL Editor** (left sidebar)
2. Click **New Query**
3. Open the file `/Users/fullsail/bet-check/schema.sql` in a text editor
4. Copy all the SQL code
5. Paste into the Supabase SQL editor
6. Click **Run** (top right)

✅ **You'll see a success message. Tables are now created!**

---

## Step 2: Configure Environment Variables (2 minutes)

1. Open `/Users/fullsail/bet-check/.env` in your text editor
2. Fill in the values you saved from Step 1.2:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# Keep these as-is for local development
SPORTS_API_KEY=demo
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Save the file

✅ **Environment is configured!**

---

## Step 3: Start the Backend (2 minutes)

### Open Terminal 1

```bash
cd /Users/fullsail/bet-check/backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r ../requirements.txt

# Start the server
python main.py
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend running at http://localhost:8000**

**Test it:** Open http://localhost:8000/docs in your browser - you'll see the API documentation!

---

## Step 4: Seed Initial Data (2 minutes)

### Open Terminal 2

```bash
cd /Users/fullsail/bet-check/scripts

# Make sure your .env is in the root directory!
# These scripts will read it

# Populate factors
python seed_factors.py

# Fetch upcoming games
python update_games.py
```

**Expected output:**
```
✓ Seeded factors successfully!
✓ Successfully updated 4 games!
```

✅ **Database is populated with initial data!**

---

## Step 5: Start the Frontend (2 minutes)

### Open Terminal 3

```bash
cd /Users/fullsail/bet-check/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected output:**
```
> bet-check-frontend@0.1.0 dev
> next dev

  ▲ Next.js 14.0.0
  - Local: http://localhost:3000
```

✅ **Frontend running at http://localhost:3000**

---

## Step 6: Open Your Application

1. Go to **http://localhost:3000** in your browser
2. You should see a list of upcoming games!

### Explore the App

- **Home Page** (`/`) - Browse upcoming games
- **Game Page** (`/game/{gameId}`) - Click a game to see prediction
- **Dashboard** (`/dashboard`) - View accuracy metrics and factor weights

✅ **Your app is live!**

---

## Testing the Full Workflow

### Get a Game ID

1. Go to http://localhost:3000
2. Note a game ID from the list (e.g., `nba_2025_01_15_lakers_celtics`)

### Test the API

Open Terminal 4:

```bash
cd /Users/fullsail/bet-check

# Test API endpoints
python test_api.py
```

This will:
- ✓ Check backend health
- ✓ List all games
- ✓ Get a prediction for the first game
- ✓ Show current factor weights
- ✓ Display accuracy metrics

### Log a Game Result

```bash
curl -X POST http://localhost:8000/log_result \
  -H "Content-Type: application/json" \
  -d '{
    "game_id": "nba_2025_01_15_lakers_celtics",
    "actual_outcome": "Los Angeles Lakers"
  }'
```

✅ **The model learns and updates factor weights automatically!**

---

## Verify Everything is Working

Run this verification script:

```bash
cd /Users/fullsail/bet-check/scripts
python verify_db.py
```

Should show:
```
✓ games                            -   4 rows
✓ factors                          -   5 rows
✓ predictions                      -   1 rows
✓ results                          -   0 rows
```

---

## Troubleshooting

### "Connection Error: SUPABASE_URL not found"
- [ ] Copy and paste credentials into `.env` (not `.env.example`)
- [ ] Check quotes: `SUPABASE_URL=https://...` (no quotes needed)
- [ ] Restart the backend after updating `.env`

### "Backend won't start"
- [ ] Check Python 3.8+: `python --version`
- [ ] Port 8000 in use? `lsof -i :8000`
- [ ] Virtual environment activated? Check for `(venv)` in terminal

### "Frontend shows 'Failed to load games'"
- [ ] Is backend running? Check http://localhost:8000/health
- [ ] Check browser console (F12) for errors
- [ ] Verify `NEXT_PUBLIC_API_URL=http://localhost:8000` in `.env`

### "No games displaying"
- [ ] Did you run `python scripts/update_games.py`?
- [ ] Check Supabase: Settings → Logs for errors
- [ ] Run `python scripts/verify_db.py` to check database

### Database tables don't exist
- [ ] Did you run the `schema.sql` in Supabase SQL Editor?
- [ ] Click **Run** button (not just paste)
- [ ] Wait for success message

---

## Next Steps

### Learn the System

1. **API Documentation**: http://localhost:8000/docs (interactive)
2. **Read**: Check the main README.md for architecture details
3. **Experiment**: Change factor weights in Supabase and see predictions change

### Customize

Edit `/Users/fullsail/bet-check/backend/main.py`:
- **LEARNING_RATE** (line ~110): How fast the model learns
- **Factor weights**: Change initial base_weight values
- **Prediction logic**: Modify score calculations

### Add More Data

Use `scripts/update_games.py` to fetch more games (modify for your API):

```python
# Add more sports
SAMPLE_GAMES = [
    # NBA games
    # NFL games
    # MLB games
]
```

### Deploy

To deploy to production:
1. Use Docker: `docker-compose up`
2. Deploy backend to Heroku, Railway, or similar
3. Deploy frontend to Vercel, Netlify, or similar
4. Update `NEXT_PUBLIC_API_URL` to production backend URL

---

## File Structure Reference

```
bet-check/
├── backend/main.py           ← Prediction engine & API
├── frontend/pages/           ← Web pages
│   ├── index.tsx            ← Home (games list)
│   ├── game/[gameId].tsx    ← Prediction details
│   └── dashboard.tsx        ← Analytics & factors
├── scripts/
│   ├── seed_factors.py      ← Initialize factors
│   ├── update_games.py      ← Fetch games
│   └── verify_db.py         ← Check database
├── schema.sql               ← Database structure
├── .env                     ← Your secrets (created)
└── README.md               ← Full documentation
```

---

## Getting Help

1. **API Issues?** Check http://localhost:8000/docs
2. **Database Issues?** Run `python scripts/verify_db.py`
3. **Frontend Issues?** Open browser console (F12) and look for errors
4. **Code Questions?** Files have detailed comments explaining each section

---

**You're all set! Enjoy your sports prediction tool! 🎉**

*Questions? Check README.md or visit http://localhost:8000/docs*
