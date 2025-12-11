---
title: Bet Check - Sports Prediction Tool
description: Complete full-stack application with adaptive learning
---

# 🚀 Bet Check - Sports Prediction Tool (Reference)

## ✅ Status: Fully Generated and Ready to Launch

Reference only. For active development, use `README.md` and `QUICK_START_GUIDE.md`.

---

## 📖 Documentation Index

Read these in order:

1. **[START_HERE.md](./START_HERE.md)** ← **Start with this!**
   - Complete project overview
   - System architecture
   - Key features and capabilities
   - 10 min read

2. **[LAUNCH_CHECKLIST.md](./LAUNCH_CHECKLIST.md)** ← **Do this next**
   - Step-by-step action items
   - Phase-by-phase instructions
   - Verification checklist
   - 20-30 min execution time

3. **[QUICKSTART.md](./QUICKSTART.md)** ← **For detailed guidance**
   - Detailed setup instructions
   - Troubleshooting section
   - Configuration explanations
   - 15 min read

4. **[README.md](./README.md)** ← **Full reference**
   - Complete documentation
   - API endpoints reference
   - Feature descriptions
   - Advanced topics

5. **[FILE_STRUCTURE.md](./FILE_STRUCTURE.md)** ← **Understand organization**
   - File-by-file descriptions
   - Dependencies map
   - Directory structure

6. **[GENERATION_SUMMARY.md](./GENERATION_SUMMARY.md)** ← **What was built**
   - Complete inventory
   - Architecture details
   - Configuration options

7. **[PROJECT_SUMMARY.txt](./PROJECT_SUMMARY.txt)** ← **Quick reference**
   - Visual summary
   - Statistics
   - Key features

---

## 🎯 Quick Start (30 minutes)

### Phase 1: Database (5 min)
```bash
# 1. Create Supabase account at https://supabase.com
# 2. Create new project
# 3. Get Project URL and anon key
# 4. In SQL Editor, run schema.sql
```

### Phase 2: Configuration (2 min)
```bash
cp .env.example .env
# Edit .env with Supabase credentials
```

### Phase 3: Backend (3 min) - Terminal 1
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python main.py
```

### Phase 4: Frontend (3 min) - Terminal 2
```bash
cd frontend
npm install
npm run dev
```

### Phase 5: Data (2 min) - Terminal 3
```bash
cd scripts
python seed_factors.py
python update_games.py
```

### Phase 6: Open App
```
http://localhost:3000
```

✅ **Done! Your app is running!**

---

## 📁 What You Have

```
bet-check/
├── 📄 Documentation (6 files)
│   ├── START_HERE.md              ← Overview
│   ├── LAUNCH_CHECKLIST.md        ← Actions
│   ├── QUICKSTART.md              ← Setup guide
│   ├── README.md                  ← Reference
│   ├── FILE_STRUCTURE.md          ← Files explained
│   └── GENERATION_SUMMARY.md      ← What was built
│
├── 💻 Backend (Python/FastAPI)
│   ├── backend/main.py            ← Prediction engine
│   ├── backend/db.py              ← Database utilities
│   └── requirements.txt           ← Dependencies
│
├── 🎨 Frontend (Next.js/React)
│   ├── frontend/pages/index.tsx   ← Home page
│   ├── frontend/pages/game/[gameId].tsx  ← Game page
│   ├── frontend/pages/dashboard.tsx      ← Dashboard
│   ├── frontend/package.json            ← NPM dependencies
│   └── frontend/styles/               ← Styling
│
├── 🛠️ Scripts (Python)
│   ├── scripts/seed_factors.py     ← Initialize weights
│   ├── scripts/update_games.py     ← Fetch games
│   └── scripts/verify_db.py        ← Check database
│
├── 📊 Database
│   └── schema.sql                  ← Database structure
│
├── ⚙️ Configuration
│   ├── .env.example                ← Copy to .env
│   ├── .gitignore                  ← Git config
│   └── docker-compose.yml          ← Optional containerization
│
└── 🧪 Testing
    └── test_api.py                 ← API test suite
```

---

## 🎓 Architecture

```
Browser (http://localhost:3000)
    ↕ HTTP REST API
FastAPI Backend (http://localhost:8000)
    ↕ SQL Queries
Supabase PostgreSQL Database
```

### Prediction System
- **5 Weighted Factors**: Recent Form, Injuries, Offensive Efficiency, Defensive Efficiency, Home Court Advantage
- **Adaptive Learning**: Weights adjust based on prediction accuracy
- **Confidence Scores**: 0-100% confidence for each prediction
- **Explainability**: Top 3 reasons for each prediction

---

## 🚀 Immediate Actions Required

1. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```

2. **Add Supabase Credentials**
   - Get from: https://supabase.com
   - Paste into `.env`

3. **Run Database Schema**
   - Copy `schema.sql`
   - Run in Supabase SQL Editor

4. **Follow LAUNCH_CHECKLIST.md**
   - Step-by-step phases
   - 20-30 minutes total

---

## ✅ Success Indicators

Your app works when you see:

- ✅ Backend terminal: `INFO: Uvicorn running on http://0.0.0.0:8000`
- ✅ Frontend terminal: `Local: http://localhost:3000`
- ✅ Browser shows games list at http://localhost:3000
- ✅ Click game → see prediction page
- ✅ Dashboard shows metrics

---

## 🧠 How It Works

### Step 1: Predict
- Takes game data
- Calculates scores using 5 weighted factors
- Determines winner (higher score)
- Returns confidence and top 3 reasons

### Step 2: Actual Result
- User logs real game outcome
- System compares to prediction

### Step 3: Learn
- If correct: factor weights increase ↑
- If incorrect: factor weights decrease ↓
- Model improves over time automatically

---

## 📚 Key Files to Know

| File | Purpose | Edit For |
|------|---------|----------|
| `backend/main.py` | Prediction engine | Logic changes |
| `scripts/seed_factors.py` | Factor initialization | Initial weights |
| `frontend/pages/index.tsx` | Home page | UI changes |
| `schema.sql` | Database structure | Schema changes |
| `.env` | Configuration | Credentials |

---

## 🔧 Customization

### Learning Rate
```python
# backend/main.py, line ~110
LEARNING_RATE = 0.05  # Change to 0.01-0.1
```

### Factor Weights
```python
# scripts/seed_factors.py
"base_weight": 0.20  # Adjust starting weights
```

### Colors/Styling
```css
/* frontend/styles/globals.css */
/* Edit Tailwind colors and styles */
```

---

## 📞 Getting Help

**Setup questions?**
→ Read LAUNCH_CHECKLIST.md (step-by-step)

**Technical questions?**
→ Check http://localhost:8000/docs (API docs)

**Code questions?**
→ Files have detailed comments

**Database questions?**
→ Run `python scripts/verify_db.py`

---

## 🎯 Next Steps

1. **Today**: Follow LAUNCH_CHECKLIST.md (30 min)
2. **This Week**: Log game results, watch model learn
3. **This Month**: Integrate real API, customize UI
4. **Future**: Deploy, add auth, machine learning

---

## 📊 Project Stats

- **Files**: 30+
- **Lines of Code**: 2,500+
- **Languages**: Python, TypeScript, JavaScript, SQL
- **Setup Time**: 20-30 minutes
- **Database**: PostgreSQL/Supabase
- **API Endpoints**: 6
- **Prediction Factors**: 5
- **Frontend Pages**: 3

---

## ✨ Features

✅ AI-powered sports predictions  
✅ 5 weighted prediction factors  
✅ Automatic adaptive learning  
✅ 0-100% confidence scores  
✅ Top 3 reasons per prediction  
✅ Interactive dashboard  
✅ Mobile responsive  
✅ Production-ready code  
✅ Fully documented  
✅ Easy to customize  

---

## 🚀 Ready to Launch?

1. Read **[START_HERE.md](./START_HERE.md)** (5 min)
2. Follow **[LAUNCH_CHECKLIST.md](./LAUNCH_CHECKLIST.md)** (20-30 min)
3. Open **http://localhost:3000** ✅

**That's it! You're done!**

---

*Complete full-stack sports prediction tool with adaptive learning*  
*Built with FastAPI + Next.js + Supabase + Tailwind CSS*  
*Ready to customize and deploy*

**Happy predicting! 🎉**
