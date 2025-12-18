# Bet-Check Migration Checklist

**Quick Reference Guide for Migrating to tiltcheck-monorepo**

📋 Print this checklist and check off items as you complete them.

---

## Pre-Migration (30 minutes)

### Backup & Preparation
- [ ] Create backup branch in bet-check repo
  ```bash
  git checkout -b backup/pre-migration-$(date +%Y%m%d)
  git push origin backup/pre-migration-$(date +%Y%m%d)
  ```
- [ ] Test current bet-check works locally
  - [ ] Backend runs: `http://localhost:8000/docs`
  - [ ] Frontend runs: `http://localhost:3000`
  - [ ] Docker Compose works: `docker-compose up`
- [ ] Export .env file to secure location
- [ ] Document any local modifications

### Monorepo Analysis
- [ ] Clone tiltcheck-monorepo
- [ ] Create feature branch: `feature/migrate-bet-check`
- [ ] Identify monorepo structure (apps/, services/, packages/)
- [ ] Check for port conflicts (8000, 3000, 9000)
- [ ] Review existing docker-compose setup

---

## Backend Migration (45 minutes)

### Directory Setup
- [ ] Create `apps/bet-check-backend/` (or appropriate path)
- [ ] Copy backend code files
- [ ] Copy `requirements.txt`
- [ ] Copy `Dockerfile.backend` as `Dockerfile`
- [ ] Copy scripts directory
- [ ] Copy database schemas (*.sql files)
- [ ] Copy test files (test_*.py)

### Configuration
- [ ] Create backend README.md
- [ ] Update imports if directory structure changed
- [ ] Test backend starts locally:
  ```bash
  cd apps/bet-check-backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python -m uvicorn main:app --reload
  ```
- [ ] Verify API docs: `http://localhost:8000/docs`
- [ ] Test health endpoint: `curl http://localhost:8000/health`

---

## Frontend Migration (45 minutes)

### Directory Setup
- [ ] Create `apps/bet-check-frontend/` (or appropriate path)
- [ ] Copy all frontend files and subdirectories
- [ ] Copy configuration files (.eslintrc.js, etc.)

### Configuration
- [ ] Update `package.json` name field
- [ ] Update `next.config.js` if basePath needed
- [ ] Create frontend README.md
- [ ] Test frontend starts locally:
  ```bash
  cd apps/bet-check-frontend
  npm install
  export NEXT_PUBLIC_API_URL=http://localhost:8000
  npm run dev
  ```
- [ ] Verify frontend loads: `http://localhost:9000` (or 3000)
- [ ] Verify frontend connects to backend

---

## Infrastructure Migration (30 minutes)

### Docker Configuration
- [ ] Create `infrastructure/docker/bet-check/` directory
- [ ] Create docker-compose.yml with updated paths
- [ ] Update context paths (relative to docker-compose.yml)
- [ ] Update port mappings if conflicts exist
- [ ] Test Docker Compose:
  ```bash
  cd infrastructure/docker/bet-check
  docker-compose up --build
  ```
- [ ] Verify backend: `http://localhost:8000`
- [ ] Verify frontend: `http://localhost:9000`

### Environment Variables
- [ ] Add bet-check vars to monorepo `.env.example`
- [ ] Copy `.env` to monorepo root
- [ ] Verify env vars load in Docker
- [ ] Test with real Supabase credentials

---

## Documentation Migration (20 minutes)

### Files to Copy
- [ ] Create `docs/bet-check/` directory
- [ ] Copy main README.md
- [ ] Copy QUICK_START_GUIDE.md
- [ ] Copy DEPLOYMENT_GUIDE.md
- [ ] Copy AI_GURU_SETUP.md
- [ ] Copy LICENSE
- [ ] Copy COPYRIGHT_IMPLEMENTATION.md

### Create New Docs
- [ ] Create docs/bet-check/INDEX.md
- [ ] Create docs/bet-check/MIGRATION_NOTES.md
- [ ] Update monorepo root README.md with bet-check section

---

## Monorepo Integration (30 minutes)

### Package Configuration
- [ ] Add bet-check to workspaces (if using npm workspaces)
- [ ] Add build scripts to root package.json:
  - [ ] `bet-check:backend`
  - [ ] `bet-check:frontend`
  - [ ] `bet-check:docker`
  - [ ] `bet-check:test`

### Git Operations
- [ ] Review all changes: `git status`
- [ ] Stage files: `git add apps/ infrastructure/ docs/ .env.example`
- [ ] Commit with descriptive message
- [ ] Push to remote: `git push origin feature/migrate-bet-check`

---

## Verification & Testing (30 minutes)

### Functional Tests
- [ ] **Backend API**
  - [ ] Health check: `GET /health`
  - [ ] List games: `GET /games`
  - [ ] Get prediction: `GET /predict/{game_id}`
  - [ ] API docs: `/docs`

- [ ] **Frontend Pages**
  - [ ] Home page: `/`
  - [ ] Game detail: `/game/[id]`
  - [ ] Dashboard: `/dashboard`
  - [ ] AI Guru: `/guru`
  - [ ] Mines game: `/mines`

- [ ] **Docker Compose**
  - [ ] Both services start
  - [ ] Backend accessible
  - [ ] Frontend accessible
  - [ ] Services communicate
  - [ ] Hot reload works

### Integration Tests
- [ ] Run `python test_api.py`
- [ ] Run `python test_chat.py`
- [ ] Run migration test script (if created)
- [ ] Test database operations
- [ ] Verify Supabase connection

### Performance Tests
- [ ] Measure startup time
- [ ] Check API response times
- [ ] Monitor Docker resource usage
- [ ] Verify no memory leaks

---

## Cleanup & Finalization (20 minutes)

### Documentation Updates
- [ ] Create MIGRATION_NOTES.md with results
- [ ] Update all documentation links
- [ ] Verify installation instructions work
- [ ] Add troubleshooting notes for issues found

### Repository Management
- [ ] Create Pull Request in monorepo
- [ ] Add descriptive PR description
- [ ] Request code review
- [ ] Address review feedback

### Original Repository
- [ ] Add MIGRATION_NOTICE.md to bet-check repo
- [ ] Update bet-check README with migration notice
- [ ] Commit and push notice
- [ ] Archive bet-check repository (GitHub Settings)

---

## Post-Merge Tasks

### CI/CD Updates (if applicable)
- [ ] Update GitHub Actions workflows
- [ ] Update deployment pipelines
- [ ] Update environment variables in CI
- [ ] Test automated deployments

### Team Communication
- [ ] Notify team of migration
- [ ] Update internal documentation
- [ ] Update deployment runbooks
- [ ] Schedule knowledge sharing session

### Monitoring
- [ ] Monitor production for 24-48 hours
- [ ] Check error logs
- [ ] Verify metrics are flowing
- [ ] Confirm alerts are working

---

## Rollback Plan (If Needed)

### Before Merge
- [ ] Discard monorepo branch
- [ ] Return to using bet-check repo
- [ ] Fix issues and retry

### After Merge
- [ ] Revert merge commit
- [ ] Deploy from old bet-check repo temporarily
- [ ] Fix issues in development
- [ ] Re-migrate when ready

---

## Success Criteria

✅ Migration is complete when ALL of these are true:

- [ ] All files copied to monorepo
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Docker Compose works
- [ ] All API endpoints respond
- [ ] Frontend connects to backend
- [ ] Database operations work
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Original repo archived

---

## Time Tracking

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| Pre-Migration | 30 min | | |
| Backend | 45 min | | |
| Frontend | 45 min | | |
| Infrastructure | 30 min | | |
| Documentation | 20 min | | |
| Integration | 30 min | | |
| Testing | 30 min | | |
| Cleanup | 20 min | | |
| **Total** | **4 hours** | | |

---

## Quick Commands Reference

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

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build
```

---

## Emergency Contacts

**Migration Lead:** Jamie Vargas  
**Email:** jme@tiltcheck.me  
**GitHub:** @jmenichole

**Resources:**
- Full Plan: `MIGRATION_PLAN.md`
- Issues: Section 7 of MIGRATION_PLAN.md
- Rollback: Section 6 of MIGRATION_PLAN.md

---

## Notes & Issues

Use this space to track issues encountered during migration:

```
Issue 1: [Description]
Solution: [What fixed it]
Time lost: [X minutes]

Issue 2: [Description]
Solution: [What fixed it]
Time lost: [X minutes]
```

---

**Migration Date:** _______________  
**Completed By:** _______________  
**Review By:** _______________  
**Sign-off Date:** _______________  

---

✅ **MIGRATION COMPLETE!**

Remember to:
- Update deployment configurations
- Monitor production for 24-48 hours
- Archive old repository
- Celebrate! 🎉
