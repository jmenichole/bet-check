# Visual Migration Guide

**Interactive visual reference for the bet-check → tiltcheck-monorepo migration**

---

## Migration Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    MIGRATION PROCESS                             │
│                                                                  │
│  START → Prep → Backend → Frontend → Infra → Docs → Test → END │
│   (5m)   (45m)    (45m)     (30m)    (20m)   (30m)    (✓)      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Current Structure (bet-check repo)

```
github.com/jmenichole/bet-check
│
├── bet-check/
│   │
│   ├── backend/                    ← Python FastAPI
│   │   ├── main.py                 ← Core API
│   │   ├── db.py
│   │   ├── mines.py
│   │   └── ...
│   │
│   ├── frontend/                   ← Next.js React
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── package.json
│   │
│   ├── scripts/                    ← Utility scripts
│   │   ├── seed_factors.py
│   │   └── update_games.py
│   │
│   ├── docker-compose.yml          ← Container orchestration
│   ├── requirements.txt            ← Python deps
│   ├── *.sql                       ← Database schemas
│   └── README.md                   ← Documentation
│
└── README.md                       ← Repo root
```

---

## Target Structure (tiltcheck-monorepo)

```
github.com/jmenichole/tiltcheck-monorepo
│
├── apps/
│   │
│   ├── bet-check-backend/          ← MIGRATED: Backend
│   │   ├── main.py                 │  (from bet-check/backend/)
│   │   ├── db.py                   │
│   │   ├── mines.py                │
│   │   ├── scripts/                │
│   │   ├── requirements.txt        │
│   │   ├── Dockerfile              │
│   │   └── *.sql                   │
│   │                               │
│   ├── bet-check-frontend/         ← MIGRATED: Frontend
│   │   ├── components/             │  (from bet-check/frontend/)
│   │   ├── pages/                  │
│   │   ├── styles/                 │
│   │   ├── package.json            │
│   │   └── Dockerfile              │
│   │                               │
│   └── [other-apps]/               ← Existing monorepo apps
│
├── infrastructure/
│   └── docker/
│       └── bet-check/              ← MIGRATED: Docker setup
│           └── docker-compose.yml  │  (from bet-check/)
│
├── docs/
│   └── bet-check/                  ← MIGRATED: Documentation
│       ├── README.md               │  (from bet-check/)
│       ├── INDEX.md                │  (new)
│       └── ...                     │
│
├── .env.example                    ← UPDATED: With bet-check vars
└── README.md                       ← UPDATED: Mention bet-check
```

---

## Migration Mapping

### Backend Files

```
FROM: bet-check/backend/*
TO:   apps/bet-check-backend/*

┌──────────────────────────┐     ┌───────────────────────────────┐
│ bet-check/               │     │ tiltcheck-monorepo/           │
│                          │     │                               │
│ backend/                 │ ──→ │ apps/bet-check-backend/       │
│  ├─ main.py              │ ──→ │  ├─ main.py                   │
│  ├─ db.py                │ ──→ │  ├─ db.py                     │
│  ├─ mines.py             │ ──→ │  ├─ mines.py                  │
│  └─ ...                  │ ──→ │  └─ ...                       │
│                          │     │                               │
│ requirements.txt         │ ──→ │  requirements.txt             │
│ Dockerfile.backend       │ ──→ │  Dockerfile                   │
│                          │     │                               │
│ scripts/                 │ ──→ │  scripts/                     │
│  ├─ seed_factors.py      │ ──→ │   ├─ seed_factors.py          │
│  └─ update_games.py      │ ──→ │   └─ update_games.py          │
│                          │     │                               │
│ *.sql                    │ ──→ │  *.sql                        │
│ test_*.py                │ ──→ │  test_*.py                    │
└──────────────────────────┘     └───────────────────────────────┘
```

### Frontend Files

```
FROM: bet-check/frontend/*
TO:   apps/bet-check-frontend/*

┌──────────────────────────┐     ┌───────────────────────────────┐
│ bet-check/               │     │ tiltcheck-monorepo/           │
│                          │     │                               │
│ frontend/                │ ──→ │ apps/bet-check-frontend/      │
│  ├─ components/          │ ──→ │  ├─ components/               │
│  ├─ pages/               │ ──→ │  ├─ pages/                    │
│  ├─ styles/              │ ──→ │  ├─ styles/                   │
│  ├─ package.json         │ ──→ │  ├─ package.json             │
│  ├─ tsconfig.json        │ ──→ │  ├─ tsconfig.json            │
│  ├─ tailwind.config.ts   │ ──→ │  ├─ tailwind.config.ts       │
│  ├─ next.config.js       │ ──→ │  ├─ next.config.js           │
│  └─ Dockerfile           │ ──→ │  └─ Dockerfile               │
└──────────────────────────┘     └───────────────────────────────┘
```

### Infrastructure Files

```
FROM: bet-check/docker-compose.yml
TO:   infrastructure/docker/bet-check/docker-compose.yml

┌──────────────────────────┐     ┌───────────────────────────────┐
│ bet-check/               │     │ tiltcheck-monorepo/           │
│                          │     │                               │
│ docker-compose.yml       │ ──→ │ infrastructure/docker/        │
│                          │     │   bet-check/                  │
│ (with updated paths)     │     │     docker-compose.yml        │
└──────────────────────────┘     └───────────────────────────────┘
```

---

## Migration Timeline

```
Hour 0:00 ─┬─ START
           │
Hour 0:05 ─┼─ ✓ Preparation Complete
           │   • Backups created
           │   • Branch created
           │   • Structure analyzed
           │
Hour 0:50 ─┼─ ✓ Backend Migrated
           │   • Files copied
           │   • Config updated
           │   • Local test passed
           │
Hour 1:35 ─┼─ ✓ Frontend Migrated
           │   • Files copied
           │   • package.json updated
           │   • Local test passed
           │
Hour 2:05 ─┼─ ✓ Infrastructure Setup
           │   • Docker Compose created
           │   • Paths updated
           │   • Env vars configured
           │
Hour 2:25 ─┼─ ✓ Documentation Migrated
           │   • Docs copied
           │   • READMEs created
           │   • Links updated
           │
Hour 2:55 ─┼─ ✓ Testing Complete
           │   • Backend tested
           │   • Frontend tested
           │   • Docker tested
           │   • Integration tested
           │
Hour 3:00 ─┴─ END ✅ Migration Complete
```

---

## Network Architecture

### Before Migration

```
┌─────────────────────────────────────────────────────────────┐
│                    bet-check (standalone)                    │
└─────────────────────────────────────────────────────────────┘

Internet
    ↓
    ↓ HTTP
    ↓
┌─────────────────────┐
│   Frontend          │  Port 3000/9000
│   (Next.js)         │  ← User Interface
└──────────┬──────────┘
           │
           │ REST API
           ↓
┌─────────────────────┐
│   Backend           │  Port 8000
│   (FastAPI)         │  ← Business Logic
└──────────┬──────────┘
           │
           │ PostgreSQL
           ↓
┌─────────────────────┐
│   Supabase          │  External Service
│   (Database)        │  ← Data Storage
└─────────────────────┘
```

### After Migration

```
┌─────────────────────────────────────────────────────────────┐
│              tiltcheck-monorepo (unified)                    │
└─────────────────────────────────────────────────────────────┘

Internet
    ↓
    ↓ HTTP
    ↓
┌──────────────────────────────────────────────────────────────┐
│                     Monorepo Apps                             │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │ bet-check      │  │ other-app-1    │  │ other-app-2  │   │
│  │ frontend       │  │ frontend       │  │ frontend     │   │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘   │
│           │                   │                  │            │
│           │ REST              │ REST             │ REST       │
│           ↓                   ↓                  ↓            │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │ bet-check      │  │ other-app-1    │  │ other-app-2  │   │
│  │ backend        │  │ backend        │  │ backend      │   │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘   │
└───────────┼────────────────────┼──────────────────┼───────────┘
            │                    │                  │
            │                    │                  │
            │ PostgreSQL         │ Database         │ Database
            ↓                    ↓                  ↓
┌─────────────────────┐  ┌──────────────┐  ┌──────────────┐
│   Supabase          │  │  Database 1  │  │  Database 2  │
│   (bet-check DB)    │  │              │  │              │
└─────────────────────┘  └──────────────┘  └──────────────┘

Note: Database connection remains unchanged - same Supabase instance
```

---

## Docker Compose Flow

### Before Migration

```
docker-compose.yml (in root)
│
├─ backend service
│  ├─ Build: ./Dockerfile.backend
│  ├─ Context: .
│  └─ Port: 8000
│
└─ frontend service
   ├─ Build: ./frontend/Dockerfile
   ├─ Context: ./frontend
   └─ Port: 3000 or 9000
```

### After Migration

```
infrastructure/docker/bet-check/docker-compose.yml
│
├─ backend service
│  ├─ Build: ../../../apps/bet-check-backend/Dockerfile
│  ├─ Context: ../../../apps/bet-check-backend
│  └─ Port: 8000
│
└─ frontend service
   ├─ Build: ../../../apps/bet-check-frontend/Dockerfile
   ├─ Context: ../../../apps/bet-check-frontend
   └─ Port: 9000
```

**Key Change:** Paths are relative to docker-compose.yml location

---

## Environment Variables Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Environment Variables                      │
└─────────────────────────────────────────────────────────────┘

BEFORE:
  .env (root)
    ↓
    ├─→ backend/ (reads: SUPABASE_URL, SUPABASE_KEY)
    └─→ frontend/ (reads: NEXT_PUBLIC_API_URL)

AFTER:
  .env (monorepo root)
    ↓
    ├─→ apps/bet-check-backend/ (reads: SUPABASE_URL, SUPABASE_KEY)
    ├─→ apps/bet-check-frontend/ (reads: NEXT_PUBLIC_API_URL)
    └─→ infrastructure/docker/bet-check/ (passes to containers)

NOTE: Same variables, same values, different location
```

---

## Decision Tree

```
                        Start Migration?
                              │
                ┌─────────────┴─────────────┐
                │                           │
               YES                          NO
                │                           │
                ↓                           ↓
       Review Documentation         Wait / Reconsider
                │
                ↓
    Choose Migration Approach
                │
        ┌───────┴───────┐
        │               │
   Experienced?      New to Stack?
        │               │
        ↓               ↓
  Quick Start     Full Plan
  (30 min)        (4 hours)
        │               │
        └───────┬───────┘
                │
                ↓
         Execute Migration
                │
        ┌───────┴───────┐
        │               │
    Success?        Failed?
        │               │
        ↓               ↓
   Verify & Test   Troubleshoot
        │               │
        │               ├─→ Check Section 7
        │               │   (Common Issues)
        │               │
        │               ├─→ Still Failing?
        │               │        │
        │               │        ↓
        │               └──→ Rollback
        │                    (Section 6)
        ↓
   Commit & Push
        │
        ↓
   Create PR
        │
        ↓
   Review & Merge
        │
        ↓
   Archive Old Repo
        │
        ↓
    ✅ COMPLETE!
```

---

## File Size Comparison

```
Component              Files   Size     Lines of Code
─────────────────────────────────────────────────────────
Backend               7       50 KB    ~3,500
Frontend              20      150 KB   ~5,000
Documentation         30+     500 KB   ~15,000
Dependencies
  - Python            8       15 MB    -
  - Node.js           18      200 MB   -
Database Schemas      4       20 KB    ~500
Docker Files          3       5 KB     ~100
─────────────────────────────────────────────────────────
Total (excl. deps)    65+     725 KB   ~24,000
Total (incl. deps)    -       940 MB   -
```

---

## Port Mapping

```
┌────────────┬──────────┬────────────┬──────────────────┐
│ Service    │ Before   │ After      │ Notes            │
├────────────┼──────────┼────────────┼──────────────────┤
│ Backend    │ 8000     │ 8000       │ Unchanged        │
│ Frontend   │ 3000     │ 9000       │ Changed (avoid   │
│            │ (or 9000)│            │ conflicts)       │
│ Database   │ External │ External   │ Supabase (cloud) │
│            │ (Supab.) │ (Supabase) │                  │
└────────────┴──────────┴────────────┴──────────────────┘
```

---

## Testing Checkpoints

```
Phase 1: Backend Testing
│
├─ [ ] Health Check
│   curl http://localhost:8000/health
│   Expected: {"status": "ok"}
│
├─ [ ] API Endpoints
│   curl http://localhost:8000/games
│   Expected: JSON array of games
│
└─ [ ] API Documentation
    open http://localhost:8000/docs
    Expected: Swagger UI loads

Phase 2: Frontend Testing
│
├─ [ ] Home Page
│   open http://localhost:9000
│   Expected: Game list renders
│
├─ [ ] API Connection
│   Check browser console
│   Expected: No errors, API calls succeed
│
└─ [ ] Navigation
    Test all routes
    Expected: All pages load

Phase 3: Integration Testing
│
├─ [ ] Backend ↔ Frontend
│   Make API calls from UI
│   Expected: Data flows correctly
│
├─ [ ] Backend ↔ Database
│   Test CRUD operations
│   Expected: Supabase operations work
│
└─ [ ] Docker Compose
    docker-compose up
    Expected: Both services start

Phase 4: End-to-End Testing
│
└─ [ ] Full User Flow
    1. Load homepage
    2. View game prediction
    3. Check analytics
    4. Use AI chat
    Expected: Everything works
```

---

## Success Indicators

```
✅ GREEN LIGHTS (All Must Be True)
│
├─ ✓ Backend starts without errors
├─ ✓ Frontend starts without errors
├─ ✓ API health check returns 200
├─ ✓ Frontend loads in browser
├─ ✓ API calls succeed (no CORS errors)
├─ ✓ Database queries work
├─ ✓ Docker Compose builds successfully
├─ ✓ All tests pass
├─ ✓ No console errors
└─ ✓ Documentation is accurate

⚠️ YELLOW LIGHTS (Review Needed)
│
├─ ~ Some tests skipped
├─ ~ Minor console warnings
├─ ~ Docs need updates
└─ ~ Performance slightly slower

🔴 RED LIGHTS (Must Fix)
│
├─ ✗ Services won't start
├─ ✗ API returns errors
├─ ✗ Frontend can't connect
├─ ✗ Database connection fails
├─ ✗ Tests failing
└─ ✗ Docker build fails
```

---

## Quick Reference: Commands by Phase

```
┌─────────────┬──────────────────────────────────────────────┐
│ Phase       │ Commands                                     │
├─────────────┼──────────────────────────────────────────────┤
│ Prep        │ git clone <monorepo>                         │
│             │ git checkout -b feature/migrate-bet-check    │
├─────────────┼──────────────────────────────────────────────┤
│ Backend     │ cp -r backend/* apps/bet-check-backend/      │
│             │ cd apps/bet-check-backend                    │
│             │ python -m uvicorn main:app --reload          │
├─────────────┼──────────────────────────────────────────────┤
│ Frontend    │ cp -r frontend/* apps/bet-check-frontend/    │
│             │ cd apps/bet-check-frontend                   │
│             │ npm install && npm run dev                   │
├─────────────┼──────────────────────────────────────────────┤
│ Docker      │ cd infrastructure/docker/bet-check           │
│             │ docker-compose up --build                    │
├─────────────┼──────────────────────────────────────────────┤
│ Test        │ curl http://localhost:8000/health            │
│             │ python test_api.py                           │
│             │ open http://localhost:9000                   │
├─────────────┼──────────────────────────────────────────────┤
│ Commit      │ git add apps/ infrastructure/ docs/          │
│             │ git commit -m "feat: migrate bet-check"      │
│             │ git push origin feature/migrate-bet-check    │
└─────────────┴──────────────────────────────────────────────┘
```

---

## Visual Rollback Path

```
PROBLEM DETECTED!
       │
       ↓
┌──────────────┐
│ Is it merged?│
└──────┬───────┘
       │
   ┌───┴───┐
   NO     YES
   │       │
   ↓       ↓
Delete   Revert
Branch   Commit
   │       │
   │       ↓
   │   git revert -m 1 <hash>
   │       │
   └───┬───┘
       │
       ↓
  Original repo
  still works!
       │
       ↓
   Fix issues
       │
       ↓
  Try again
```

---

## Documentation Roadmap

```
Start Here
    ↓
MIGRATION_SUMMARY.md
(Executive overview)
    │
    ├─→ For detailed process
    │   └─→ MIGRATION_PLAN.md
    │       (60 pages, comprehensive)
    │
    ├─→ For quick execution
    │   └─→ MIGRATION_QUICK_START.md
    │       (30-minute guide)
    │
    ├─→ For step-by-step
    │   └─→ MIGRATION_CHECKLIST.md
    │       (Print & check off)
    │
    └─→ For visual learners
        └─→ MIGRATION_VISUAL_GUIDE.md
            (This document!)
```

---

## Legend

```
Symbol  Meaning
──────  ─────────────────────────────
→       Flow direction
│       Connection
├─      Branch
└─      End of branch
↓       Next step
✓       Completed
✗       Failed
~       Warning
[ ]     Checkbox (unchecked)
[x]     Checkbox (checked)
```

---

## Color Coding (for printed version)

```
🟢 GREEN  = Safe, working, complete
🟡 YELLOW = Caution, review needed
🔴 RED    = Error, must fix
🔵 BLUE   = Information
⚪ WHITE  = Neutral, no action
```

---

## Key Metrics Dashboard

```
┌─────────────────────────────────────────────────────────┐
│                  MIGRATION METRICS                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Total Files to Migrate:     65+                       │
│  Total Size (excl deps):     725 KB                    │
│  Lines of Code:              ~24,000                   │
│                                                         │
│  Estimated Time:             3-4 hours                 │
│  Actual Time:                _____ hours               │
│                                                         │
│  Risk Level:                 LOW ⚠️                    │
│  Complexity:                 LOW-MEDIUM                │
│  Reversibility:              HIGH ✅                   │
│                                                         │
│  Tests Passing:              _____ / _____             │
│  Success Rate:               _____%                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Final Checklist

```
Pre-Migration
  [ ] Read documentation
  [ ] Understand structure
  [ ] Create backups
  [ ] Prepare environment

Migration
  [ ] Backend complete
  [ ] Frontend complete
  [ ] Infrastructure complete
  [ ] Documentation complete

Verification
  [ ] Backend tests pass
  [ ] Frontend tests pass
  [ ] Docker works
  [ ] Integration works

Finalization
  [ ] Commit changes
  [ ] Push to remote
  [ ] Create PR
  [ ] Archive old repo

🎉 COMPLETE!
```

---

**End of Visual Guide**

For detailed instructions, see:
- MIGRATION_PLAN.md (complete guide)
- MIGRATION_CHECKLIST.md (step-by-step)
- MIGRATION_QUICK_START.md (30-minute)
- MIGRATION_SUMMARY.md (executive overview)

---

**Document Version:** 1.0  
**Last Updated:** December 18, 2024  
**Author:** Jamie Vargas (@jmenichole)
