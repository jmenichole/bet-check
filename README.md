# Bet Check Repository

This repository contains the **bet-check** sports prediction application.

## 📦 Migration to Monorepo

**Important:** This project is designed to be migrated into the [tiltcheck-monorepo](https://github.com/jmenichole/tiltcheck-monorepo).

### Migration Documentation

We provide comprehensive migration documentation to ensure a smooth transition:

1. **[MIGRATION_PLAN.md](bet-check/MIGRATION_PLAN.md)** - Complete migration guide (60+ pages)
   - Full project analysis
   - Step-by-step migration process
   - Troubleshooting guide
   - Rollback procedures

2. **[MIGRATION_CHECKLIST.md](bet-check/MIGRATION_CHECKLIST.md)** - Print-friendly checklist
   - Quick reference for migration tasks
   - Time tracking
   - Success criteria

3. **[MIGRATION_QUICK_START.md](bet-check/MIGRATION_QUICK_START.md)** - 30-minute fast track
   - Condensed migration steps
   - Quick commands reference
   - Common issues & solutions

### Quick Migration Overview

The migration process involves:
- Moving backend to `tiltcheck-monorepo/apps/bet-check-backend/`
- Moving frontend to `tiltcheck-monorepo/apps/bet-check-frontend/`
- Setting up Docker Compose in monorepo structure
- Updating documentation and configurations
- **No database changes needed** (Supabase stays the same)

**Estimated Time:** 2-4 hours  
**Difficulty:** Easy to Moderate  
**Risk Level:** Low (original repo unchanged)

### Getting Started with Migration

```bash
# 1. Review the migration plan
cat bet-check/MIGRATION_PLAN.md

# 2. Print the checklist
cat bet-check/MIGRATION_CHECKLIST.md

# 3. Follow quick start for fast migration
cat bet-check/MIGRATION_QUICK_START.md
```

## 📖 Project Documentation

For complete project documentation, see:
- **[bet-check/README.md](bet-check/README.md)** - Full project documentation
- **[bet-check/QUICK_START_GUIDE.md](bet-check/QUICK_START_GUIDE.md)** - Local development setup
- **[bet-check/DEPLOYMENT_GUIDE.md](bet-check/DEPLOYMENT_GUIDE.md)** - Production deployment

## 🚀 Quick Start (Current Repo)

To run bet-check in this repository before migration:

```bash
cd bet-check
cp .env.example .env
# Edit .env with your Supabase credentials
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📞 Contact

**Developer:** Jamie Vargas  
**Email:** jme@tiltcheck.me  
**GitHub:** [@jmenichole](https://github.com/jmenichole)  
**LinkedIn:** [Jamie Vargas](https://linkedin.com/in/jmenichole0)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](bet-check/LICENSE) file for details.

© 2025 Jamie Vargas. All rights reserved.
