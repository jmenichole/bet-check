# ✅ Launch Checklist (Reference)

For quick setup, use `README.md` and `QUICK_START_GUIDE.md`. This checklist is a longer reference.

---

## Phase 1: Supabase Setup (5 minutes)

- [ ] **Create Supabase Account**
  - Go to https://supabase.com/sign-up
  - Sign up with email or GitHub
  
- [ ] **Create New Project**
  - Click "New Project"
  - Project name: `bet-check`
  - Password: (save this, you'll need it)
  - Region: closest to you
  - Click "Create new project"
  - ⏳ Wait 2-3 minutes for database to initialize

- [ ] **Get Credentials**
  - Click **Settings** (bottom left)
  - Go to **API** tab
  - Copy **Project URL** (starts with `https://`)
  - Copy **anon public** key
  - Save both temporarily (next step)

- [ ] **Create Database Schema**
  - Go to **SQL Editor** (left sidebar)
  - Click **New Query**
  - Open file: `/Users/fullsail/bet-check/schema.sql`
  - Copy ALL the SQL code
  - Paste into Supabase SQL editor
  - Click **Run** (top right)
  - ✅ Wait for success message

---

## Phase 2: Environment Setup (2 minutes)

- [ ] **Create .env File**
  ```bash
  cd /Users/fullsail/bet-check
  cp .env.example .env
  ```

- [ ] **Edit .env with Your Credentials**
  - Open `.env` in text editor
  - Paste your **Project URL** after `SUPABASE_URL=`
  - Paste your **anon key** after `SUPABASE_KEY=`
  - Save file
  
  Example (replace with YOUR values):
  ```env
  SUPABASE_URL=https://xyzabc.supabase.co
  SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI...
  SPORTS_API_KEY=demo
  BACKEND_PORT=8000
  BACKEND_HOST=0.0.0.0
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

- [ ] **Verify .env is Created**
  ```bash
  ls -la /Users/fullsail/bet-check/.env
  ```

---

## Phase 3: Backend Setup (3 minutes)

- [ ] **Open Terminal 1 (Backend)**
  ```bash
  cd /Users/fullsail/bet-check/backend
  ```

- [ ] **Create Python Virtual Environment**
  ```bash
  python3 -m venv venv
  ```

- [ ] **Activate Virtual Environment**
  ```bash
  source venv/bin/activate
  ```
  ✅ You should see `(venv)` at start of terminal prompt

- [ ] **Install Python Dependencies**
  ```bash
  pip install -r ../requirements.txt
  ```
  ⏳ Wait 30-60 seconds

- [ ] **Start Backend Server**
  ```bash
  python main.py
  ```
  
  ✅ Expected output:
  ```
  INFO:     Uvicorn running on http://0.0.0.0:8000
  INFO:     Application startup complete
  ```

- [ ] **Test Backend Health** (in new browser tab)
  - Open: http://localhost:8000/health
  - ✅ Should show: `{"status":"healthy"}`

---

## Phase 4: Data Seeding (2 minutes)

- [ ] **Open Terminal 2 (Scripts)**
  ```bash
  cd /Users/fullsail/bet-check/scripts
  ```

- [ ] **Seed Factor Weights**
  ```bash
  python seed_factors.py
  ```
  
  ✅ Expected output:
  ```
  Seeding factors into Supabase...
  ✓ Inserted factor: Recent Form
  ✓ Inserted factor: Injury Status
  ✓ Inserted factor: Offensive Efficiency
  ✓ Inserted factor: Defensive Efficiency
  ✓ Inserted factor: Home Court Advantage
  
  ✓ Factors seeded successfully!
  ```

- [ ] **Update Games List**
  ```bash
  python update_games.py
  ```
  
  ✅ Expected output:
  ```
  Fetching upcoming games...
  Using sample games for demo...
  Found 4 upcoming games
  ✓ Upserted game: Los Angeles Lakers vs Boston Celtics
  ...
  ✓ Successfully updated 4 games!
  ```

- [ ] **Verify Database** (optional)
  ```bash
  python verify_db.py
  ```
  
  ✅ Should show:
  ```
  ✓ games                 -  4 rows
  ✓ factors              -  5 rows
  ```

---

## Phase 5: Frontend Setup (3 minutes)

- [ ] **Open Terminal 3 (Frontend)**
  ```bash
  cd /Users/fullsail/bet-check/frontend
  ```

- [ ] **Install Node Dependencies**
  ```bash
  npm install
  ```
  ⏳ Wait 1-2 minutes

- [ ] **Start Frontend Development Server**
  ```bash
  npm run dev
  ```
  
  ✅ Expected output:
  ```
  > bet-check-frontend@0.1.0 dev
  > next dev
  
    ▲ Next.js 14.0.0
    - Local:        http://localhost:3000
  ```

- [ ] **Open Frontend in Browser**
  - Go to: http://localhost:3000
  - ✅ You should see a page titled "Bet Check"
  - ✅ Games list should display 4 upcoming games

---

## Phase 6: Testing (5 minutes)

- [ ] **Test Games Page**
  - Go to: http://localhost:3000
  - ✅ See "Upcoming Games" heading
  - ✅ See 4 game cards (Lakers vs Celtics, etc.)
  - ✅ Games show date and team names

- [ ] **Click on a Game**
  - Click "View Prediction →" on any game card
  - ✅ See game prediction details
  - ✅ See predicted winner
  - ✅ See confidence percentage
  - ✅ See top 3 reasons

- [ ] **View Dashboard**
  - Click "Dashboard" link in header
  - ✅ See "Prediction Accuracy" section
  - ✅ See factor weights
  - ✅ See "Insufficient data" message (normal - no results logged yet)

- [ ] **Test API Documentation**
  - Go to: http://localhost:8000/docs
  - ✅ See Swagger UI with all endpoints
  - ✅ Can expand and read each endpoint

- [ ] **Run Full API Test** (Terminal 4)
  ```bash
  cd /Users/fullsail/bet-check
  python test_api.py
  ```
  
  ✅ Should show:
  ```
  ✓ Health check passed
  ✓ Games fetched: 4
  ✓ Prediction generated
  ✓ Factors loaded: 5
  ✓ Analytics retrieved
  
  ✓ All tests completed!
  ```

---

## Phase 7: Log Your First Result (Optional - shows learning)

- [ ] **Get a Game ID**
  - Go to http://localhost:3000
  - Note a game ID (e.g., `nba_2025_01_15_lakers_celtics`)

- [ ] **Get the Prediction**
  - Click on that game
  - Note what it predicts (e.g., "Lakers wins")

- [ ] **Log the Result** (Terminal 4)
  ```bash
  curl -X POST http://localhost:8000/log_result \
    -H "Content-Type: application/json" \
    -d '{
      "game_id": "nba_2025_01_15_lakers_celtics",
      "actual_outcome": "Los Angeles Lakers"
    }'
  ```
  
  ✅ Response:
  ```json
  {
    "status": "success",
    "message": "Result logged...",
    "weights_updated": true
  }
  ```

- [ ] **Check Dashboard**
  - Go to: http://localhost:3000/dashboard
  - ✅ Accuracy should now show 1 prediction, 1 correct
  - ✅ Factor weights may have changed slightly

---

## ✅ Final Verification

Run this checklist to confirm everything works:

- [ ] Backend running: http://localhost:8000/health → shows `{"status":"healthy"}`
- [ ] Frontend running: http://localhost:3000 → shows games list
- [ ] Games display: Can see 4 game cards
- [ ] Predictions work: Click game → see prediction page
- [ ] Dashboard shows: Metrics and factor weights
- [ ] API docs work: http://localhost:8000/docs → shows Swagger UI
- [ ] Database has data: 
  ```bash
  python scripts/verify_db.py
  ```

---

## 🎉 Success Indicators

You're done when you see:

✅ **Backend Terminal**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ **Frontend Terminal**
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
```

✅ **Browser at localhost:3000**
- Page loads without errors
- Games list displays
- Can click games and see predictions

✅ **Database**
```
✓ games                 -  4 rows
✓ factors              -  5 rows
✓ predictions          -  1+ rows
```

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "Cannot find module 'fastapi'" | Run: `pip install -r requirements.txt` |
| "SUPABASE_URL not found" | Edit `.env` and add credentials |
| "npm command not found" | Install Node.js from nodejs.org |
| "Port 8000 in use" | Change BACKEND_PORT in .env |
| "No games displaying" | Run: `python scripts/update_games.py` |
| "Failed to connect to API" | Is backend running? Check terminal 1 |
| "Tables don't exist" | Did you run schema.sql in Supabase? |

---

## Next Steps After Launch

Once everything is working:

1. **Experiment with Learning**
   - Log multiple game results
   - Watch factor weights change in dashboard

2. **Customize**
   - Edit factor names/descriptions
   - Adjust learning rate in `backend/main.py`
   - Change colors in `frontend/styles/globals.css`

3. **Add Real Data**
   - Modify `scripts/update_games.py` for real sports API
   - Add more factors to prediction engine
   - Integrate betting lines

4. **Deploy** (when ready)
   - Backend: Railway, Heroku, or similar
   - Frontend: Vercel or Netlify
   - Update `NEXT_PUBLIC_API_URL` to production URL

---

## Documentation References

- **Setup Help**: QUICKSTART.md
- **Full Docs**: README.md
- **File Descriptions**: FILE_STRUCTURE.md
- **What Was Built**: GENERATION_SUMMARY.md
- **API Docs**: http://localhost:8000/docs (when running)

---

## Important Notes

⚠️ **Keep your .env file secret!** It contains your Supabase credentials
- Add `.env` to `.gitignore` (already done)
- Never commit `.env` to git
- Never share `.env` contents

💡 **Terminal Windows Stay Open**
- Keep all 3 terminal windows open while developing
- If you close one, restart it using the commands above

📱 **Mobile Testing**
- Frontend is mobile responsive
- Test on phone by going to: `http://[YOUR_IP]:3000`

---

## Getting Help

1. **Backend issues?**
   - Check: http://localhost:8000/docs (API documentation)
   - Check terminal output for error messages
   - Run: `python scripts/verify_db.py`

2. **Frontend issues?**
   - Open browser console: F12 → Console tab
   - Check if backend is running
   - Check `.env` for correct `NEXT_PUBLIC_API_URL`

3. **Database issues?**
   - Check Supabase dashboard
   - Verify schema.sql was run
   - Check credentials in `.env`

---

**You're ready to go! Start with Phase 1 and work through each phase in order.** 🚀

*Estimated total time: 20-30 minutes*

When you reach Phase 6 testing successfully, your app is fully operational! 🎉
