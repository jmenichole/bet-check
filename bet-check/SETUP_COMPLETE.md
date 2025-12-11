# ✅ Auto-Restart & Game Updates - Complete Setup

## Summary

You now have a fully automated BetCheck system on your Mac that:

### 🚀 Auto-Restart Features
- **Backend** automatically starts on Mac boot (port 9001)
- **Frontend** automatically starts on Mac boot (port 3001)
- **Game Updates** run automatically every 6 hours
- **Services auto-restart** if they crash (KeepAlive enabled)
- **All output logged** for debugging in `/Users/fullsail/bet-check/logs/`

### 📊 Game Configuration
| Setting | Value |
|---------|-------|
| **Games Displayed** | 4 |
| **Update Frequency** | Every 6 hours |
| **Source** | Demo games in `scripts/update_games.py` |
| **Data Location** | `SAMPLE_GAMES` array (lines 35-67) |
| **Backend Endpoint** | `GET /games` |

### 🎮 Current Games
1. Los Angeles Lakers vs Boston Celtics
2. Golden State Warriors vs Denver Nuggets
3. Miami Heat vs Milwaukee Bucks
4. Phoenix Suns vs Memphis Grizzlies

---

## 🔗 Access Your App

Once Mac restarts (or services are running):
- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:9001
- **API Docs:** http://localhost:9001/docs

---

## 📋 Service Status

All services configured and running:

```
✓ Backend FastAPI (port 9001)
  LaunchAgent: com.jmenichole.betcheck-backend
  Status: Running
  
✓ Frontend Next.js (port 3001)
  LaunchAgent: com.jmenichole.betcheck-frontend
  Status: Running
  
✓ Game Updates Scheduler
  LaunchAgent: com.jmenichole.betcheck-update-games
  Frequency: Every 6 hours (21,600 seconds)
  Status: Running
```

Check status anytime:
```bash
launchctl list | grep betcheck
```

---

## 🎛️ How to Customize

### Add More Games
Edit `/Users/fullsail/bet-check/scripts/update_games.py` and add more entries to `SAMPLE_GAMES`:

```python
SAMPLE_GAMES = [
    # ... existing games ...
    {
        "game_id": "nba_2025_01_19_lakers_warriors",
        "sport": "nba",
        "team_a": "Los Angeles Lakers",
        "team_b": "Golden State Warriors",
        "scheduled_date": (datetime.utcnow() + timedelta(days=5)).isoformat(),
        "result": None,
    },
]
```

### Change Update Frequency
Default is **every 6 hours**. To change:

```bash
nano ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

Find this section and change the value (in seconds):
```xml
<key>StartInterval</key>
<integer>21600</integer>  <!-- Change this number -->
```

Common values:
- 3600 = 1 hour
- 10800 = 3 hours
- 21600 = 6 hours (current)
- 43200 = 12 hours
- 86400 = 1 day

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Use Real Sports API Instead of Demo
1. Get API key from [RapidAPI - api-nba](https://rapidapi.com/api-nba/api/api-nba)
2. Add to `.env`: `SPORTS_API_KEY=your_key_here`
3. Edit `scripts/update_games.py` and uncomment the API call section (lines 81-90)

---

## 🔧 Service Management

### Stop All Services
```bash
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist
launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### Start All Services
```bash
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist
launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist
```

### View Logs
```bash
# Real-time game update logs
tail -f /Users/fullsail/bet-check/logs/games-update.log

# Backend logs
tail -f /Users/fullsail/bet-check/logs/backend.log

# Frontend logs
tail -f /Users/fullsail/bet-check/logs/frontend.log

# View all logs
ls -la /Users/fullsail/bet-check/logs/
```

### Manually Run Game Update
```bash
cd /Users/fullsail/bet-check/scripts
python3 update_games.py
```

---

## 📂 Important Files

| Path | Purpose |
|------|---------|
| `scripts/update_games.py` | Game data source - Edit to add/modify games |
| `backend/main.py` | API server - Returns games on `GET /games` |
| `logs/games-update.log` | Where game update logs are stored |
| `~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist` | Game update scheduler config |

---

## ❓ FAQ

**Q: Will it restart automatically after Mac restarts?**
A: Yes! All three services are configured with `RunAtLoad=true` and will start automatically on Mac boot.

**Q: How often do games update?**
A: Every 6 hours by default. Change the `StartInterval` value in the plist (in seconds).

**Q: How many games are shown?**
A: Currently 4. Add more by editing the `SAMPLE_GAMES` array in `scripts/update_games.py`.

**Q: Where are the games coming from?**
A: Demo data in `scripts/update_games.py`. To use real data, add an API key and uncomment the API call.

**Q: What if a service crashes?**
A: It automatically restarts thanks to the `KeepAlive=true` setting.

**Q: Where can I see what's happening?**
A: Check the log files in `/Users/fullsail/bet-check/logs/`.

**Q: How do I stop the services?**
A: Use `launchctl unload` command (see Service Management section above).

---

## 📝 Files Generated

These files were created for you:
- `setup_auto_restart.sh` - Main setup script (executable)
- `AUTO_RESTART_CONFIG.md` - Detailed configuration guide
- `GAME_UPDATES_QUICK_REF.md` - Quick reference guide
- `SETUP_COMPLETE.md` - This file

---

## ✨ You're All Set!

Your BetCheck system is now:
- ✅ Automatically running backend and frontend
- ✅ Updating games every 6 hours
- ✅ Restarting automatically on Mac boot
- ✅ Logging all activity for debugging
- ✅ Fully operational and ready to use

**Made for degens by degens** ❤️

Copyright (c) 2025 Jmenichole
https://jmenichole.github.io/Portfolio/
