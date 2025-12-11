#!/bin/bash
# BetCheck Auto-Restart Script for macOS
# 
# Copyright (c) 2025 Jamie McNichol
# Licensed under MIT License
# https://jmenichole.github.io/Portfolio/
#
# This script sets up automatic restart on Mac startup and handles game updates
# Run: chmod +x setup_auto_restart.sh && ./setup_auto_restart.sh

set -e

PROJECT_ROOT="/Users/fullsail/bet-check"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
VENV_PATH="$BACKEND_DIR/venv"
PLIST_DIR="$HOME/Library/LaunchAgents"
LOG_DIR="$PROJECT_ROOT/logs"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}BetCheck Auto-Restart Setup${NC}"
echo -e "${BLUE}================================${NC}\n"

# Create logs directory
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✓${NC} Created logs directory"

# 1. Update games immediately
echo -e "\n${BLUE}1. Updating games database...${NC}"
cd "$SCRIPTS_DIR"
if [ -f "$VENV_PATH/bin/python" ]; then
    source "$VENV_PATH/bin/activate"
    python3 update_games.py
    echo -e "${GREEN}✓${NC} Games updated"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found"
fi

# 2. Create LaunchAgent plist for Backend
echo -e "\n${BLUE}2. Setting up Backend auto-restart...${NC}"

BACKEND_PLIST="$PLIST_DIR/com.jmenichole.betcheck-backend.plist"

cat > "$BACKEND_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jmenichole.betcheck-backend</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd /Users/fullsail/bet-check/backend && /Users/fullsail/bet-check/backend/venv/bin/python main.py >> /Users/fullsail/bet-check/logs/backend.log 2>&1</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/Users/fullsail/bet-check/logs/backend-error.log</string>
    <key>StandardOutPath</key>
    <string>/Users/fullsail/bet-check/logs/backend-stdout.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/fullsail/bet-check</string>
</dict>
</plist>
EOF

chmod 644 "$BACKEND_PLIST"
echo -e "${GREEN}✓${NC} Backend LaunchAgent created: $BACKEND_PLIST"

# 3. Create LaunchAgent plist for Frontend
echo -e "\n${BLUE}3. Setting up Frontend auto-restart...${NC}"

FRONTEND_PLIST="$PLIST_DIR/com.jmenichole.betcheck-frontend.plist"

cat > "$FRONTEND_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jmenichole.betcheck-frontend</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd /Users/fullsail/bet-check/frontend && npm run dev >> /Users/fullsail/bet-check/logs/frontend.log 2>&1</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>/Users/fullsail/bet-check/logs/frontend-error.log</string>
    <key>StandardOutPath</key>
    <string>/Users/fullsail/bet-check/logs/frontend-stdout.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/fullsail/bet-check</string>
</dict>
</plist>
EOF

chmod 644 "$FRONTEND_PLIST"
echo -e "${GREEN}✓${NC} Frontend LaunchAgent created: $FRONTEND_PLIST"

# 4. Create LaunchAgent plist for Game Updates (runs every 6 hours)
echo -e "\n${BLUE}4. Setting up Game Update scheduler (every 6 hours)...${NC}"

UPDATE_PLIST="$PLIST_DIR/com.jmenichole.betcheck-update-games.plist"

cat > "$UPDATE_PLIST" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jmenichole.betcheck-update-games</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd /Users/fullsail/bet-check/scripts && /Users/fullsail/bet-check/backend/venv/bin/python3 update_games.py >> /Users/fullsail/bet-check/logs/games-update.log 2>&1</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardErrorPath</key>
    <string>/Users/fullsail/bet-check/logs/games-update-error.log</string>
    <key>StandardOutPath</key>
    <string>/Users/fullsail/bet-check/logs/games-update-stdout.log</string>
    <key>WorkingDirectory</key>
    <string>/Users/fullsail/bet-check</string>
</dict>
</plist>
EOF

chmod 644 "$UPDATE_PLIST"
echo -e "${GREEN}✓${NC} Game Update LaunchAgent created: $UPDATE_PLIST"

# 5. Load LaunchAgents
echo -e "\n${BLUE}5. Loading LaunchAgents...${NC}"

launchctl load "$BACKEND_PLIST" 2>/dev/null || launchctl unload "$BACKEND_PLIST" 2>/dev/null; launchctl load "$BACKEND_PLIST"
echo -e "${GREEN}✓${NC} Backend LaunchAgent loaded"

launchctl load "$FRONTEND_PLIST" 2>/dev/null || launchctl unload "$FRONTEND_PLIST" 2>/dev/null; launchctl load "$FRONTEND_PLIST"
echo -e "${GREEN}✓${NC} Frontend LaunchAgent loaded"

launchctl load "$UPDATE_PLIST" 2>/dev/null || launchctl unload "$UPDATE_PLIST" 2>/dev/null; launchctl load "$UPDATE_PLIST"
echo -e "${GREEN}✓${NC} Game Update LaunchAgent loaded"

# 6. Summary
echo -e "\n${BLUE}================================${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}================================${NC}\n"

echo -e "${GREEN}Services configured:${NC}"
echo "  • Backend FastAPI (port 9001) - Auto-starts on Mac boot"
echo "  • Frontend Next.js (port 3001) - Auto-starts on Mac boot"
echo "  • Game Updates - Runs every 6 hours (21,600 seconds)"
echo ""
echo -e "${GREEN}Log files location:${NC}"
echo "  • Backend: $LOG_DIR/backend.log"
echo "  • Frontend: $LOG_DIR/frontend.log"
echo "  • Game Updates: $LOG_DIR/games-update.log"
echo ""
echo -e "${GREEN}To manage services:${NC}"
echo "  • Stop Backend:   launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist"
echo "  • Start Backend:  launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-backend.plist"
echo "  • Stop Frontend:  launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist"
echo "  • Start Frontend: launchctl load ~/Library/LaunchAgents/com.jmenichole.betcheck-frontend.plist"
echo "  • Stop Updates:   launchctl unload ~/Library/LaunchAgents/com.jmenichole.betcheck-update-games.plist"
echo ""
echo -e "${GREEN}Check service status:${NC}"
echo "  • launchctl list | grep betcheck"
echo ""
echo -e "${YELLOW}Access BetCheck:${NC}"
echo "  • Frontend: http://localhost:3001"
echo "  • Backend:  https://jmenichole.github.io/bet-check"
echo "  • API Docs: https://jmenichole.github.io/bet-check/docs"
