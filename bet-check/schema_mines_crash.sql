-- Mines & Limbo/Crash Predictor Database Schema
-- Run this in Supabase to create tables for both game predictors
-- 
-- Copyright (c) 2025 Jamie McNichol
-- Licensed under MIT License

-- ==================== MINES TABLES ====================

-- Mines games tracking
CREATE TABLE IF NOT EXISTS mines_games (
    game_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grid_size INTEGER NOT NULL CHECK (grid_size IN (5, 6, 8, 10)),
    num_bombs INTEGER NOT NULL,
    num_tiles INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_clicks INTEGER DEFAULT 0,
    bombs_hit INTEGER DEFAULT 0,
    safe_clicks INTEGER DEFAULT 0,
    result VARCHAR(20) CHECK (result IN ('ongoing', 'completed', 'busted'))
);

-- Individual tile predictions and outcomes
CREATE TABLE IF NOT EXISTS mines_tiles (
    tile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES mines_games(game_id) ON DELETE CASCADE,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    predicted_safe_prob DECIMAL(5, 3) DEFAULT 0.5,
    clicked BOOLEAN DEFAULT FALSE,
    click_order INTEGER,
    actual_result VARCHAR(10) CHECK (actual_result IN ('safe', 'bomb', 'unclicked')),
    clicked_at TIMESTAMP,
    UNIQUE (game_id, x, y)
);

-- Mines prediction records
CREATE TABLE IF NOT EXISTS mines_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES mines_games(game_id) ON DELETE CASCADE,
    tile_id UUID REFERENCES mines_tiles(tile_id) ON DELETE CASCADE,
    predicted_safe_prob DECIMAL(5, 3) NOT NULL,
    confidence DECIMAL(5, 3) NOT NULL,
    was_correct BOOLEAN,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mines learning data (adjacency, streaks, patterns)
CREATE TABLE IF NOT EXISTS mines_learning (
    learning_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES mines_games(game_id) ON DELETE CASCADE,
    grid_size INTEGER NOT NULL,
    consecutive_safe_clicks INTEGER,
    consecutive_bombs INTEGER,
    total_safe_clicks INTEGER,
    total_bomb_clicks INTEGER,
    adjacency_patterns JSONB,
    tile_history JSONB,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mines historical analytics
CREATE TABLE IF NOT EXISTS mines_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grid_size INTEGER NOT NULL,
    total_games INTEGER,
    avg_safe_clicks DECIMAL(5, 2),
    avg_bombs_hit DECIMAL(5, 2),
    prediction_accuracy DECIMAL(5, 3),
    confidence_avg DECIMAL(5, 3),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (grid_size)
);

-- Indexes for Mines queries
CREATE INDEX IF NOT EXISTS idx_mines_games_created ON mines_games(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mines_games_grid ON mines_games(grid_size);
CREATE INDEX IF NOT EXISTS idx_mines_tiles_game ON mines_tiles(game_id);
CREATE INDEX IF NOT EXISTS idx_mines_tiles_result ON mines_tiles(actual_result);
CREATE INDEX IF NOT EXISTS idx_mines_predictions_game ON mines_predictions(game_id);

-- ==================== LIMBO/CRASH TABLES ====================

-- Limbo/Crash games tracking
CREATE TABLE IF NOT EXISTS crash_games (
    game_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_type VARCHAR(10) NOT NULL CHECK (game_type IN ('limbo', 'crash')),
    crash_point DECIMAL(10, 2) NOT NULL,
    user_exit_point DECIMAL(10, 2),
    user_won BOOLEAN,
    prediction_confidence DECIMAL(5, 3),
    predicted_crash DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER
);

-- Crash predictions
CREATE TABLE IF NOT EXISTS crash_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_id UUID NOT NULL REFERENCES crash_games(game_id) ON DELETE CASCADE,
    predicted_crash DECIMAL(10, 2) NOT NULL,
    recommended_exit DECIMAL(10, 2) NOT NULL,
    confidence DECIMAL(5, 3) NOT NULL,
    was_correct BOOLEAN,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reasoning JSONB
);

-- Crash historical data
CREATE TABLE IF NOT EXISTS crash_history (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_type VARCHAR(10) NOT NULL CHECK (game_type IN ('limbo', 'crash')),
    crash_point DECIMAL(10, 2) NOT NULL,
    game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crash learning data (volatility, streaks, patterns)
CREATE TABLE IF NOT EXISTS crash_learning (
    learning_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_type VARCHAR(10) NOT NULL,
    consecutive_wins INTEGER,
    consecutive_losses INTEGER,
    win_streak_max INTEGER,
    loss_streak_max INTEGER,
    volatility DECIMAL(5, 3),
    avg_crash DECIMAL(10, 2),
    std_dev DECIMAL(10, 2),
    trend VARCHAR(20) CHECK (trend IN ('increasing', 'decreasing', 'stable', 'neutral')),
    games_analyzed INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crash analytics
CREATE TABLE IF NOT EXISTS crash_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    game_type VARCHAR(10) NOT NULL,
    total_games INTEGER,
    avg_crash_point DECIMAL(10, 2),
    prediction_accuracy DECIMAL(5, 3),
    confidence_avg DECIMAL(5, 3),
    win_rate DECIMAL(5, 3),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (game_type)
);

-- Indexes for Crash queries
CREATE INDEX IF NOT EXISTS idx_crash_games_created ON crash_games(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_crash_games_type ON crash_games(game_type);
CREATE INDEX IF NOT EXISTS idx_crash_games_result ON crash_games(user_won);
CREATE INDEX IF NOT EXISTS idx_crash_history_type ON crash_history(game_type);
CREATE INDEX IF NOT EXISTS idx_crash_predictions_game ON crash_predictions(game_id);
CREATE INDEX IF NOT EXISTS idx_crash_analytics_type ON crash_analytics(game_type);

-- ==================== VIEWS ====================

-- Mines stats view
CREATE OR REPLACE VIEW mines_stats_by_grid AS
SELECT
    mg.grid_size,
    COUNT(DISTINCT mg.game_id) as total_games,
    COUNT(DISTINCT CASE WHEN mg.result = 'completed' THEN mg.game_id END) as completed_games,
    AVG(mg.safe_clicks) as avg_safe_clicks,
    AVG(mg.bombs_hit) as avg_bombs_hit,
    AVG(CASE WHEN mp.was_correct THEN 1 ELSE 0 END) as prediction_accuracy
FROM mines_games mg
LEFT JOIN mines_predictions mp ON mg.game_id = mp.game_id
GROUP BY mg.grid_size;

-- Crash stats view
CREATE OR REPLACE VIEW crash_stats_by_type AS
SELECT
    cg.game_type,
    COUNT(DISTINCT cg.game_id) as total_games,
    COUNT(DISTINCT CASE WHEN cg.user_won THEN cg.game_id END) as won_games,
    AVG(cg.crash_point) as avg_crash_point,
    AVG(cg.user_exit_point) as avg_exit_point,
    AVG(CASE WHEN cg.user_won THEN 1 ELSE 0 END) as win_rate,
    AVG(cp.confidence) as avg_prediction_confidence
FROM crash_games cg
LEFT JOIN crash_predictions cp ON cg.game_id = cp.game_id
GROUP BY cg.game_type;

-- ==================== RLS POLICIES ====================
-- Disable RLS for development (enable in production)

ALTER TABLE mines_games DISABLE ROW LEVEL SECURITY;
ALTER TABLE mines_tiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE mines_predictions DISABLE ROW LEVEL SECURITY;
ALTER TABLE mines_learning DISABLE ROW LEVEL SECURITY;
ALTER TABLE mines_analytics DISABLE ROW LEVEL SECURITY;

ALTER TABLE crash_games DISABLE ROW LEVEL SECURITY;
ALTER TABLE crash_predictions DISABLE ROW LEVEL SECURITY;
ALTER TABLE crash_history DISABLE ROW LEVEL SECURITY;
ALTER TABLE crash_learning DISABLE ROW LEVEL SECURITY;
ALTER TABLE crash_analytics DISABLE ROW LEVEL SECURITY;
