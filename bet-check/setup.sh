#!/bin/bash

# Sports Prediction Tool - Quick Start Script
# Run this script to set up and launch the application locally

set -e  # Exit on error

echo "🚀 Bet Check - Sports Prediction Tool Setup"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update .env with your Supabase credentials:${NC}"
    echo "   1. Sign up at https://supabase.com"
    echo "   2. Copy Project URL and Key from Settings → API"
    echo "   3. Paste into .env file"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓${NC} .env file found"
echo ""

# Backend setup
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r ../requirements.txt > /dev/null 2>&1

echo -e "${GREEN}✓${NC} Backend dependencies installed"
cd ..
echo ""

# Frontend setup
echo -e "${BLUE}Setting up Frontend...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install > /dev/null 2>&1
fi

echo -e "${GREEN}✓${NC} Frontend dependencies installed"
cd ..
echo ""

# Print startup instructions
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Start the Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2. Start the Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Seed Initial Data (Terminal 3, after backend starts):"
echo "   cd scripts"
echo "   python seed_factors.py"
echo "   python update_games.py"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo -e "${YELLOW}First Time Setup Only:${NC}"
echo "  - Run the schema.sql in your Supabase SQL Editor"
echo "  - Get credentials from: Settings → API → Project URL & anon key"
echo "  - Update .env with your credentials"
echo ""
