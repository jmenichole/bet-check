# 🚀 BetCheck - Deployment Guide

Complete instructions for deploying BetCheck to production.

---

## 📋 Pre-Deployment Checklist

- [ ] All endpoints tested locally
- [ ] Database schema applied in Supabase
- [ ] Environment variables configured
- [ ] Docker images built successfully
- [ ] Frontend build completes without errors
- [ ] API tests pass (`python test_api.py`)
- [ ] CORS properly configured for your domain
- [ ] Secrets not committed to git

---

## 🐳 Docker Deployment

### 1. Build Docker Images

```bash
# Build all services
docker-compose build

# Verify builds
docker images | grep bet-check
```

### 2. Configure Production Environment

```bash
# Copy template
cp .env.example .env

# Edit with real Supabase credentials
nano .env
```

Update these values:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=sb_live_your_production_key
SPORTS_API_KEY=your_sports_api_key
NEXT_PUBLIC_API_URL=https://your-domain.com
```

### 3. Start Services

```bash
# Start in background
docker-compose up -d

# Monitor logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## ☁️ Cloud Deployment (AWS, GCP, Azure)

### AWS ECS/Fargate

```bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name bet-check-backend
aws ecr create-repository --repository-name bet-check-frontend

# 2. Tag and push images
docker tag bet-check-backend:latest {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/bet-check-backend:latest
docker push {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/bet-check-backend:latest

# 3. Create ECS task definitions (see AWS documentation)
# 4. Create ECS service
# 5. Configure load balancer
```

### Heroku Deployment

```bash
# 1. Install Heroku CLI
brew install heroku/brew/heroku

# 2. Login
heroku login

# 3. Create apps
heroku create bet-check-backend
heroku create bet-check-frontend

# 4. Set environment variables
heroku config:set SUPABASE_URL=... -a bet-check-backend
heroku config:set SUPABASE_KEY=... -a bet-check-backend

# 5. Deploy
git push heroku main
```

### Vercel (Frontend Only)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
cd frontend
vercel

# 3. Add environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://your-backend-domain
```

---

## 🗄️ Database Setup (Supabase)

### 1. Create Supabase Project

1. Visit https://supabase.com
2. Create new project
3. Wait for initialization
4. Get credentials from Settings → API

### 2. Apply Schema

```bash
# Option A: Copy-paste schema.sql in Supabase SQL editor
# Option B: Run via psql
PGPASSWORD=your_password psql -h db.{your-project}.supabase.co \
  -U postgres -d postgres -f schema.sql
```

### 3. Initialize Data

```bash
# Set environment variables
export SUPABASE_URL=your_url
export SUPABASE_KEY=your_key

# Seed factors
python scripts/seed_factors.py

# Update games
python scripts/update_games.py

# Verify setup
python scripts/verify_db.py
```

### 4. Configure RLS Policies

The schema includes public read policies. For production:

```sql
-- Restrict writes to authenticated users only (optional)
CREATE POLICY "Enable write for authenticated users" ON games
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

---

## 🔐 Security Configuration

### 1. API Keys Management

Store secrets in your deployment platform:
- AWS Secrets Manager
- Google Cloud Secret Manager
- Heroku Config Vars
- Environment variables

Never commit `.env` to version control.

### 2. CORS Configuration

Edit `backend/main.py` for production domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. HTTPS Only

Ensure all traffic is encrypted:
- Configure SSL/TLS certificates
- Redirect HTTP to HTTPS
- Use security headers

### 4. Rate Limiting

Add rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/games")
@limiter.limit("100/minute")
async def list_games(...):
    ...
```

---

## 📊 Monitoring & Logging

### Application Monitoring

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Or in cloud platform:
# - AWS CloudWatch
# - Google Cloud Logging
# - Azure Application Insights
```

### Database Monitoring

Monitor via Supabase dashboard:
- Query performance
- Database size
- RLS policies

### Health Checks

```bash
# Check API health
curl https://your-domain/health

# Implement health check in load balancer
# - Path: /health
# - Expected: {"status": "healthy"}
# - Interval: 30 seconds
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and test
        run: |
          pip install -r requirements.txt
          python test_api.py
      
      - name: Deploy to Docker
        run: |
          docker-compose build
          docker-compose push
      
      - name: Deploy to Cloud
        run: |
          # Your deployment command here
```

---

## 📈 Scaling Considerations

### Database Scaling
- Monitor connection count
- Use connection pooling for many requests
- Consider read replicas for analytics queries

### Backend Scaling
- Deploy multiple backend instances
- Use load balancer
- Monitor CPU and memory
- Scale based on request rate

### Frontend Scaling
- Use CDN (CloudFlare, AWS CloudFront)
- Enable caching headers
- Optimize images
- Use edge functions for dynamic content

---

## 🔄 Backup & Recovery

### Database Backups

```bash
# Manual backup
pg_dump -h db.{project}.supabase.co -U postgres -d postgres > backup.sql

# Restore from backup
psql -h db.{project}.supabase.co -U postgres -d postgres < backup.sql
```

Supabase includes:
- Automatic daily backups
- 7-day backup retention
- One-click restore

### Application Backups

Store in version control:
```bash
git commit -m "Backup before major change"
git push origin main
```

---

## 🚨 Troubleshooting Production

### High Latency

```bash
# Check API response times
time curl https://your-domain/health

# Monitor database queries
# In Supabase: Logs → Postgres → Query performance
```

### Database Connection Errors

```bash
# Verify credentials
psql -h db.{project}.supabase.co -U postgres

# Check connection pool
# Increase max_connections in Supabase settings
```

### Memory Issues

```bash
# Monitor container memory
docker stats

# Increase memory allocation in docker-compose.yml
services:
  backend:
    mem_limit: 1gb
    memswap_limit: 1gb
```

---

## 🎯 Performance Optimization

### Frontend Optimization
- Minify CSS/JS (Next.js does automatically)
- Enable image optimization
- Use lazy loading
- Configure caching headers

### Backend Optimization
- Add database indexes (see schema.sql)
- Use pagination for large datasets
- Cache factor weights in memory
- Use async/await for I/O operations

### Database Optimization
- Monitor slow queries
- Add indexes as needed
- Archive old predictions
- Consider partitioning large tables

---

## 📞 Support & Troubleshooting

### Getting Help

1. Check application logs
2. Run diagnostic script: `python scripts/verify_db.py`
3. Review error messages in UI
4. Check backend/frontend logs

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Update `allow_origins` in main.py |
| Database timeout | Increase `max_connections` in Supabase |
| Missing games | Run `python scripts/update_games.py` |
| High latency | Check database query performance |
| Memory errors | Increase container memory limits |

---

## 🎓 Maintenance Schedule

### Daily
- [ ] Monitor error logs
- [ ] Check API health endpoint

### Weekly
- [ ] Review analytics dashboard
- [ ] Check database size
- [ ] Monitor costs

### Monthly
- [ ] Update dependencies
- [ ] Review security logs
- [ ] Optimize database queries
- [ ] Test backup/restore

### Quarterly
- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Update documentation

---

## ✅ Deployment Verification

After deployment, verify:

1. **Health Check**
   ```bash
   curl https://your-domain/health
   ```

2. **API Endpoints**
   ```bash
   curl https://your-domain/games
   curl https://your-domain/factors
   ```

3. **Frontend Access**
   ```bash
   # Should load without errors
   https://your-domain
   ```

4. **Database Connection**
   ```bash
   python scripts/verify_db.py
   ```

5. **Full Test Suite**
   ```bash
   # Update test_api.py with production URL
   python test_api.py
   ```

---

## 📝 Deployment Record

| Date | Environment | Status | Notes |
|------|-------------|--------|-------|
| YYYY-MM-DD | Development | ✅ | Initial setup |
| YYYY-MM-DD | Staging | ✅ | QA testing |
| YYYY-MM-DD | Production | ✅ | Live deployment |

---

**Deployment Complete!** 🎉

Your BetCheck instance is now running in production. Monitor logs, track performance, and continuously improve the system.

For questions or issues, review the troubleshooting section or consult the detailed architecture guide.
