# AI Sports Guru - Setup & Testing Guide

**Feature:** Embedded AI chat module with intelligent game recommendations  
**Date Added:** December 11, 2025  
**Copyright:** Jmenichole • CC BY-NC 4.0 License

---

## Overview

The AI Sports Guru is an embedded chat interface that analyzes natural language questions and provides AI-powered game predictions with confidence scores. Users can ask about "best picks," "safe bets," "upsets," or filter by specific sports.

### Features
- 💬 **Embedded Chat Interface** - Scrollable chat history with neon-themed UI
- 🤖 **Intent Detection** - Analyzes keywords like "best", "safe", "upset", "today"
- 🏀 **Sport Filtering** - Detects NBA, NFL, MLB mentions
- 🎯 **Smart Recommendations** - Returns games filtered by confidence thresholds
- 🔥 **Popular Matches** - Shows top 4 trending games below chat
- 💾 **Chat History** - Stores conversations in database

---

## Architecture

### Backend (FastAPI)
**File:** `backend/main.py` (3 new endpoints added)

1. **POST /chat**
   - Accepts: `{message: string, user_id: string}`
   - Returns: `{ai_message: string, suggested_games: [...], timestamp: string}`
   - Logic: Parses intent → Filters games → Generates predictions → Stores chat

2. **GET /chat/popular-games**
   - Returns: Top 4 games sorted by confidence
   - Used by: PopularMatchesList component

3. **GET /chat/history**
   - Accepts: `?user_id=string`
   - Returns: Array of chat messages for user

**Intent Detection:**
```python
# Keywords trigger confidence filters
"best" or "top" → confidence >= 65%
"safe" or "sure" → confidence >= 70%
"upset" or "underdog" → confidence < 60%
"today" → scheduled_date = today

# Sport filtering
"nba" or "basketball" → sport = "NBA"
"nfl" or "football" → sport = "NFL"
"mlb" or "baseball" → sport = "MLB"
```

### Database (PostgreSQL)
**File:** `schema_chat.sql`

**Table:** `chat_messages`
```sql
- id: bigserial (primary key)
- user_id: text
- message_text: text
- is_ai: boolean
- timestamp: timestamp with time zone
```

**Indexes:**
- `idx_chat_user_id` on user_id
- `idx_chat_timestamp` on timestamp

**Security:** Row Level Security enabled with public read/insert policies

### Frontend (Next.js/React)
**New Files:**
1. `frontend/components/ChatEmbedded.tsx` - Main chat interface
2. `frontend/components/PopularMatchesList.tsx` - Popular games display
3. `frontend/pages/guru.tsx` - Dedicated AI Guru page

**Updated Files:**
- `frontend/components/Header.tsx` - Added "AI Guru" navigation link

---

## Installation

### 1. Apply Database Migration
```bash
# Option A: Using Supabase Dashboard
# 1. Log into Supabase dashboard
# 2. Go to SQL Editor
# 3. Paste contents of schema_chat.sql
# 4. Execute

# Option B: Using psql CLI
psql $DATABASE_URL < schema_chat.sql
```

### 2. Verify Backend Endpoints
```bash
# Start backend (if not running)
cd backend
python -m uvicorn main:app --reload

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me the best NBA picks",
    "user_id": "test_user"
  }'

# Test popular games
curl http://localhost:8000/chat/popular-games

# Test chat history
curl "http://localhost:8000/chat/history?user_id=test_user"
```

### 3. Install Frontend Dependencies (if needed)
```bash
cd frontend
npm install axios  # Should already be installed
```

### 4. Start Frontend
```bash
cd frontend
npm run dev
```

### 5. Access AI Guru
Open browser: `http://localhost:3000/guru`

---

## Usage Examples

### Chat Queries

**Best Picks:**
```
User: "What are the best NBA games to bet on today?"
AI: Returns games with confidence >= 65%
```

**Safe Bets:**
```
User: "Give me safe picks"
AI: Returns games with confidence >= 70%
```

**Upsets:**
```
User: "Any potential upsets in NFL?"
AI: Returns NFL games with confidence < 60%
```

**Today's Games:**
```
User: "Show me today's matches"
AI: Returns games scheduled for today
```

**Sport-Specific:**
```
User: "Best basketball picks?"
AI: Returns NBA games with confidence >= 65%
```

### Popular Matches
- Automatically displays top 4 games by confidence
- Horizontal scroll on mobile, grid on desktop
- Click any card to view full game prediction

---

## Component Integration

### Add Chat to Existing Page

```tsx
import ChatEmbedded from '@/components/ChatEmbedded'
import PopularMatchesList from '@/components/PopularMatchesList'

export default function YourPage() {
  return (
    <div>
      {/* Your existing content */}
      
      <ChatEmbedded />
      <PopularMatchesList />
    </div>
  )
}
```

### Styling
Components use BetCheck's existing neon theme:
- AI messages: `#ff00cc` (neon pink) with glow effect
- User messages: White with dark background
- Accents: `#00ffff` (cyan)
- Confidence bars: Pink-to-cyan gradient

---

## Testing Checklist

### Backend Tests
- [ ] POST /chat returns AI response with suggested games
- [ ] Intent detection works for "best", "safe", "upset", "today"
- [ ] Sport filtering works for NBA, NFL, MLB
- [ ] Chat history stores in database
- [ ] GET /chat/popular-games returns 4 games
- [ ] GET /chat/history retrieves user conversations

### Frontend Tests
- [ ] Chat messages display correctly (pink for AI, white for user)
- [ ] Auto-scroll to bottom on new messages
- [ ] Loading animation shows during API calls
- [ ] Suggested game cards clickable and navigate properly
- [ ] Popular matches list displays below chat
- [ ] Header "AI Guru" link navigates to /guru page
- [ ] Responsive design works on mobile and desktop
- [ ] Custom scrollbar styling appears

### Integration Tests
- [ ] Chat → Backend → Database round trip successful
- [ ] Game cards link to correct /game/[gameId] pages
- [ ] Predictions match existing PredictionEngine output
- [ ] Error handling shows friendly messages

---

## Troubleshooting

### Issue: "Failed to fetch chat response"
**Fix:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check NEXT_PUBLIC_API_URL in frontend/.env: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Check browser console for CORS errors

### Issue: No games returned in suggestions
**Fix:**
1. Verify games exist: `curl http://localhost:8000/games`
2. Check database has games: Run `scripts/update_games.py`
3. Try broader query: "Show me games" instead of "NBA games today"

### Issue: Popular matches not displaying
**Fix:**
1. Test endpoint: `curl http://localhost:8000/chat/popular-games`
2. Verify games have predictions in database
3. Check browser console for errors

### Issue: Chat history not saving
**Fix:**
1. Verify schema_chat.sql was applied: Check Supabase dashboard
2. Check Supabase connection in backend: Verify SUPABASE_URL and SUPABASE_KEY
3. Look for errors in backend logs

### Issue: Styling doesn't match theme
**Fix:**
1. Verify Tailwind config includes custom colors in `tailwind.config.ts`:
```js
colors: {
  'neon-pink': '#ff00cc',
  'neon-cyan': '#00ffff',
}
```
2. Rebuild frontend: `npm run dev` (restart server)

---

## Customization

### Adjust Confidence Thresholds
**File:** `backend/main.py`

```python
# Line ~450 in /chat endpoint
if "safe" in message_lower or "sure" in message_lower:
    min_confidence = 0.70  # Change to 0.75 for even safer picks
elif "best" in message_lower or "top" in message_lower:
    min_confidence = 0.65  # Change to 0.60 for more results
```

### Change Popular Games Count
**File:** `backend/main.py`

```python
# Line ~520 in /chat/popular-games endpoint
popular_games = sorted_games[:4]  # Change to [:6] for 6 games
```

### Modify Chat UI Layout
**File:** `frontend/components/ChatEmbedded.tsx`

```tsx
// Line ~230 - Chat container height
<div className="h-[500px]">  // Change to h-[600px] for taller chat
```

---

## API Reference

### POST /chat
**Request:**
```json
{
  "message": "string",
  "user_id": "string"
}
```

**Response:**
```json
{
  "ai_message": "string",
  "suggested_games": [
    {
      "game_id": "string",
      "sport": "string",
      "team_a": "string",
      "team_b": "string",
      "scheduled_date": "ISO8601",
      "predicted_outcome": "string",
      "confidence": number
    }
  ],
  "timestamp": "ISO8601"
}
```

### GET /chat/popular-games
**Response:** Array of games (same structure as suggested_games)

### GET /chat/history?user_id={id}
**Response:**
```json
[
  {
    "message_text": "string",
    "is_ai": boolean,
    "timestamp": "ISO8601"
  }
]
```

---

## Future Enhancements

- [ ] Add user authentication (currently uses string user_id)
- [ ] Implement chat memory across sessions
- [ ] Add voice input for chat queries
- [ ] Include live game scores in responses
- [ ] Add betting odds integration
- [ ] Export chat history as PDF
- [ ] Multi-language support
- [ ] Dark/light theme toggle

---

## Credits

**Developer:** Jmenichole  
**Portfolio:** https://jmenichole.github.io/Portfolio/  
**License:** CC BY-NC 4.0 (Non-Commercial Use)  
**Project:** BetCheck Sports Prediction Engine

For commercial licensing inquiries, contact via GitHub profile.
