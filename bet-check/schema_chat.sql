-- AI Sports Guru Chat - Database Migration
-- Add chat_messages table for storing conversation history
-- 
-- Copyright (c) 2025 Jmenichole
-- Licensed under CC BY-NC 4.0
-- https://jmenichole.github.io/Portfolio/

-- Chat messages table: stores user questions and AI responses
CREATE TABLE IF NOT EXISTS chat_messages (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL DEFAULT 'anonymous',
  message_text TEXT NOT NULL,
  is_ai BOOLEAN NOT NULL DEFAULT FALSE,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for fast user lookup
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp DESC);

-- Enable Row Level Security
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

-- Create public read policy for chat messages
CREATE POLICY "Enable read access for all users" ON chat_messages
  FOR SELECT USING (true);

-- Create public insert policy (for demo - restrict in production)
CREATE POLICY "Enable insert for all users" ON chat_messages
  FOR INSERT WITH CHECK (true);

-- Sample welcome message
INSERT INTO chat_messages (user_id, message_text, is_ai, timestamp) VALUES
  ('system', 'Welcome to AI Sports Guru! Ask me anything about upcoming games, and I''ll suggest the best bets with predictions and confidence scores.', true, NOW())
ON CONFLICT DO NOTHING;
