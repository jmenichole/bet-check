# BetCheck Auto-Restart & Game Updates Configuration

## 📋 Current Configuration

### Game Update Schedule
- **Frequency:** Every 6 hours (21,600 seconds)
- **Source:** Sample games (demo mode - no API key required)
- **Games Displayed:** 4 upcoming NBA games
- **Database:** Supabase PostgreSQL (demo fallback if unavailable)

### Games Currently Available
The system displays 4 sample NBA games:
1. **Los Angeles Lakers vs Boston Celtics** - Day 1
2. **Golden State Warriors vs Denver Nuggets** - Day 2
3. **Miami Heat vs Milwaukee Bucks** - Day 3
4. **Phoenix Suns vs Memphis Grizzlies** - Day 4

**Data Source:** `scripts/update_games.py` → Demo games (SAMPLE_GAMES array)
**Backend Endpoint:** `GET /games` (returns all games from database or demo data)
**Frontend Display:** Home page lists all available games

---

## 🚀 Auto-Restart Setup

### Installation
```bash
cd /Users/fullsail/bet-check
chmod +x setup_auto_restart.sh
./setup_auto_restart.sh
```

### What It Does
1. **Creates logs directory** for debugging
2. **Updates games immediately** on setup
3. **Creates 3 LaunchAgent services:**
   - Backend FastAPI (port 9001) - Always on
   - Frontend Next.js (port 3001) - Always on
   - Game Updates - Every 6 hours

### MacOS LaunchAgent Files Created
All files are stored in `~/Library/LaunchAgents/`:
- `com.jmenichole.betcheck-backend.plist` - Backend service
- `com.jmenichole.betcheck-frontend.plist` - Frontend service
- `com.jmenichole.betcheck-update-games.plist` - Game update scheduler

---

## 🔧 Manual Service Management

### Check Status
```bash
launchctl list | grep betcheck
```

### Start Services
```bash
# Start Backend
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist

# Start Frontend
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist

# Start Game Updates
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Stop Services
```bash
# Stop Backend
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist

# Stop Frontend
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist

# Stop Game Updates
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Restart Services
```bash
# Unload and reload
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
```

---

## 📊 Game Update Details

### Update Interval
- **Default:** Every 6 hours (21,600 seconds)
- **Can be modified:** Edit the `<key>StartInterval</key>` value in the plist file

### Number of Games
- **Current:** 4 games displayed
- **Update source:** `scripts/update_games.py`
- **Demo mode:** Generates games starting from current date + 1 to 4 days

### To Display More Games
Edit `/Users/fullsail/bet-check/scripts/update_games.py`:
```python
SAMPLE_GAMES = [
    # Add more game dictionaries here following the same pattern
    {
        "game_id": "nba_2025_01_19_game_name",
        "sport": "nba",
        "team_a": "Team A",
        "team_b": "Team B",
        "scheduled_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "result": None,
    },
]
```

### To Use Real Sports API
1. Get API key from [RapidAPI - api-nba](https://rapidapi.com/api-nba/api/api-nba)
2. Add `SPORTS_API_KEY` to `.env` file
3. Uncomment the API call in `scripts/update_games.py`:
   ```python
   def fetch_nba_games():
       headers = {
           "x-rapidapi-host": RAPIDAPI_HOST,
           "x-rapidapi-key": RAPIDAPI_KEY
       }
       # ... API call code
   ```

---

## 📁 Log Files Location
All logs are stored in `/Users/fullsail/bet-check/logs/`:

| Log File | Purpose |
|----------|---------|
| `backend.log` | Backend startup and API logs |
| `backend-error.log` | Backend errors |
| `backend-stdout.log` | Backend standard output |
| `frontend.log` | Frontend build and dev server logs |
| `frontend-error.log` | Frontend errors |
| `frontend-stdout.log` | Frontend standard output |
| `games-update.log` | Game update script output |
| `games-update-error.log` | Game update errors |
| `games-update-stdout.log` | Game update standard output |

### View Logs
```bash
# Follow backend logs in real-time
tail -f /Users/fullsail/bet-check/logs/backend.log

# View last 50 lines of game updates
tail -50 /Users/fullsail/bet-check/logs/games-update.log

# View all logs
ls -lah /Users/fullsail/bet-check/logs/
```

---

## 🌐 Access Points

Once auto-restart is configured and Mac boots:
- **Frontend:** http://localhost:3001
- **Backend API:** https://jmenichole.github.io/bet-check
- **API Documentation:** https://jmenichole.github.io/bet-check/docs (Swagger UI)

---

## ⚙️ Customization

### Change Update Interval
To modify game update frequency (in seconds):
```bash
# Edit the plist file
nano ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist

# Find this section and change the value:
<key>StartInterval</key>
<integer>21600</integer>  <!-- Change this number (in seconds) -->

# Reload the service
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

**Common intervals:**
- 3600 = 1 hour
- 7200 = 2 hours
- 10800 = 3 hours
- 21600 = 6 hours (default)
- 43200 = 12 hours
- 86400 = 24 hours (1 day)

### Change Game Limit
To display more games, modify `scripts/update_games.py`:
1. Add more entries to `SAMPLE_GAMES` array
2. Or configure real API key and modify `fetch_nba_games()` function

---

## 🔍 Troubleshooting

### Services Not Starting
```bash
# Check if LaunchAgent is loaded
launchctl list | grep betcheck

# View error logs
tail /Users/fullsail/bet-check/logs/backend-error.log
tail /Users/fullsail/bet-check/logs/frontend-error.log
```

### Port Already in Use
If ports 3001 or 9001 are in use:
```bash
# Find process using port
lsof -i :3001
lsof -i :9001

# Kill process
kill -9 <PID>
```

### Games Not Updating
```bash
# Check game update logs
tail -f /Users/fullsail/bet-check/logs/games-update.log

# Manually run update script
cd /Users/fullsail/bet-check/scripts
python3 update_games.py
```

### Services Keep Stopping
- Check log files for errors
- Ensure virtual environment is properly configured
- Verify paths in plist files are correct

---

## 📝 Notes

- **Auto-restart enabled on Mac boot** ✅
- **Frontend and backend run as background services** ✅
- **Games update every 6 hours automatically** ✅
- **All output logged for debugging** ✅
- **Services restart if they crash** (KeepAlive setting) ✅

## Copyright
Copyright (c) 2025 Jmenichole - MIT License
https://jmenichole.github.io/Portfolio/
