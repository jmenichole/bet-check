# BetCheck Quick Reference - Game Updates & Auto-Restart

## 📊 Game Update Summary

### Current Setup
| Setting | Value |
|---------|-------|
| **Update Frequency** | Every 6 hours (21,600 seconds) |
| **Games Displayed** | 4 games |
| **Data Source** | Demo games (sample data) |
| **Update Method** | Automated via LaunchAgent |
| **First Update** | On Mac startup |

### Games Currently Shown
```
1. Los Angeles Lakers vs Boston Celtics (Day 1)
2. Golden State Warriors vs Denver Nuggets (Day 2)
3. Miami Heat vs Milwaukee Bucks (Day 3)
4. Phoenix Suns vs Memphis Grizzlies (Day 4)
```

### Games Sourced From
- **File:** `/Users/fullsail/bet-check/scripts/update_games.py`
- **Array:** `SAMPLE_GAMES` (lines 35-67)
- **Schedule:** Updated by LaunchAgent every 6 hours
- **Database:** Supabase PostgreSQL (fallback to demo mode if unavailable)

---

## 🚀 Auto-Restart Status

### ✅ Currently Active
```
✓ Backend FastAPI (port 9001)
  - Status: Running
  - LaunchAgent: com.jmenichole.betcheck-backend
  - Restart Policy: Automatic (KeepAlive enabled)
  
✓ Frontend Next.js (port 3001)
  - Status: Running
  - LaunchAgent: com.jmenichole.betcheck-frontend
  - Restart Policy: Automatic (KeepAlive enabled)

✓ Game Updates Scheduler
  - Status: Running
  - LaunchAgent: com.jmenichole.betcheck-update-games
  - Frequency: Every 6 hours
  - Last Run: After setup script execution
```

### What Happens on Mac Restart
1. **Services automatically start** on boot
2. **Game updates** run on schedule
3. **Logs written** to `/Users/fullsail/bet-check/logs/`
4. **Services restart if they crash** (KeepAlive = true)

---

## 🔧 Quick Commands

### Check Service Status
```bash
launchctl list | grep betcheck
```

### View Game Update Logs
```bash
# Real-time
tail -f /Users/fullsail/bet-check/logs/games-update.log

# Last 20 lines
tail -20 /Users/fullsail/bet-check/logs/games-update.log
```

### Manually Trigger Game Update
```bash
cd /Users/fullsail/bet-check/scripts
python3 update_games.py
```

### Add More Games
Edit `/Users/fullsail/bet-check/scripts/update_games.py`:
```python
SAMPLE_GAMES = [
    # Existing 4 games...
    {
        "game_id": "nba_2025_01_19_new_team_a_new_team_b",
        "sport": "nba",
        "team_a": "New Team A",
        "team_b": "New Team B",
        "scheduled_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "result": None,
    },
]
```

### Change Update Frequency
```bash
# Current: Every 6 hours
# 1 hour = 3600
# 3 hours = 10800
# 12 hours = 43200
# 24 hours = 86400

# Edit the plist:
nano ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist

# Find and change this line:
# <integer>21600</integer>  ← Change 21600 to desired seconds

# Reload service:
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Stop Services
```bash
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Start Services
```bash
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

---

## 📱 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3001 | Games dashboard & predictions |
| **Backend API** | http://localhost:9001 | REST API |
| **API Docs** | http://localhost:9001/docs | Swagger UI documentation |

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `/Users/fullsail/bet-check/scripts/update_games.py` | Game update script |
| `/Users/fullsail/bet-check/logs/games-update.log` | Game update logs |
| `~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist` | Game update scheduler config |

---

## 🎮 Demo vs Real API

### Current: Demo Mode
- ✅ 4 sample games
- ✅ No API key needed
- ✅ Games refresh every 6 hours
- ✅ Always available

### To Switch to Real NBA Data
1. Get API key from [RapidAPI - api-nba](https://rapidapi.com/api-nba/api/api-nba)
2. Add to `.env`: `SPORTS_API_KEY=your_key_here`
3. Uncomment API code in `scripts/update_games.py` (lines 81-90)
4. Increase game limit as needed

---

## 📝 Summary

| Question | Answer |
|----------|--------|
| **How often do games update?** | Every 6 hours automatically |
| **How many games shown?** | 4 games currently |
| **Where are games from?** | `/scripts/update_games.py` SAMPLE_GAMES array |
| **Auto-restart on Mac boot?** | ✅ YES - All 3 services configured |
| **Where are logs?** | `/Users/fullsail/bet-check/logs/` |
| **What happens if service crashes?** | Automatically restarts (KeepAlive = true) |
| **Can I change update frequency?** | ✅ YES - Edit StartInterval in plist (in seconds) |
| **Can I add more games?** | ✅ YES - Edit SAMPLE_GAMES array or use real API |

---

## Copyright
Copyright (c) 2025 Jamie McNichol - MIT License
https://jmenichole.github.io/Portfolio/
