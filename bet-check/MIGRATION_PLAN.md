# Migration Plan: bet-check → tiltcheck-monorepo

**Document Version:** 1.0  
**Created:** 2025-12-18  
**Author:** Jamie Vargas  
**Purpose:** Safe migration of bet-check project into tiltcheck-monorepo without breaking functionality

---

## Executive Summary

This document provides a comprehensive, step-by-step plan to migrate the `bet-check` project into the `tiltcheck-monorepo` repository. The migration will preserve all functionality, maintain deployment capabilities, and integrate seamlessly with any existing monorepo structure.

**Estimated Migration Time:** 2-4 hours  
**Risk Level:** Low (with proper testing)  
**Rollback Time:** <15 minutes

---

## Table of Contents

1. [Current Project Analysis](#1-current-project-analysis)
2. [Pre-Migration Checklist](#2-pre-migration-checklist)
3. [Migration Strategy](#3-migration-strategy)
4. [Step-by-Step Migration Process](#4-step-by-step-migration-process)
5. [Post-Migration Verification](#5-post-migration-verification)
6. [Rollback Plan](#6-rollback-plan)
7. [Common Issues & Solutions](#7-common-issues--solutions)

---

## 1. Current Project Analysis

### 1.1 Project Overview

**bet-check** is a full-stack sports prediction application with:
- Real-time game predictions using adaptive ML algorithms
- AI-powered sports guru chat interface
- Mines game implementation
- Analytics dashboard
- Multi-sport support (NBA, NFL, MLB)

### 1.2 Technology Stack

#### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Runtime:** Uvicorn ASGI server
- **Dependencies:** 
  - fastapi==0.104.1
  - uvicorn==0.24.0
  - pydantic==2.12.5
  - python-dotenv==1.0.0
  - supabase==2.3.4
  - requests==2.32.4
  - httpx==0.25.0
  - numpy>=1.26.0

#### Frontend
- **Framework:** Next.js 14.0.0 (React 18.2.0)
- **Language:** TypeScript 5.3.3
- **Styling:** Tailwind CSS 3.3.6
- **Key Dependencies:**
  - axios==1.6.2
  - react-icons==5.5.0
  - clsx==2.0.0

#### Database
- **Service:** Supabase (PostgreSQL)
- **Tables:** games, factors, results, predictions, chat_messages, mines_games
- **Schema Files:** 
  - schema.sql (core tables)
  - schema_chat.sql (chat feature)
  - schema_mines_crash.sql (games feature)
  - disable_rls.sql (security config)

#### Infrastructure
- **Containerization:** Docker Compose
- **Deployment:** Render.com, Railway support
- **Ports:** 
  - Backend: 8000 (default), 9001 (alt)
  - Frontend: 3000 (default), 9000 (alt)

### 1.3 Current File Structure

```
bet-check/
├── backend/                    # FastAPI backend
│   ├── main.py                # Core API & prediction engine
│   ├── db.py                  # Database utilities
│   ├── mines.py               # Mines game logic
│   ├── mines_engine.py        # Mines game engine
│   ├── limbo_crash_engine.py  # Crash game engine
│   └── result_fetcher.py      # ESPN result fetcher
├── frontend/                   # Next.js frontend
│   ├── components/            # React components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── ChatEmbedded.tsx
│   │   ├── ConfidenceMeter.tsx
│   │   ├── Footer.tsx
│   │   ├── Header.tsx
│   │   ├── PopularMatchesList.tsx
│   │   └── ReasonItem.tsx
│   ├── pages/                 # Next.js pages
│   │   ├── _app.tsx
│   │   ├── _document.tsx
│   │   ├── index.tsx          # Home page
│   │   ├── dashboard.tsx      # Analytics
│   │   ├── guru.tsx           # AI chat
│   │   ├── mines.tsx          # Mines game
│   │   ├── past-games.tsx     # History
│   │   └── game/[gameId].tsx  # Game details
│   ├── styles/
│   │   └── globals.css        # Tailwind styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
├── scripts/                    # Utility scripts
│   ├── seed_factors.py        # Initialize factors
│   ├── update_games.py        # Fetch games
│   └── verify_db.py           # Database verification
├── .github/                    # GitHub workflows
│   └── workflows/
├── schema.sql                  # Database schema
├── schema_chat.sql            # Chat schema
├── schema_mines_crash.sql     # Games schema
├── disable_rls.sql            # Security config
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker orchestration
├── Dockerfile.backend         # Backend container
├── Procfile                   # Heroku/Railway config
├── render.yaml                # Render.com config
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
└── [30+ documentation files]  # Setup & deployment guides
```

### 1.4 External Dependencies

#### Required Services
1. **Supabase Project**
   - Database URL
   - Anon/Service key
   - RLS policies configured

2. **Sports API** (Optional)
   - RapidAPI key for live data
   - Falls back to demo mode

#### Environment Variables
```env
SUPABASE_URL=https://[project].supabase.co
SUPABASE_KEY=sb_publishable_[key]
SPORTS_API_KEY=demo
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 1.5 Critical Integration Points

1. **Backend → Supabase:** All database operations via Supabase client
2. **Frontend → Backend:** REST API calls to NEXT_PUBLIC_API_URL
3. **Docker Compose:** Network bridge for internal communication
4. **CORS:** Configured to allow frontend origin

---

## 2. Pre-Migration Checklist

### 2.1 Required Information

- [ ] **Monorepo Structure:** Understand tiltcheck-monorepo organization
  - Root directory structure
  - Existing package/app naming conventions
  - Shared dependencies location
  - Build system (npm workspaces, turborepo, lerna, etc.)

- [ ] **Existing Applications:** Identify current apps in monorepo
  - App naming pattern (e.g., `apps/bet-check`, `packages/bet-check`)
  - Port allocation strategy
  - Shared component libraries
  - Common configuration files

- [ ] **Infrastructure:** Document monorepo deployment setup
  - Docker Compose setup (if exists)
  - CI/CD pipelines
  - Environment variable management
  - Database access patterns

### 2.2 Pre-Migration Tasks

#### In bet-check Repository

- [ ] **Create backup branch**
  ```bash
  cd /path/to/bet-check
  git checkout main
  git pull origin main
  git checkout -b backup/pre-migration-$(date +%Y%m%d)
  git push origin backup/pre-migration-$(date +%Y%m%d)
  ```

- [ ] **Document current state**
  ```bash
  # Test all services are working
  docker-compose up --build
  # Verify frontend: http://localhost:3000
  # Verify backend: http://localhost:8000/docs
  # Verify API health: curl http://localhost:8000/health
  
  # Run tests
  python test_api.py
  python test_chat.py
  
  # Export database schema
  # (If using Supabase, download current schema from dashboard)
  ```

- [ ] **Identify local modifications**
  ```bash
  git status
  git diff origin/main
  ```

- [ ] **Document environment variables**
  ```bash
  cp .env .env.backup
  # Store sensitive values securely (1Password, LastPass, etc.)
  ```

#### In tiltcheck-monorepo Repository

- [ ] **Clone and explore monorepo**
  ```bash
  git clone https://github.com/jmenichole/tiltcheck-monorepo
  cd tiltcheck-monorepo
  git checkout main
  git pull origin main
  ```

- [ ] **Create migration branch**
  ```bash
  git checkout -b feature/migrate-bet-check
  ```

- [ ] **Analyze monorepo structure**
  ```bash
  tree -L 2 -I 'node_modules|.git'
  cat package.json  # Check for workspaces configuration
  cat lerna.json    # Check if using Lerna
  cat turbo.json    # Check if using Turborepo
  ```

- [ ] **Check for conflicts**
  - Port usage (8000, 3000, 9000, 9001)
  - Package naming
  - Shared dependency versions
  - Environment variable naming

---

## 3. Migration Strategy

### 3.1 Recommended Monorepo Structure

Based on common monorepo patterns, the recommended structure is:

```
tiltcheck-monorepo/
├── apps/                       # Applications
│   ├── bet-check-backend/     # Migrated backend
│   └── bet-check-frontend/    # Migrated frontend
├── packages/                   # Shared packages (optional)
│   ├── ui/                    # Shared UI components
│   └── utils/                 # Shared utilities
├── infrastructure/             # Docker, K8s configs
│   └── docker/
│       └── bet-check/
│           ├── docker-compose.yml
│           └── Dockerfile.backend
├── docs/                      # Documentation
│   └── bet-check/
└── scripts/                   # Shared scripts
```

**Alternative Structure** (if monorepo uses different pattern):
```
tiltcheck-monorepo/
├── services/
│   └── bet-check/            # All bet-check code
│       ├── backend/
│       ├── frontend/
│       └── docker-compose.yml
```

### 3.2 Migration Approach

**Option A: Preserve Git History (Recommended)**
- Use `git subtree` or `git filter-repo` to maintain commit history
- Preserves contributors, blame, and historical context
- More complex but professional

**Option B: Fresh Copy**
- Copy files directly into monorepo
- Simpler and faster
- Loses git history but easier to troubleshoot

**Recommendation:** Use Option B for speed, but document Option A steps for reference.

### 3.3 Key Modifications Required

1. **Path Updates**
   - Backend imports: Update if directory structure changes
   - Frontend API calls: Update NEXT_PUBLIC_API_URL
   - Docker Compose: Update context paths

2. **Port Configuration**
   - Check monorepo for port conflicts
   - Document allocated ports
   - Update docker-compose.yml if needed

3. **Environment Variables**
   - Prefix with `BET_CHECK_` if needed for clarity
   - Add to monorepo's .env.example
   - Update docker-compose.yml env mappings

4. **Build Scripts**
   - Add to monorepo root package.json (if using npm workspaces)
   - Update CI/CD pipelines
   - Configure build order if dependencies exist

5. **Documentation**
   - Update README references
   - Create app-specific README in new location
   - Update links to point to monorepo structure

---

## 4. Step-by-Step Migration Process

### Phase 1: Preparation (30 minutes)

#### Step 1.1: Create Migration Workspace
```bash
# In a temporary directory
mkdir -p /tmp/bet-check-migration
cd /tmp/bet-check-migration

# Clone both repositories
git clone https://github.com/jmenichole/bet-check.git bet-check-source
git clone https://github.com/jmenichole/tiltcheck-monorepo.git tiltcheck-monorepo

# Create working branch in monorepo
cd tiltcheck-monorepo
git checkout -b feature/migrate-bet-check
```

#### Step 1.2: Analyze Monorepo Structure
```bash
# Determine where to place bet-check
# Look for existing apps
ls -la apps/ 2>/dev/null || ls -la services/ 2>/dev/null || ls -la packages/ 2>/dev/null

# Check package.json for workspace configuration
cat package.json | grep -A 10 "workspaces"

# Identify build system
ls turbo.json lerna.json nx.json 2>/dev/null
```

#### Step 1.3: Plan Directory Structure
Based on findings, decide on final structure. Example:
```
tiltcheck-monorepo/
└── apps/
    ├── bet-check-backend/
    └── bet-check-frontend/
```

### Phase 2: Backend Migration (45 minutes)

#### Step 2.1: Create Backend Directory
```bash
cd tiltcheck-monorepo

# Create directory (adjust path as needed)
mkdir -p apps/bet-check-backend
```

#### Step 2.2: Copy Backend Files
```bash
# Copy backend code
cp -r ../bet-check-source/bet-check/backend/* apps/bet-check-backend/

# Copy backend dependencies
cp ../bet-check-source/bet-check/requirements.txt apps/bet-check-backend/

# Copy backend Docker file
cp ../bet-check-source/bet-check/Dockerfile.backend apps/bet-check-backend/Dockerfile

# Copy scripts
mkdir -p apps/bet-check-backend/scripts
cp ../bet-check-source/bet-check/scripts/*.py apps/bet-check-backend/scripts/

# Copy database schemas
mkdir -p apps/bet-check-backend/db
cp ../bet-check-source/bet-check/*.sql apps/bet-check-backend/db/

# Copy test files
cp ../bet-check-source/bet-check/test_*.py apps/bet-check-backend/
```

#### Step 2.3: Create Backend README
```bash
cat > apps/bet-check-backend/README.md << 'EOF'
# Bet Check - Backend API

Sports prediction engine with FastAPI.

## Quick Start

### Local Development
```bash
cd apps/bet-check-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Docker
```bash
docker build -t bet-check-backend .
docker run -p 8000:8000 --env-file ../../.env bet-check-backend
```

## Environment Variables

See `../../.env.example` for required variables:
- SUPABASE_URL
- SUPABASE_KEY
- SPORTS_API_KEY (optional)

## API Documentation

Once running, visit: http://localhost:8000/docs

## Testing

```bash
python test_api.py
python test_chat.py
```

For full documentation, see: ../../docs/bet-check/
EOF
```

#### Step 2.4: Update Backend Imports (if needed)
```bash
# Check if any imports need updating
cd apps/bet-check-backend
grep -r "from backend\." . || echo "No backend imports found"

# If imports exist like "from backend.xyz", they may need updating
# Example: If main.py has "from backend.mines import X"
# It might need to become "from mines import X"
# This depends on how you run the backend
```

### Phase 3: Frontend Migration (45 minutes)

#### Step 3.1: Create Frontend Directory
```bash
cd ../../  # Back to monorepo root
mkdir -p apps/bet-check-frontend
```

#### Step 3.2: Copy Frontend Files
```bash
# Copy all frontend files
cp -r ../bet-check-source/bet-check/frontend/* apps/bet-check-frontend/

# Copy .eslintrc if exists
cp ../bet-check-source/bet-check/frontend/.eslintrc.js apps/bet-check-frontend/ 2>/dev/null || true
```

#### Step 3.3: Update Frontend Configuration

**Update package.json:**
```bash
cd apps/bet-check-frontend

# Update name field
cat package.json | sed 's/"name": "bet-check-frontend"/"name": "@tiltcheck\/bet-check-frontend"/' > package.json.tmp
mv package.json.tmp package.json
```

**Update next.config.js (if needed):**
```javascript
// Add or modify basePath if monorepo requires it
module.exports = {
  // basePath: '/bet-check',  // Uncomment if needed
  reactStrictMode: true,
  // ... rest of config
}
```

#### Step 3.4: Create Frontend README
```bash
cat > README.md << 'EOF'
# Bet Check - Frontend

Next.js frontend for sports prediction app.

## Quick Start

### Local Development
```bash
cd apps/bet-check-frontend
npm install
npm run dev
```

Access at: http://localhost:9000 (or 3000 depending on config)

### Docker
```bash
docker build -t bet-check-frontend .
docker run -p 9000:9000 bet-check-frontend
```

## Environment Variables

Set `NEXT_PUBLIC_API_URL` to backend URL:
- Local: `http://localhost:8000`
- Docker: `http://backend:8000`

## Building

```bash
npm run build
npm start
```

For full documentation, see: ../../docs/bet-check/
EOF
```

### Phase 4: Infrastructure Migration (30 minutes)

#### Step 4.1: Create Infrastructure Directory
```bash
cd ../../  # Back to monorepo root
mkdir -p infrastructure/docker/bet-check
```

#### Step 4.2: Create Monorepo Docker Compose
```bash
cat > infrastructure/docker/bet-check/docker-compose.yml << 'EOF'
version: '3.8'

services:
  # FastAPI Backend
  bet-check-backend:
    build:
      context: ../../../apps/bet-check-backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SPORTS_API_KEY=${SPORTS_API_KEY:-demo}
      - BACKEND_PORT=8000
    volumes:
      - ../../../apps/bet-check-backend:/app
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - bet-check-network

  # Next.js Frontend
  bet-check-frontend:
    build:
      context: ../../../apps/bet-check-frontend
      dockerfile: Dockerfile
    ports:
      - "9000:9000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - PORT=9000
    volumes:
      - ../../../apps/bet-check-frontend:/app
      - /app/node_modules
    command: npm run dev
    depends_on:
      - bet-check-backend
    networks:
      - bet-check-network

networks:
  bet-check-network:
    name: bet-check-network
EOF
```

#### Step 4.3: Update Environment Template
```bash
# Add bet-check variables to monorepo .env.example
cat >> .env.example << 'EOF'

# ========================================
# BET-CHECK CONFIGURATION
# ========================================

# Supabase Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here

# Sports API (optional - uses demo by default)
SPORTS_API_KEY=demo

# Backend API
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

### Phase 5: Documentation Migration (20 minutes)

#### Step 5.1: Create Documentation Directory
```bash
mkdir -p docs/bet-check
```

#### Step 5.2: Copy Essential Documentation
```bash
# Copy main README as reference
cp ../bet-check-source/bet-check/README.md docs/bet-check/

# Copy setup guides
cp ../bet-check-source/bet-check/QUICK_START_GUIDE.md docs/bet-check/ 2>/dev/null || true
cp ../bet-check-source/bet-check/DEPLOYMENT_GUIDE.md docs/bet-check/ 2>/dev/null || true
cp ../bet-check-source/bet-check/AI_GURU_SETUP.md docs/bet-check/ 2>/dev/null || true

# Copy other critical docs
cp ../bet-check-source/bet-check/LICENSE docs/bet-check/
cp ../bet-check-source/bet-check/COPYRIGHT_IMPLEMENTATION.md docs/bet-check/ 2>/dev/null || true
```

#### Step 5.3: Create Master Documentation Index
```bash
cat > docs/bet-check/INDEX.md << 'EOF'
# Bet Check Documentation

## Overview
Sports prediction application with AI-powered recommendations.

## Quick Links
- [Main README](./README.md) - Complete project documentation
- [Quick Start Guide](./QUICK_START_GUIDE.md) - Get running in 5 minutes
- [Deployment Guide](./DEPLOYMENT_GUIDE.md) - Production deployment
- [AI Guru Setup](./AI_GURU_SETUP.md) - Chat feature configuration

## Architecture
- **Backend:** `apps/bet-check-backend/` - FastAPI Python service
- **Frontend:** `apps/bet-check-frontend/` - Next.js React app
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Docker Compose

## Running Locally

```bash
# From monorepo root
cd infrastructure/docker/bet-check
cp ../../../.env.example ../../../.env
# Edit .env with your Supabase credentials
docker-compose up --build
```

Access:
- Frontend: http://localhost:9000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development Workflow

### Backend
```bash
cd apps/bet-check-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Frontend
```bash
cd apps/bet-check-frontend
npm install
npm run dev
```

## Testing
```bash
cd apps/bet-check-backend
python test_api.py
python test_chat.py
```

## Support
See main README for troubleshooting and support information.
EOF
```

### Phase 6: Monorepo Integration (30 minutes)

#### Step 6.1: Update Root Package.json (if using npm workspaces)
```bash
cd ..  # Back to monorepo root

# Check if workspaces exist
if grep -q "workspaces" package.json; then
  echo "Workspaces found, updating..."
  
  # Manually add to workspaces array in package.json
  # Example: Add "apps/bet-check-backend" and "apps/bet-check-frontend"
  
else
  echo "No workspaces configuration found"
  echo "Manual integration may be needed"
fi
```

#### Step 6.2: Add Build Scripts
```bash
# Add bet-check scripts to root package.json
# Example additions:

# "scripts": {
#   ...
#   "bet-check:backend": "cd apps/bet-check-backend && python -m uvicorn main:app --reload",
#   "bet-check:frontend": "cd apps/bet-check-frontend && npm run dev",
#   "bet-check:docker": "cd infrastructure/docker/bet-check && docker-compose up",
#   "bet-check:test": "cd apps/bet-check-backend && python test_api.py && python test_chat.py"
# }
```

#### Step 6.3: Update Main README
```bash
# Add bet-check section to monorepo README
cat >> README.md << 'EOF'

## Bet Check

Sports prediction application with adaptive ML and AI chat.

**Location:** `apps/bet-check-backend/`, `apps/bet-check-frontend/`

**Quick Start:**
```bash
cd infrastructure/docker/bet-check
docker-compose up
```

**Documentation:** See `docs/bet-check/`

EOF
```

### Phase 7: Verification & Testing (30 minutes)

#### Step 7.1: Commit Migration Changes
```bash
# Review changes
git status
git diff

# Stage files
git add apps/bet-check-backend/
git add apps/bet-check-frontend/
git add infrastructure/docker/bet-check/
git add docs/bet-check/
git add .env.example
git add README.md

# Commit
git commit -m "feat: migrate bet-check project into monorepo

- Added bet-check-backend to apps/
- Added bet-check-frontend to apps/
- Created Docker Compose configuration
- Added documentation
- Updated environment template

Closes #[issue-number]
"
```

#### Step 7.2: Test Backend
```bash
# Test without Docker
cd apps/bet-check-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy env from root
cp ../../.env .env 2>/dev/null || echo "Create .env with required variables"

# Run backend
python -m uvicorn main:app --reload --port 8000
```

In another terminal:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API docs
open http://localhost:8000/docs  # or xdg-open on Linux
```

#### Step 7.3: Test Frontend
```bash
# Stop backend (Ctrl+C), then test frontend
cd ../../apps/bet-check-frontend
npm install

# Set API URL
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Run frontend
npm run dev
```

Open browser: http://localhost:9000

#### Step 7.4: Test Docker Compose
```bash
# Stop all local services, then test Docker
cd ../../infrastructure/docker/bet-check

# Ensure .env exists in monorepo root
ls -la ../../../.env

# Build and run
docker-compose up --build

# Verify services
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Test endpoints
curl http://localhost:8000/health
open http://localhost:9000
```

#### Step 7.5: Run Tests
```bash
# Keep Docker running, open new terminal
cd apps/bet-check-backend
source venv/bin/activate

# Run API tests
python test_api.py
python test_chat.py

# Check for errors
echo "Exit code: $?"
```

### Phase 8: Cleanup & Documentation (20 minutes)

#### Step 8.1: Create Migration Documentation
```bash
cat > docs/bet-check/MIGRATION_NOTES.md << 'EOF'
# Migration Notes

**Date:** $(date +%Y-%m-%d)
**From:** github.com/jmenichole/bet-check
**To:** github.com/jmenichole/tiltcheck-monorepo

## Changes Made

### Directory Structure
- Backend: `bet-check/backend/` → `apps/bet-check-backend/`
- Frontend: `bet-check/frontend/` → `apps/bet-check-frontend/`
- Docker: Root `docker-compose.yml` → `infrastructure/docker/bet-check/docker-compose.yml`
- Docs: Root `*.md` → `docs/bet-check/`

### Configuration Changes
- Frontend port: 3000 → 9000 (to avoid conflicts)
- Backend port: 8000 (unchanged)
- Environment variables: Added to monorepo `.env.example`

### Build Scripts
- Added to root `package.json` (if applicable)
- Docker Compose paths updated for monorepo structure

## Known Issues
- None identified during migration

## Testing Results
- [x] Backend starts successfully
- [x] Frontend starts successfully
- [x] Docker Compose builds and runs
- [x] API endpoints respond correctly
- [x] Frontend connects to backend
- [x] Database operations work
- [x] Tests pass

## Rollback Instructions
See MIGRATION_PLAN.md Section 6: Rollback Plan

## Next Steps
1. Update CI/CD pipelines
2. Update deployment configurations
3. Archive old repository
EOF
```

#### Step 8.2: Push to Monorepo
```bash
cd ../..  # Back to monorepo root

# Final review
git status
git log --oneline -5

# Push to remote
git push origin feature/migrate-bet-check

# Create pull request on GitHub
# Title: "Migrate bet-check project into monorepo"
# Description: See MIGRATION_NOTES.md for details
```

#### Step 8.3: Update Original Repository
```bash
# Go to original bet-check repo
cd ../bet-check-source

# Create deprecation notice
cat > MIGRATION_NOTICE.md << 'EOF'
# ⚠️ Repository Migrated

This repository has been migrated to the **tiltcheck-monorepo**.

**New Location:** https://github.com/jmenichole/tiltcheck-monorepo

- Backend: `apps/bet-check-backend/`
- Frontend: `apps/bet-check-frontend/`

**This repository is now archived and read-only.**

For new issues, PRs, and development, please use the monorepo.

---
Migrated on: $(date +%Y-%m-%d)
EOF

# Add notice to README
echo "" >> README.md
echo "---" >> README.md
cat MIGRATION_NOTICE.md >> README.md

# Commit and push
git add MIGRATION_NOTICE.md README.md
git commit -m "docs: add migration notice - project moved to monorepo"
git push origin main

# Archive repository on GitHub (manual step in Settings)
```

---

## 5. Post-Migration Verification

### 5.1 Functional Testing Checklist

#### Backend API
- [ ] Health check: `GET /health`
- [ ] List games: `GET /games?sport=nba`
- [ ] Get prediction: `GET /predict/{game_id}`
- [ ] Log result: `POST /log_result`
- [ ] Get analytics: `GET /analytics`
- [ ] Chat endpoint: `POST /chat`
- [ ] API documentation: `/docs`

#### Frontend Pages
- [ ] Home page: `/` - Shows upcoming games
- [ ] Game detail: `/game/[id]` - Shows prediction
- [ ] Dashboard: `/dashboard` - Shows analytics
- [ ] AI Guru: `/guru` - Chat interface
- [ ] Mines game: `/mines` - Game works
- [ ] Past games: `/past-games` - History loads

#### Docker Compose
- [ ] Both services start: `docker-compose up`
- [ ] Backend accessible: http://localhost:8000
- [ ] Frontend accessible: http://localhost:9000
- [ ] Inter-service communication works
- [ ] Environment variables load correctly
- [ ] Volumes mount properly (hot reload works)

#### Database
- [ ] Backend connects to Supabase
- [ ] Tables exist and accessible
- [ ] CRUD operations work
- [ ] Factor weights update
- [ ] Chat history persists

### 5.2 Integration Testing

```bash
# Full integration test script
cat > apps/bet-check-backend/test_migration.py << 'EOF'
#!/usr/bin/env python3
"""Test migration - verify all endpoints work"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("✓ Health check passed")

def test_games():
    r = requests.get(f"{BASE_URL}/games")
    assert r.status_code == 200
    print(f"✓ Games endpoint passed ({len(r.json())} games)")

def test_factors():
    r = requests.get(f"{BASE_URL}/factors")
    assert r.status_code == 200
    print(f"✓ Factors endpoint passed ({len(r.json())} factors)")

def test_analytics():
    r = requests.get(f"{BASE_URL}/analytics")
    assert r.status_code == 200
    print("✓ Analytics endpoint passed")

if __name__ == "__main__":
    try:
        test_health()
        test_games()
        test_factors()
        test_analytics()
        print("\n✅ All migration tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Migration test failed: {e}")
        sys.exit(1)
EOF

chmod +x apps/bet-check-backend/test_migration.py
python apps/bet-check-backend/test_migration.py
```

### 5.3 Performance Verification

```bash
# Check startup times
time docker-compose up -d

# Check response times
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/health
curl -w "\nTime: %{time_total}s\n" http://localhost:8000/games

# Check resource usage
docker stats bet-check-backend bet-check-frontend --no-stream
```

### 5.4 Documentation Review

- [ ] All links in READMEs work
- [ ] Environment variable examples are correct
- [ ] Installation instructions are accurate
- [ ] API documentation is accessible
- [ ] Docker commands work as documented

---

## 6. Rollback Plan

### 6.1 If Issues Found During Migration

**Before committing to monorepo:**
```bash
# Simply discard changes
cd tiltcheck-monorepo
git checkout main
git branch -D feature/migrate-bet-check

# Original bet-check repo is untouched and still works
```

### 6.2 If Issues Found After Merging

**Revert the merge:**
```bash
cd tiltcheck-monorepo

# Find the merge commit
git log --oneline --graph -10

# Revert the merge (replace COMMIT_HASH)
git revert -m 1 COMMIT_HASH

# Push revert
git push origin main
```

### 6.3 If Issues Found in Production

**Emergency rollback:**
```bash
# 1. Point production to old bet-check repo temporarily
# 2. Revert merge in monorepo
# 3. Fix issues in development
# 4. Re-migrate when ready
```

**Timeline:**
- Detection: 5 minutes
- Rollback execution: 5 minutes
- Verification: 5 minutes
- **Total: <15 minutes**

### 6.4 Data Rollback

**If database issues:**
- Supabase database is separate - no migration needed
- No data rollback required
- Configuration changes only

**If database schema changed:**
```sql
-- Restore from backup
-- Run this in Supabase SQL editor
-- (Schema shouldn't change during migration)
```

---

## 7. Common Issues & Solutions

### 7.1 Import Errors

**Problem:** Backend imports fail after migration
```
ModuleNotFoundError: No module named 'backend'
```

**Solution:**
```bash
# Check Python path
cd apps/bet-check-backend
python -c "import sys; print(sys.path)"

# Update imports in code
# Change: from backend.mines import X
# To: from mines import X

# Or add parent directory to path in main.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

### 7.2 Frontend API Connection Failed

**Problem:** Frontend can't reach backend
```
AxiosError: Network Error
```

**Solution:**
```bash
# Check NEXT_PUBLIC_API_URL
echo $NEXT_PUBLIC_API_URL

# Update .env
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" >> .env

# Restart frontend
npm run dev
```

### 7.3 Docker Build Failures

**Problem:** Docker Compose fails to build
```
ERROR: failed to solve: failed to compute cache key
```

**Solution:**
```bash
# Check context paths in docker-compose.yml
# Ensure paths are relative to docker-compose.yml location

# Clear Docker cache
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up
```

### 7.4 Port Conflicts

**Problem:** Port already in use
```
Error: bind: address already in use
```

**Solution:**
```bash
# Find process using port
lsof -i :8000
lsof -i :9000

# Kill process
kill -9 PID

# Or change ports in docker-compose.yml and .env
```

### 7.5 Environment Variables Not Loading

**Problem:** Application starts but can't connect to Supabase
```
Error: SUPABASE_URL not set
```

**Solution:**
```bash
# Check .env file exists in correct location
ls -la .env

# Check docker-compose.yml env_file or environment sections
# Ensure path to .env is correct

# For Docker, rebuild:
docker-compose down
docker-compose up --build

# For local dev:
source .env  # or export manually
```

### 7.6 Database Connection Fails

**Problem:** Can't connect to Supabase
```
Error: Connection refused
```

**Solution:**
```bash
# Verify Supabase credentials
curl -I $SUPABASE_URL

# Check if URL is correct format
# Should be: https://PROJECT_ID.supabase.co

# Verify key is anon key (not service role)
# Check in Supabase dashboard: Settings → API

# Test connection
python -c "
from supabase import create_client
import os
client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
print('Connected!')
"
```

### 7.7 npm Install Fails in Frontend

**Problem:** Dependencies won't install
```
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solution:**
```bash
cd apps/bet-check-frontend

# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force

# Install with legacy peer deps
npm install --legacy-peer-deps

# Or update to compatible versions
npm update
```

### 7.8 Hot Reload Not Working

**Problem:** Code changes don't reflect immediately

**Solution:**
```bash
# For backend - ensure volumes are mounted in docker-compose.yml
volumes:
  - ../../../apps/bet-check-backend:/app

# For frontend - ensure node_modules isn't overwritten
volumes:
  - ../../../apps/bet-check-frontend:/app
  - /app/node_modules  # This line is crucial

# Restart with fresh build
docker-compose down
docker-compose up --build
```

---

## 8. Success Criteria

Migration is considered successful when:

- [x] All files copied to monorepo
- [x] Backend starts without errors
- [x] Frontend starts without errors
- [x] Docker Compose builds and runs both services
- [x] All API endpoints respond correctly
- [x] Frontend can fetch data from backend
- [x] Database operations work
- [x] Existing tests pass
- [x] Documentation is updated
- [x] Original repository is archived with notice

---

## 9. Timeline Estimate

| Phase | Duration | Tasks |
|-------|----------|-------|
| Preparation | 30 min | Backups, analysis, branch creation |
| Backend Migration | 45 min | Copy files, update configs, test |
| Frontend Migration | 45 min | Copy files, update configs, test |
| Infrastructure | 30 min | Docker Compose, env variables |
| Documentation | 20 min | Copy docs, create guides |
| Integration | 30 min | Monorepo scripts, root config |
| Verification | 30 min | Full testing cycle |
| Cleanup | 20 min | Final docs, push, archive |
| **Total** | **4 hours** | Complete migration |

**Minimum Time** (experienced): 2 hours  
**Maximum Time** (first time): 6 hours  
**Recommended** (with buffer): 4 hours

---

## 10. Contact & Support

**Migration Lead:** Jamie Vargas  
**Email:** jme@tiltcheck.me  
**GitHub:** [@jmenichole](https://github.com/jmenichole)

**Resources:**
- Original Repo: https://github.com/jmenichole/bet-check
- Monorepo: https://github.com/jmenichole/tiltcheck-monorepo
- Portfolio: https://jmenichole.github.io/Portfolio/

**For Issues:**
1. Check "Common Issues & Solutions" section above
2. Review bet-check README troubleshooting
3. Check Docker logs: `docker-compose logs`
4. Open issue in monorepo with "bet-check" label

---

## Appendix A: Environment Variables Reference

### Required Variables

```env
# Supabase (Required)
SUPABASE_URL=https://PROJECT_ID.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Backend (Required)
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Frontend (Required)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Optional Variables

```env
# Sports API (Optional - uses demo mode if not set)
SPORTS_API_KEY=your_rapidapi_key

# Development (Optional)
NODE_ENV=development
PYTHON_ENV=development
```

---

## Appendix B: File Checklist

### Backend Files to Migrate
- [x] `backend/main.py` - Core API
- [x] `backend/db.py` - Database utilities
- [x] `backend/mines.py` - Mines game
- [x] `backend/mines_engine.py` - Mines engine
- [x] `backend/limbo_crash_engine.py` - Crash game
- [x] `backend/result_fetcher.py` - ESPN fetcher
- [x] `requirements.txt` - Python deps
- [x] `Dockerfile.backend` - Container config
- [x] `scripts/seed_factors.py` - DB seeding
- [x] `scripts/update_games.py` - Game updates
- [x] `scripts/verify_db.py` - DB verification
- [x] `test_api.py` - API tests
- [x] `test_chat.py` - Chat tests
- [x] `schema.sql` - DB schema
- [x] `schema_chat.sql` - Chat schema
- [x] `schema_mines_crash.sql` - Games schema
- [x] `disable_rls.sql` - Security config

### Frontend Files to Migrate
- [x] `frontend/components/` - All React components
- [x] `frontend/pages/` - All Next.js pages
- [x] `frontend/styles/` - CSS files
- [x] `frontend/package.json` - Dependencies
- [x] `frontend/tsconfig.json` - TypeScript config
- [x] `frontend/tailwind.config.ts` - Tailwind config
- [x] `frontend/next.config.js` - Next.js config
- [x] `frontend/postcss.config.js` - PostCSS config
- [x] `frontend/.eslintrc.js` - Linting config
- [x] `frontend/Dockerfile` - Container config

### Infrastructure Files
- [x] `docker-compose.yml` - Container orchestration
- [x] `Procfile` - Heroku/Railway config
- [x] `render.yaml` - Render.com config
- [x] `.env.example` - Environment template
- [x] `.gitignore` - Git ignore rules

### Documentation Files
- [x] `README.md` - Main documentation
- [x] `LICENSE` - License file
- [x] `COPYRIGHT_IMPLEMENTATION.md` - Copyright info
- [x] `QUICK_START_GUIDE.md` - Quick start
- [x] `DEPLOYMENT_GUIDE.md` - Deployment
- [x] `AI_GURU_SETUP.md` - AI chat setup

---

## Appendix C: Git Subtree Method (Advanced)

For preserving git history (advanced users):

```bash
# In tiltcheck-monorepo
git remote add bet-check https://github.com/jmenichole/bet-check.git
git fetch bet-check

# Add as subtree
git subtree add --prefix=apps/bet-check bet-check main --squash

# Or use git filter-repo for more control
git filter-repo --path bet-check/ --path-rename bet-check/:apps/bet-check/
```

**Note:** This method is complex and can cause merge conflicts. Only use if git history preservation is critical.

---

## Document Changelog

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-18 | Initial migration plan created | Jamie Vargas |

---

**End of Migration Plan**

For questions or issues, contact: jme@tiltcheck.me
