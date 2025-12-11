# Railway.app Backend Deployment Configuration
# Deploy your FastAPI backend to Railway.app

# 1. Install Railway CLI: npm install -g @railway/cli
# 2. Run: railway login
# 3. Run: railway init
# 4. Run: railway up

# Or deploy via GitHub:
# 1. Connect repository at railway.app
# 2. Set environment variables in Railway dashboard
# 3. Deploy automatically on push

# Required Environment Variables (set in Railway dashboard):
# - SUPABASE_URL
# - SUPABASE_KEY
# - SPORTS_API_KEY (optional)
# - PORT (automatically set by Railway)

# Start Command (Railway auto-detects, or set manually):
# uvicorn backend.main:app --host 0.0.0.0 --port $PORT
