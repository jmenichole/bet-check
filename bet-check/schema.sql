-- Sports Prediction Tool - Supabase/PostgreSQL Schema
-- Run this SQL in your Supabase database editor or SQL client
-- Note: This schema is designed for PostgreSQL/Supabase. Use PostgreSQL SQL dialect in your editor.

-- Games table: stores upcoming and completed games
CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  sport TEXT NOT NULL,
  team_a TEXT NOT NULL,
  team_b TEXT NOT NULL,
  scheduled_date TIMESTAMP NOT NULL,
  result TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Factors table: prediction factors with adaptive weights
CREATE TABLE IF NOT EXISTS factors (
  factor_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  description TEXT,
  base_weight DECIMAL(5, 4) NOT NULL,
  current_weight DECIMAL(5, 4) NOT NULL,
  min_weight DECIMAL(5, 4) NOT NULL DEFAULT 0.05,
  max_weight DECIMAL(5, 4) NOT NULL DEFAULT 0.50,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Predictions table: stores all predictions made
CREATE TABLE IF NOT EXISTS predictions (
  prediction_id SERIAL PRIMARY KEY,
  game_id TEXT NOT NULL REFERENCES games(game_id),
  predicted_outcome TEXT NOT NULL,
  confidence DECIMAL(5, 2) NOT NULL,
  result_verified BOOLEAN DEFAULT FALSE,
  was_correct BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prediction factor contributions table: tracks which factors influenced each prediction
CREATE TABLE IF NOT EXISTS prediction_factor_contributions (
  id SERIAL PRIMARY KEY,
  prediction_id INTEGER NOT NULL REFERENCES predictions(prediction_id),
  factor_id INTEGER NOT NULL REFERENCES factors(factor_id),
  contribution_value DECIMAL(10, 6) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Results table: stores actual game outcomes
CREATE TABLE IF NOT EXISTS results (
  result_id SERIAL PRIMARY KEY,
  game_id TEXT NOT NULL REFERENCES games(game_id),
  actual_outcome TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_games_sport ON games(sport);
CREATE INDEX IF NOT EXISTS idx_games_scheduled ON games(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_predictions_game_id ON predictions(game_id);
CREATE INDEX IF NOT EXISTS idx_predictions_was_correct ON predictions(was_correct);
CREATE INDEX IF NOT EXISTS idx_prediction_factors_prediction_id ON prediction_factor_contributions(prediction_id);
CREATE INDEX IF NOT EXISTS idx_results_game_id ON results(game_id);

-- Enable Row Level Security (RLS) for multi-tenant support
ALTER TABLE games ENABLE ROW LEVEL SECURITY;
ALTER TABLE factors ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE prediction_factor_contributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE results ENABLE ROW LEVEL SECURITY;

-- Create public policies (optional: restrict based on your security needs)
CREATE POLICY "Enable read access for all users" ON games
  FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON factors
  FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON predictions
  FOR SELECT USING (true);

CREATE POLICY "Enable read access for all users" ON results
  FOR SELECT USING (true);

-- Sample data for games (optional)
INSERT INTO games (game_id, sport, team_a, team_b, scheduled_date) VALUES
  ('nba_2025_01_15_lakers_celtics', 'nba', 'Los Angeles Lakers', 'Boston Celtics', NOW() + INTERVAL '1 day'),
  ('nba_2025_01_16_warriors_nuggets', 'nba', 'Golden State Warriors', 'Denver Nuggets', NOW() + INTERVAL '2 days'),
  ('nba_2025_01_17_heat_bucks', 'nba', 'Miami Heat', 'Milwaukee Bucks', NOW() + INTERVAL '3 days'),
  ('nba_2025_01_18_suns_grizzlies', 'nba', 'Phoenix Suns', 'Memphis Grizzlies', NOW() + INTERVAL '4 days')
ON CONFLICT DO NOTHING;

-- Sample data for factors
INSERT INTO factors (factor_id, name, description, base_weight, current_weight, min_weight, max_weight) VALUES
  (1, 'Recent Form', 'Team performance in last 5 games', 0.20, 0.20, 0.05, 0.40),
  (2, 'Injury Status', 'Impact of key player injuries', 0.18, 0.18, 0.05, 0.35),
  (3, 'Offensive Efficiency', 'Points per possession and shooting metrics', 0.22, 0.22, 0.10, 0.40),
  (4, 'Defensive Efficiency', 'Points allowed per possession', 0.20, 0.20, 0.10, 0.40),
  (5, 'Home Court Advantage', 'Performance differential at home vs away', 0.20, 0.20, 0.05, 0.30)
ON CONFLICT DO NOTHING;
