# 🎯 Quick Deploy Steps - BetCheck

## You're 3 Steps Away from Going Live! 🚀

All deployment files are configured and pushed to GitHub. Follow these steps:

---

## Step 1: Enable GitHub Pages (2 minutes)

1. Go to: `https://github.com/jmenichole/bet-check/settings/pages`
2. Under **Build and deployment**:
   - **Source**: Select `GitHub Actions`
3. Click **Save**

That's it! The workflow will automatically trigger.

---

## Step 2: Deploy Backend to Render.com (5 minutes)

### Quick Deploy Button:
1. Go to: https://render.com/deploy
2. Click **"Connect Account"** (sign up if needed - it's free)
3. Once logged in, use this link for one-click deploy:
   ```
   https://render.com/deploy?repo=https://github.com/jmenichole/bet-check
   ```

### Manual Deploy (Alternative):
1. Sign up at https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub: `jmenichole/bet-check`
4. Configure:
   - **Name**: `bet-check-backend`
   - **Root Directory**: (leave blank)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Add Environment Variables (all optional - will use demo mode):
   - `SUPABASE_URL` (optional)
   - `SUPABASE_KEY` (optional)
6. Click **"Create Web Service"**
7. Wait 2-5 minutes for deployment
8. **Copy your backend URL**: `https://bet-check-backend.onrender.com`

---

## Step 3: Connect Frontend to Backend (1 minute)

1. Go to: `https://github.com/jmenichole/bet-check/settings/secrets/actions`
2. Click **"New repository secret"**
3. Add:
   - **Name**: `BACKEND_URL`
   - **Value**: Your Render backend URL (e.g., `https://bet-check-backend.onrender.com`)
4. Click **"Add secret"**
5. Go to **Actions** tab and re-run the deployment workflow

---

## ✅ Verify Deployment

### Frontend (GitHub Pages):
- **URL**: `https://jmenichole.github.io/bet-check`
- Check: Can you see the games list?
- Check: Do sport filter tabs work?

### Backend (Render):
- **URL**: `https://your-backend-url.onrender.com/health`
- Should return: `{"status":"healthy","service":"sports-prediction-api"}`

### Full Integration Test:
1. Open your GitHub Pages site
2. Click on any game
3. Prediction should load
4. Test mines game
5. Check dashboard analytics

---

## 🎉 You're Live!

**Frontend**: `https://jmenichole.github.io/bet-check`
**Backend**: `https://bet-check-backend.onrender.com`

### Share Your Site:
- Direct Link: `https://jmenichole.github.io/bet-check`
- Add to Portfolio: Link from `https://jmenichole.github.io/Portfolio/`

---

## 🐛 Troubleshooting

### GitHub Pages not deploying?
- Check: **Settings** → **Pages** → Source is `GitHub Actions`
- Check: **Actions** tab for build errors
- Look for the green checkmark ✓

### Backend not responding?
- Check Render dashboard for errors
- Verify environment variables (optional for demo mode)
- Free tier sleeps after 15 min - first request wakes it (30s delay)

### API calls failing?
- Press F12 → Console tab
- Look for CORS errors or 404s
- Verify `BACKEND_URL` secret matches your Render URL

### Need to update code?
```bash
git add -A
git commit -m "Your changes"
git push
# Both frontend and backend auto-deploy!
```

---

## 📊 Current Build Status

Check deployment status:
- **Actions**: https://github.com/jmenichole/bet-check/actions
- **Pages**: https://github.com/jmenichole/bet-check/deployments

---

## 💡 Pro Tips

1. **First Load**: Backend might take 30s to wake up (free tier)
2. **Demo Mode**: Works without Supabase - uses ESPN live data
3. **Custom Domain**: Can add in GitHub Pages settings
4. **Analytics**: Add Google Analytics in `_app.tsx`
5. **Monitoring**: Set up Render email alerts for backend errors

---

## 🎁 What You Get (All Free)

- ✅ Live frontend on GitHub Pages
- ✅ Live backend API on Render
- ✅ Automatic deployments on push
- ✅ Live sports data from ESPN
- ✅ Mines game predictor
- ✅ Multi-sport support (NBA, NFL, NHL, NCAAF, NCAAB)
- ✅ Professional UI with sport filters
- ✅ Adaptive learning predictions

**Total Cost**: $0/month 🎉

---

For detailed instructions, see `DEPLOYMENT.md`
