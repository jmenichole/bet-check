# Bet Check MVP Cleanup & ESPN Integration - TODO List

## Phase 1 - Non-MVP Feature Removal
- [x] Delete `bet-check/backend/mines_endpoints.md`

## Phase 2 - Clean main.py
- [x] Remove mines endpoints (create_mines_game, get_mines_game, predict_mines_tiles, record_mines_click, get_mines_analytics)
- [x] Remove chat endpoints (chat_with_ai, get_popular_games, get_chat_history)
- [x] Remove mines/result_fetcher imports
- [x] Remove result_fetcher initialization and background job
- [x] Add Stripe webhook skeleton

## Phase 3 - ESPN Integration
- [x] Create `bet-check/scripts/espn_fetcher.py` with NBA-focused ESPN API fetcher

## Phase 4 - Monetization Hooks
- [x] Add DraftKings affiliate link in `frontend/pages/game/[gameId].tsx`

## Phase 5 - Finalization
- [ ] Commit changes with message: "feat: real ESPN integration + monetization hooks + cleanup"

