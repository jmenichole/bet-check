# 🚀 Deployment Guide - BetCheck to GitHub Pages

## Overview

BetCheck requires **two deployments**:
1. **Backend (FastAPI)** → Server hosting (Render/Railway/Fly.io)
2. **Frontend (Next.js)** → GitHub Pages (static hosting)

---

## 📋 Prerequisites

- GitHub account with repository access
- Backend hosting account (choose one):
  - [Render.com](https://render.com) (Recommended - Free tier)
  - [Railway.app](https://railway.app) (Free tier)
  - [Fly.io](https://fly.io) (Free tier)

---

## Part 1: Deploy Backend (Choose One Platform)

### Option A: Render.com (Recommended - Free Tier)

1. **Sign up** at [render.com](https://render.com)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `jmenichole/bet-check`
   - Configure:
     - **Name**: `bet-check-backend`
     - **Root Directory**: Leave blank
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free

3. **Add Environment Variables**:
   - `SUPABASE_URL` = your Supabase URL (or leave empty for demo mode)
   - `SUPABASE_KEY` = your Supabase key (or leave empty for demo mode)
   - `SPORTS_API_KEY` = (optional - not currently required)

4. **Deploy** - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Note your backend URL: `https://bet-check-backend.onrender.com`

### Option B: Railway.app

1. **Sign up** at [railway.app](https://railway.app)

2. **Create New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `jmenichole/bet-check`

3. **Configure Service**:
   - Railway auto-detects Python
   - Add **Start Command** (if not auto-detected):
     ```
     uvicorn backend.main:app --host 0.0.0.0 --port $PORT
     ```

4. **Add Environment Variables** in Settings:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

5. **Deploy** - Automatic on push
   - Note your backend URL from Railway dashboard

---

## Part 2: Deploy Frontend to GitHub Pages

### Step 1: Enable GitHub Pages

1. Go to your repository: `https://github.com/jmenichole/bet-check`
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Build and deployment**:
   - **Source**: GitHub Actions
   - Click **Save**

### Step 2: Add Backend URL Secret

1. In repository settings, go to **Secrets and variables** → **Actions**
2. Click **New repository secret**:
   - **Name**: `BACKEND_URL`
   - **Value**: Your backend URL (e.g., `https://bet-check-backend.onrender.com`)
   - Click **Add secret**

### Step 3: Push Deployment Configuration

The deployment workflow is already configured in `.github/workflows/deploy-frontend.yml`.

```bash
cd /Users/fullsail/bet-check
git add -A
git commit -m "Add deployment configuration for GitHub Pages and Render"
git push
```

### Step 4: Monitor Deployment

1. Go to **Actions** tab in your GitHub repository
2. Watch the "Deploy Frontend to GitHub Pages" workflow
3. Once complete (✓), your site will be live at:
   ```
   https://jmenichole.github.io/bet-check
   ```

---

## 🔧 Troubleshooting

### Frontend not loading?
- Check Actions tab for build errors
- Verify `BACKEND_URL` secret is set correctly
- Ensure GitHub Pages is enabled (Settings → Pages)

### Backend not responding?
- Check Render/Railway logs for errors
- Verify environment variables are set
- Test backend directly: `https://your-backend-url.com/health`

### CORS errors?
The backend already includes CORS for all origins. If issues persist:
```python
# backend/main.py already has:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API calls failing?
- Open browser DevTools → Network tab
- Check if requests go to correct backend URL
- Verify backend is deployed and healthy

---

## 📝 Post-Deployment Checklist

- [ ] Backend deployed and accessible at `/health` endpoint
- [ ] GitHub Pages site live at `https://jmenichole.github.io/bet-check`
- [ ] Can view games list on homepage
- [ ] Sport filter tabs work correctly
- [ ] Mines game loads and functions
- [ ] Dashboard shows analytics
- [ ] Predictions work for individual games

---

## 🎯 Quick Deploy Commands

```bash
# 1. Commit deployment configs
git add -A
git commit -m "Add production deployment configuration"
git push

# 2. The GitHub Action will automatically:
#    ✓ Build Next.js frontend
#    ✓ Export static files
#    ✓ Deploy to GitHub Pages

# 3. Deploy backend separately on Render/Railway (one-time setup)
```

---

## 💰 Cost Breakdown

| Service | Tier | Cost |
|---------|------|------|
| GitHub Pages | Free | $0/month |
| Render.com (Backend) | Free | $0/month |
| Supabase (Database) | Free | $0/month |
| **Total** | | **$0/month** |

**Note**: Free tiers have limitations:
- Render: 750 hours/month, sleeps after 15 min inactivity
- GitHub Pages: 1GB storage, 100GB bandwidth/month

---

## 🔄 Future Updates

After initial deployment, updates are automatic:

```bash
# Make code changes
git add -A
git commit -m "Your changes"
git push

# Frontend: Auto-deploys via GitHub Actions
# Backend: Auto-deploys on Render/Railway
```

---

## 📞 Support

**Backend URL Not Set?** The workflow defaults to `https://bet-check-backend.onrender.com`
Set `BACKEND_URL` secret in GitHub to override.

**Need Help?** Check these logs:
- Frontend build: GitHub Actions tab
- Backend: Render/Railway logs dashboard
- Browser errors: DevTools Console (F12)
