# GitHub Copilot Migration Prompt

**Use this prompt in the tiltcheck-monorepo repository to execute the bet-check migration**

---

## Instructions

1. Open the **tiltcheck-monorepo** repository in your IDE
2. Start a GitHub Copilot chat session
3. Copy and paste the prompt below
4. Follow Copilot's execution steps

---

## Copilot Prompt

```
I need you to migrate the bet-check project from the standalone repository 
(https://github.com/jmenichole/bet-check) into this tiltcheck-monorepo.

TASK: Safely migrate bet-check into the monorepo structure without breaking anything.

PROJECT OVERVIEW:
- bet-check is a sports prediction application
- Backend: Python FastAPI (port 8000)
- Frontend: Next.js/React (port 9000)
- Database: Supabase (external, no migration needed)
- Current location: https://github.com/jmenichole/bet-check

MIGRATION REQUIREMENTS:

1. TARGET STRUCTURE:
   Create this structure in the monorepo:
   ```
   tiltcheck-monorepo/
   ├── apps/
   │   ├── bet-check-backend/      # Copy from bet-check/backend/
   │   └── bet-check-frontend/     # Copy from bet-check/frontend/
   ├── infrastructure/
   │   └── docker/
   │       └── bet-check/          # Docker Compose
   └── docs/
       └── bet-check/              # Documentation
   ```

2. FILES TO MIGRATE:

   Backend (bet-check/backend/ → apps/bet-check-backend/):
   - All .py files (main.py, db.py, mines.py, mines_engine.py, limbo_crash_engine.py, result_fetcher.py)
   - requirements.txt (from root)
   - Dockerfile.backend → Dockerfile
   - scripts/ directory (seed_factors.py, update_games.py, verify_db.py)
   - *.sql files (schema.sql, schema_chat.sql, schema_mines_crash.sql, disable_rls.sql)
   - test_*.py files

   Frontend (bet-check/frontend/ → apps/bet-check-frontend/):
   - All directories: components/, pages/, styles/
   - All config files: package.json, tsconfig.json, tailwind.config.ts, next.config.js, postcss.config.js, .eslintrc.js
   - Dockerfile

   Infrastructure:
   - docker-compose.yml → infrastructure/docker/bet-check/docker-compose.yml
     (Update context paths to: ../../../apps/bet-check-backend/ and ../../../apps/bet-check-frontend/)

   Documentation:
   - README.md → docs/bet-check/README.md
   - LICENSE → docs/bet-check/LICENSE
   - QUICK_START_GUIDE.md, DEPLOYMENT_GUIDE.md, AI_GURU_SETUP.md (if they exist)

3. CONFIGURATION UPDATES:

   a) Frontend package.json:
      - Update name to "@tiltcheck/bet-check-frontend"
   
   b) Docker Compose (infrastructure/docker/bet-check/docker-compose.yml):
      - Update build contexts:
        * backend: context: ../../../apps/bet-check-backend
        * frontend: context: ../../../apps/bet-check-frontend
      - Update volume paths similarly
      - Frontend port: 9000 (to avoid conflicts)
   
   c) Environment variables (.env.example):
      - Add bet-check variables:
        ```
        # BET-CHECK CONFIGURATION
        SUPABASE_URL=https://your-project.supabase.co
        SUPABASE_KEY=your-anon-key
        SPORTS_API_KEY=demo
        BACKEND_PORT=8000
        NEXT_PUBLIC_API_URL=http://localhost:8000
        ```

4. CREATE NEW FILES:

   a) apps/bet-check-backend/README.md:
      ```markdown
      # Bet Check - Backend API
      
      Sports prediction engine with FastAPI.
      
      ## Quick Start
      ```bash
      cd apps/bet-check-backend
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      python -m uvicorn main:app --reload --port 8000
      ```
      
      ## Docker
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
      http://localhost:8000/docs
      
      ## Testing
      ```bash
      python test_api.py
      python test_chat.py
      ```
      ```

   b) apps/bet-check-frontend/README.md:
      ```markdown
      # Bet Check - Frontend
      
      Next.js frontend for sports prediction app.
      
      ## Quick Start
      ```bash
      cd apps/bet-check-frontend
      npm install
      npm run dev
      ```
      
      Access at: http://localhost:9000
      
      ## Docker
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
      ```

   c) docs/bet-check/INDEX.md:
      ```markdown
      # Bet Check Documentation
      
      ## Overview
      Sports prediction application with AI-powered recommendations.
      
      ## Quick Links
      - [Main README](./README.md)
      - [Quick Start Guide](./QUICK_START_GUIDE.md)
      - [Deployment Guide](./DEPLOYMENT_GUIDE.md)
      
      ## Architecture
      - **Backend:** `apps/bet-check-backend/` - FastAPI Python service
      - **Frontend:** `apps/bet-check-frontend/` - Next.js React app
      - **Database:** Supabase (PostgreSQL)
      
      ## Running Locally
      ```bash
      cd infrastructure/docker/bet-check
      cp ../../../.env.example ../../../.env
      # Edit .env with your Supabase credentials
      docker-compose up --build
      ```
      
      Access:
      - Frontend: http://localhost:9000
      - Backend: http://localhost:8000
      - API Docs: http://localhost:8000/docs
      ```

5. VALIDATION STEPS:

   After migration, verify:
   
   a) Backend starts:
      ```bash
      cd apps/bet-check-backend
      python -m venv venv && source venv/bin/activate
      pip install -r requirements.txt
      python -m uvicorn main:app --reload
      # Should start on port 8000
      # Test: curl http://localhost:8000/health
      ```
   
   b) Frontend starts:
      ```bash
      cd apps/bet-check-frontend
      npm install
      NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
      # Should start on port 9000
      # Test: curl http://localhost:9000
      ```
   
   c) Docker Compose:
      ```bash
      cd infrastructure/docker/bet-check
      docker-compose up --build
      # Both services should start
      # Backend: http://localhost:8000
      # Frontend: http://localhost:9000
      ```

6. IMPORTANT NOTES:

   - DO NOT modify any business logic in the code
   - DO NOT change API endpoints or contracts
   - Database connection stays the same (external Supabase)
   - Original bet-check repo is NOT modified
   - If import errors occur (e.g., "from backend.xyz"), update imports:
     * Change: from backend.mines import X
     * To: from mines import X
   
7. FINAL CHECKLIST:

   After migration is complete:
   - [ ] Backend directory structure correct
   - [ ] Frontend directory structure correct
   - [ ] Docker Compose paths updated
   - [ ] Environment variables in .env.example
   - [ ] Backend starts without errors
   - [ ] Frontend starts without errors
   - [ ] Docker Compose works
   - [ ] API health check responds: curl http://localhost:8000/health
   - [ ] Frontend loads: curl http://localhost:9000
   - [ ] All original files copied (none missing)

EXECUTION APPROACH:
1. Clone the bet-check repository to a temporary location
2. Create the directory structure in tiltcheck-monorepo
3. Copy files to the appropriate locations
4. Update configurations (paths, package.json, docker-compose.yml)
5. Create new README files
6. Test each service individually
7. Test Docker Compose
8. Commit all changes with message: "feat: migrate bet-check into monorepo"

REFERENCE DOCUMENTATION:
The bet-check repository contains comprehensive migration documentation:
- MIGRATION_PLAN.md - Complete 60-page guide
- MIGRATION_QUICK_START.md - 30-minute fast track
- MIGRATION_CHECKLIST.md - Task checklist

Please proceed with the migration step by step, validating each phase before moving to the next.
```

---

## Alternative: Detailed Step-by-Step Prompt

If you prefer more control, use this expanded prompt:

```
PHASE 1: SETUP

Step 1: Clone the source repository
```bash
# In a temporary location outside the monorepo
cd /tmp
git clone https://github.com/jmenichole/bet-check.git bet-check-source
```

Step 2: Create directory structure in monorepo
```bash
mkdir -p apps/bet-check-backend
mkdir -p apps/bet-check-frontend
mkdir -p infrastructure/docker/bet-check
mkdir -p docs/bet-check
```

PHASE 2: BACKEND MIGRATION

Step 3: Copy backend files
```bash
# From bet-check-source to monorepo
cp -r /tmp/bet-check-source/bet-check/backend/* apps/bet-check-backend/
cp /tmp/bet-check-source/bet-check/requirements.txt apps/bet-check-backend/
cp /tmp/bet-check-source/bet-check/Dockerfile.backend apps/bet-check-backend/Dockerfile
cp -r /tmp/bet-check-source/bet-check/scripts apps/bet-check-backend/
cp /tmp/bet-check-source/bet-check/*.sql apps/bet-check-backend/
cp /tmp/bet-check-source/bet-check/test_*.py apps/bet-check-backend/
```

Step 4: Create backend README
Create `apps/bet-check-backend/README.md` with quick start instructions.

Step 5: Test backend locally
```bash
cd apps/bet-check-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
# Verify: curl http://localhost:8000/health
```

PHASE 3: FRONTEND MIGRATION

Step 6: Copy frontend files
```bash
cp -r /tmp/bet-check-source/bet-check/frontend/* apps/bet-check-frontend/
```

Step 7: Update frontend package.json
Edit `apps/bet-check-frontend/package.json`:
- Change "name" from "bet-check-frontend" to "@tiltcheck/bet-check-frontend"

Step 8: Create frontend README
Create `apps/bet-check-frontend/README.md` with quick start instructions.

Step 9: Test frontend locally
```bash
cd apps/bet-check-frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
# Verify: curl http://localhost:9000
```

PHASE 4: INFRASTRUCTURE

Step 10: Create Docker Compose
Create `infrastructure/docker/bet-check/docker-compose.yml`:
```yaml
services:
  backend:
    build:
      context: ../../../apps/bet-check-backend
    ports: ["8000:8000"]
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - SPORTS_API_KEY=${SPORTS_API_KEY:-demo}
    volumes: ["../../../apps/bet-check-backend:/app"]
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ../../../apps/bet-check-frontend
    ports: ["9000:9000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - PORT=9000
    volumes:
      - ../../../apps/bet-check-frontend:/app
      - /app/node_modules
    command: npm run dev
    depends_on: [backend]
```

Step 11: Update environment template
Add to `.env.example`:
```env
# BET-CHECK CONFIGURATION
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SPORTS_API_KEY=demo
BACKEND_PORT=8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Step 12: Test Docker Compose
```bash
cd infrastructure/docker/bet-check
docker-compose up --build
# Verify both services start
```

PHASE 5: DOCUMENTATION

Step 13: Copy documentation
```bash
cp /tmp/bet-check-source/bet-check/README.md docs/bet-check/
cp /tmp/bet-check-source/bet-check/LICENSE docs/bet-check/
cp /tmp/bet-check-source/bet-check/QUICK_START_GUIDE.md docs/bet-check/ 2>/dev/null || true
```

Step 14: Create docs index
Create `docs/bet-check/INDEX.md` with overview and links.

PHASE 6: FINALIZATION

Step 15: Commit everything
```bash
git add apps/bet-check-backend/
git add apps/bet-check-frontend/
git add infrastructure/docker/bet-check/
git add docs/bet-check/
git add .env.example
git commit -m "feat: migrate bet-check into monorepo"
```

Step 16: Final verification
Run all validation steps from section 5 above.

Please execute these phases in order, validating each step before proceeding.
```

---

## Quick Reference Commands

After migration is complete, use these commands:

```bash
# Start backend locally
cd apps/bet-check-backend && python -m uvicorn main:app --reload

# Start frontend locally  
cd apps/bet-check-frontend && npm run dev

# Start with Docker
cd infrastructure/docker/bet-check && docker-compose up

# Run tests
cd apps/bet-check-backend && python test_api.py

# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError: No module named 'backend'`:
```python
# In apps/bet-check-backend/main.py
# Change: from backend.mines import X
# To: from mines import X
```

### Frontend Can't Connect
```bash
# Ensure NEXT_PUBLIC_API_URL is set
export NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

### Port Conflicts
```bash
# Check what's using the port
lsof -i :8000
lsof -i :9000

# Kill the process
kill -9 <PID>
```

### Docker Build Fails
```bash
# Clear cache and rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up
```

---

## Success Criteria

Migration is complete when:
- ✅ Backend starts on port 8000
- ✅ Frontend starts on port 9000
- ✅ Docker Compose builds successfully
- ✅ API health check returns 200
- ✅ Frontend loads in browser
- ✅ No console errors
- ✅ All tests pass

---

## Notes

- This migrates code only - database stays on Supabase (no changes)
- Original bet-check repository is not modified
- All changes are in the tiltcheck-monorepo
- Migration is fully reversible
- Estimated time: 30-60 minutes with this prompt

---

## Support

For detailed guidance, see the migration documentation in the bet-check repository:
- https://github.com/jmenichole/bet-check/blob/main/bet-check/MIGRATION_PLAN.md
- https://github.com/jmenichole/bet-check/blob/main/bet-check/MIGRATION_QUICK_START.md

---

**Ready to use!** Copy the main prompt and paste it into GitHub Copilot in the tiltcheck-monorepo repository.
