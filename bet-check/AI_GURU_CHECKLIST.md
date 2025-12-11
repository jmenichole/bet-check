# AI Sports Guru - Quick Start Deployment Checklist

**Feature:** AI-powered chat interface with game recommendations  
**Status:** Code complete, ready for deployment  
**Date:** December 11, 2025

---

## ✅ Pre-Deployment Checklist

### Database Setup
- [ ] Log into Supabase dashboard at https://supabase.com
- [ ] Navigate to your BetCheck project
- [ ] Go to **SQL Editor**
- [ ] Open `schema_chat.sql` from project root
- [ ] Copy and paste the entire SQL content
- [ ] Click **Run** to create `chat_messages` table
- [ ] Verify table created: Check **Table Editor** → `chat_messages`

### Backend Verification
- [ ] Navigate to `backend/` directory: `cd backend`
- [ ] Start backend server: `python -m uvicorn main:app --reload`
- [ ] Verify health check: Open http://localhost:8000/health
- [ ] Check new endpoints in Swagger: http://localhost:8000/docs
- [ ] Confirm you see: `/chat`, `/chat/popular-games`, `/chat/history`

### Frontend Setup
- [ ] Navigate to `frontend/` directory: `cd frontend`
- [ ] Install dependencies (if needed): `npm install`
- [ ] Verify environment variables in `.env`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```
- [ ] Start development server: `npm run dev`
- [ ] Verify site loads: Open http://localhost:3000

---

## 🧪 Testing Checklist

### Automated Backend Tests
- [ ] Navigate to project root: `cd /Users/fullsail/bet-check`
- [ ] Run test script: `python test_chat.py`
- [ ] Verify all 4 tests pass:
  - Backend Health ✅
  - Chat Endpoint ✅
  - Popular Games ✅
  - Chat History ✅

### Manual Frontend Tests
- [ ] Navigate to http://localhost:3000
- [ ] Click "🤖 AI Guru" in header
- [ ] Should navigate to `/guru` page
- [ ] Verify page loads without errors

### Chat Interface Tests
- [ ] **Test 1: Basic Chat**
  - [ ] Type "Show me the best NBA picks" in chat input
  - [ ] Press Enter
  - [ ] AI response appears in pink bubble
  - [ ] Suggested game cards display below message
  - [ ] Chat auto-scrolls to bottom

- [ ] **Test 2: Intent Detection**
  - [ ] Try: "What are safe bets?"
  - [ ] Verify AI returns high-confidence games (70%+)
  - [ ] Try: "Any upsets possible?"
  - [ ] Verify AI returns low-confidence games (<60%)

- [ ] **Test 3: Sport Filtering**
  - [ ] Try: "Best NFL games?"
  - [ ] Verify only NFL games returned
  - [ ] Try: "Show me basketball picks"
  - [ ] Verify only NBA games returned

- [ ] **Test 4: Game Card Navigation**
  - [ ] Click on a suggested game card
  - [ ] Should navigate to `/game/[game_id]` page
  - [ ] Page loads with game prediction details

### Popular Matches Tests
- [ ] **Popular Games List**
  - [ ] Scroll down below chat interface
  - [ ] "🔥 Popular Matches" section displays
  - [ ] Shows 4 game cards with confidence bars
  - [ ] Click a card → navigates to game details

### Responsive Design Tests
- [ ] **Desktop View** (browser width > 768px)
  - [ ] Chat interface spans full width
  - [ ] Popular games display in 2x2 or 4x1 grid
  - [ ] Navigation header shows all links

- [ ] **Mobile View** (browser width < 768px)
  - [ ] Chat interface is full width
  - [ ] Popular games scroll horizontally
  - [ ] Header collapses appropriately

---

## 🎨 UI/UX Verification

### Visual Elements
- [ ] AI messages have pink (#ff00cc) background with glow
- [ ] User messages have white text on dark background
- [ ] Suggested game cards have cyan borders
- [ ] Confidence bars show pink-to-cyan gradient
- [ ] Scrollbar is pink (matches theme)
- [ ] Hover effects work on cards (border brightens)

### Interactions
- [ ] Enter key sends message (not just button click)
- [ ] Loading indicator shows 3 bouncing dots
- [ ] Input field disables while waiting for AI response
- [ ] Auto-scroll only happens on new messages
- [ ] Game cards have hover effect (shadow + border glow)

---

## 🐛 Error Handling Tests

### Backend Down Scenario
- [ ] Stop backend server (Ctrl+C)
- [ ] Try sending chat message
- [ ] Verify error message displays in chat
- [ ] Restart backend, try again
- [ ] Should work normally

### No Games Available
- [ ] This will naturally work with demo data
- [ ] If no games match query, AI says "No games found"

### Network Issues
- [ ] Open browser DevTools → Network tab
- [ ] Send chat message
- [ ] Verify POST to `/chat` endpoint succeeds (200 status)
- [ ] Check response has `ai_message` and `suggested_games`

---

## 📊 Database Verification

### Check Chat History Storage
- [ ] Log into Supabase dashboard
- [ ] Go to **Table Editor** → `chat_messages`
- [ ] Should see rows with:
  - Your test user_id
  - message_text (your questions)
  - is_ai = false (your messages)
  - is_ai = true (AI responses)
  - Timestamps for all messages

### Performance Check
- [ ] Send 5-10 chat messages
- [ ] Reload `/guru` page
- [ ] Page should load quickly (<2 seconds)
- [ ] Chat history should be empty (new session)
- [ ] If you implement user_id persistence, history should show

---

## 🚀 Production Deployment (Optional)

### Backend Deployment
- [ ] Deploy to your hosting service (Heroku, Railway, AWS, etc.)
- [ ] Update `NEXT_PUBLIC_API_URL` in frontend `.env.production`:
  ```
  NEXT_PUBLIC_API_URL=https://your-backend-domain.com
  ```
- [ ] Verify health check works on production URL

### Frontend Deployment
- [ ] Deploy to Vercel/Netlify
- [ ] Set environment variable in hosting dashboard
- [ ] Test production site `/guru` page works
- [ ] Verify chat connects to production backend

### DNS & SSL
- [ ] Configure custom domain (optional)
- [ ] Ensure SSL certificate is active (HTTPS)
- [ ] Test CORS settings work with production URLs

---

## 📝 Documentation Review

### Files to Review
- [ ] Read `AI_GURU_SETUP.md` for detailed setup instructions
- [ ] Read `AI_GURU_IMPLEMENTATION.md` for technical details
- [ ] Check `README.md` has AI Guru section updated
- [ ] Verify all license headers show CC BY-NC 4.0

---

## ✨ Final Checks

### Code Quality
- [ ] No console errors in browser DevTools
- [ ] No Python errors in backend terminal
- [ ] All TypeScript compiles without errors
- [ ] ESLint/Prettier formatting is correct (if configured)

### User Experience
- [ ] Chat feels responsive and fast
- [ ] AI responses are helpful and relevant
- [ ] Game suggestions match user intent
- [ ] Navigation is intuitive
- [ ] Mobile experience is smooth

### Performance
- [ ] Page load time < 2 seconds
- [ ] Chat response time < 1 second
- [ ] No memory leaks (check after 10+ messages)
- [ ] Database queries are fast (<100ms)

---

## 🎉 Success Criteria

Your AI Sports Guru is fully deployed when:

✅ Database migration applied successfully  
✅ Backend `/chat` endpoints return valid responses  
✅ Frontend `/guru` page loads without errors  
✅ Chat interface accepts input and displays AI responses  
✅ Suggested game cards navigate to game details  
✅ Popular matches list displays below chat  
✅ All 4 automated tests pass  
✅ Manual testing complete (no critical bugs)  

---

## 🆘 Troubleshooting Quick Reference

**Problem:** Backend won't start  
**Fix:** Check Supabase credentials in `.env`, verify Python 3.8+

**Problem:** Chat returns no games  
**Fix:** Run `scripts/update_games.py` to populate database

**Problem:** Frontend shows "Cannot connect"  
**Fix:** Verify `NEXT_PUBLIC_API_URL` matches backend URL

**Problem:** Database error on chat  
**Fix:** Verify `schema_chat.sql` was applied in Supabase

**Problem:** Popular matches empty  
**Fix:** Ensure at least 4 games have predictions in database

---

## 📞 Need Help?

**Documentation:**
- Full setup guide: `AI_GURU_SETUP.md`
- Implementation details: `AI_GURU_IMPLEMENTATION.md`
- Main README: `README.md`

**Testing:**
- Run automated tests: `python test_chat.py`
- Check backend logs for errors
- Use browser DevTools Network tab

**Contact:**
- Developer: Jmenichole
- Portfolio: https://jmenichole.github.io/Portfolio/

---

**Last Updated:** December 11, 2025  
**Version:** 1.0.0  
**Status:** Ready for Deployment ✅
