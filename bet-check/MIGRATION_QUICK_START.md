# Quick Start: Migrate bet-check in 30 Minutes

**TL;DR:** Fast-track migration guide for experienced developers.

For detailed explanations, see `MIGRATION_PLAN.md`  
For step-by-step checklist, see `MIGRATION_CHECKLIST.md`

---

## Prerequisites

- [x] tiltcheck-monorepo cloned locally
- [x] bet-check repo accessible
- [x] Docker Desktop running
- [x] Supabase credentials ready

---

## 30-Minute Migration

### 1. Setup (5 minutes)

```bash
# Clone and prepare
git clone https://github.com/jmenichole/tiltcheck-monorepo.git
cd tiltcheck-monorepo
git checkout -b feature/migrate-bet-check

# Determine structure (adjust paths below if different)
# Assuming: apps/bet-check-backend/ and apps/bet-check-frontend/
```

### 2. Backend Migration (8 minutes)

```bash
# Copy backend
mkdir -p apps/bet-check-backend
cd /path/to/bet-check/bet-check
cp -r backend/* ../tiltcheck-monorepo/apps/bet-check-backend/
cp requirements.txt ../tiltcheck-monorepo/apps/bet-check-backend/
cp Dockerfile.backend ../tiltcheck-monorepo/apps/bet-check-backend/Dockerfile
cp -r scripts ../tiltcheck-monorepo/apps/bet-check-backend/
cp *.sql ../tiltcheck-monorepo/apps/bet-check-backend/
cp test_*.py ../tiltcheck-monorepo/apps/bet-check-backend/

# Quick test
cd ../tiltcheck-monorepo/apps/bet-check-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload &
sleep 5
curl http://localhost:8000/health  # Should return {"status": "ok"}
kill %1
```

### 3. Frontend Migration (7 minutes)

```bash
# Copy frontend
cd ../../
mkdir -p apps/bet-check-frontend
cd /path/to/bet-check/bet-check
cp -r frontend/* ../tiltcheck-monorepo/apps/bet-check-frontend/

# Update name in package.json
cd ../tiltcheck-monorepo/apps/bet-check-frontend
sed -i 's/"name": "bet-check-frontend"/"name": "@tiltcheck\/bet-check-frontend"/' package.json

# Quick test
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev &
sleep 10
curl http://localhost:9000  # Should return HTML
kill %1
```

### 4. Infrastructure (5 minutes)

```bash
# Docker Compose
cd ../../
mkdir -p infrastructure/docker/bet-check

cat > infrastructure/docker/bet-check/docker-compose.yml << 'EOF'
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
EOF

# Environment variables
cat >> .env.example << 'EOF'

# BET-CHECK
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SPORTS_API_KEY=demo
EOF

# Copy your actual .env
cp /path/to/bet-check/bet-check/.env .env
```

### 5. Documentation (3 minutes)

```bash
# Minimal docs
mkdir -p docs/bet-check
cp /path/to/bet-check/bet-check/README.md docs/bet-check/
cp /path/to/bet-check/bet-check/LICENSE docs/bet-check/

cat > docs/bet-check/INDEX.md << 'EOF'
# Bet Check

Location: `apps/bet-check-backend/`, `apps/bet-check-frontend/`

## Quick Start
```bash
cd infrastructure/docker/bet-check
docker-compose up
```

- Frontend: http://localhost:9000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

See README.md for full documentation.
EOF
```

### 6. Test Everything (2 minutes)

```bash
# Docker test
cd infrastructure/docker/bet-check
docker-compose up --build -d
sleep 20

# Verify
curl http://localhost:8000/health
curl http://localhost:9000
open http://localhost:9000  # Visual check

# Cleanup
docker-compose down
```

### 7. Commit & Push (< 1 minute)

```bash
cd ../../..
git add apps/ infrastructure/ docs/ .env.example
git commit -m "feat: migrate bet-check into monorepo

- Backend: apps/bet-check-backend/
- Frontend: apps/bet-check-frontend/
- Docker: infrastructure/docker/bet-check/
- Docs: docs/bet-check/
"
git push origin feature/migrate-bet-check
```

---

## Verification Commands

Run these to verify migration:

```bash
# Backend health
curl http://localhost:8000/health
curl http://localhost:8000/games

# Frontend
curl -I http://localhost:9000

# Docker status
docker-compose ps

# Logs
docker-compose logs --tail=50 backend
docker-compose logs --tail=50 frontend
```

---

## Common Issues

### Import errors in backend
```bash
# If seeing "ModuleNotFoundError: No module named 'backend'"
# In apps/bet-check-backend/main.py, change:
# from backend.mines import X
# to:
# from mines import X
```

### Frontend can't connect
```bash
# Check NEXT_PUBLIC_API_URL
echo $NEXT_PUBLIC_API_URL
# Should be: http://localhost:8000

# Update and restart
export NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

### Docker build fails
```bash
# Clear cache
docker-compose down
docker system prune -f
docker-compose build --no-cache
```

### Port conflicts
```bash
# Change ports in docker-compose.yml:
# backend: ["8001:8000"]
# frontend: ["9001:9000"]
```

---

## Next Steps

1. Create Pull Request on GitHub
2. Get code review
3. Merge to main
4. Update CI/CD (if needed)
5. Archive old bet-check repo

---

## Full Documentation

- **Complete Plan:** `MIGRATION_PLAN.md` (comprehensive guide)
- **Checklist:** `MIGRATION_CHECKLIST.md` (print-friendly)
- **This Guide:** `MIGRATION_QUICK_START.md` (fast track)

---

## Rollback

If something goes wrong:

```bash
# Before merge: just delete the branch
git checkout main
git branch -D feature/migrate-bet-check

# After merge: revert the merge commit
git revert -m 1 <merge-commit-hash>
git push origin main
```

Original bet-check repo stays untouched - you can always return to it.

---

## Summary

**Total Time:** ~30 minutes  
**Difficulty:** Easy  
**Risk:** Low (original repo unchanged)

**What we moved:**
- ✅ Backend (Python/FastAPI)
- ✅ Frontend (Next.js/React)
- ✅ Docker Compose
- ✅ Documentation
- ✅ Environment config

**What stayed the same:**
- ✅ Database (Supabase - no changes needed)
- ✅ API structure (no breaking changes)
- ✅ Frontend UI (identical)
- ✅ Features (all preserved)

---

**Ready? Let's migrate! 🚀**

Start with step 1 above, or see `MIGRATION_PLAN.md` for detailed guidance.
