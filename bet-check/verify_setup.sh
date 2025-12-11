#!/bin/bash

# BetCheck - Verification & Startup Script
# Comprehensive system verification and launch helper

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║            🎯 BetCheck - Project Verification                ║"
echo "║                                                                ║"
echo "║          Sports Prediction Engine | Full-Stack System         ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Counter for checks
PASSED=0
FAILED=0
WARNINGS=0

# Helper functions
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# 1. System Requirements
echo -e "${BLUE}═══ System Requirements ===${NC}"

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    check_pass "Python 3 installed ($PYTHON_VERSION)"
else
    check_fail "Python 3 not found"
fi

# Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    check_pass "Node.js installed ($NODE_VERSION)"
else
    check_fail "Node.js not found"
fi

# npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    check_pass "npm installed ($NPM_VERSION)"
else
    check_fail "npm not found"
fi

# Docker
if command -v docker &> /dev/null; then
    check_pass "Docker installed"
else
    check_fail "Docker not found"
fi

# Docker Compose
if command -v docker-compose &> /dev/null; then
    check_pass "Docker Compose installed"
else
    check_fail "Docker Compose not found"
fi

echo ""

# 2. Project Structure
echo -e "${BLUE}═══ Project Structure ===${NC}"

check_project_file() {
    if [ -f "$1" ]; then
        SIZE=$(wc -l < "$1" 2>/dev/null || echo "0")
        check_pass "$1 ($SIZE lines)"
    else
        check_fail "$1 missing"
    fi
}

check_project_dir() {
    if [ -d "$1" ]; then
        check_pass "$1/ (directory)"
    else
        check_fail "$1/ missing"
    fi
}

# Backend
check_project_file "backend/main.py"
check_project_file "backend/db.py"

# Frontend
check_project_dir "frontend/pages"
check_project_dir "frontend/components"
check_project_dir "frontend/styles"
check_project_file "frontend/package.json"
check_project_file "frontend/tsconfig.json"

# Database
check_project_file "schema.sql"

# Scripts
check_project_file "scripts/seed_factors.py"
check_project_file "scripts/update_games.py"
check_project_file "scripts/verify_db.py"

# Configuration
check_project_file ".env.example"
check_project_file "docker-compose.yml"
check_project_file "requirements.txt"

# Testing
check_project_file "test_api.py"

# Documentation
check_project_file "README.md"
check_project_file "QUICK_START_GUIDE.md"
check_project_file "DEPLOYMENT_GUIDE.md"

echo ""

# 3. Configuration Check
echo -e "${BLUE}═══ Configuration ===${NC}"

if [ -f ".env" ]; then
    check_pass ".env file exists"
    
    if grep -q "SUPABASE_URL=" .env; then
        check_pass "SUPABASE_URL configured"
    else
        check_warn "SUPABASE_URL not configured"
    fi
    
    if grep -q "SUPABASE_KEY=" .env; then
        check_pass "SUPABASE_KEY configured"
    else
        check_warn "SUPABASE_KEY not configured"
    fi
else
    check_fail ".env file not found (use: cp .env.example .env)"
fi

echo ""

# 4. Dependencies Check
echo -e "${BLUE}═══ Dependencies ===${NC}"

# Python packages
echo "Checking Python packages..."
MISSING_PACKAGES=0
for pkg in fastapi uvicorn pydantic python-dotenv supabase numpy; do
    if python3 -c "import $pkg" 2>/dev/null; then
        check_pass "Python package: $pkg"
    else
        check_warn "Python package missing: $pkg (run: pip install -r requirements.txt)"
        ((MISSING_PACKAGES++))
    fi
done

# Node modules
echo "Checking Node packages..."
if [ -d "frontend/node_modules" ]; then
    check_pass "Node modules installed"
else
    check_warn "Node modules not installed (run: cd frontend && npm install)"
fi

echo ""

# 5. Port Availability
echo -e "${BLUE}═══ Port Availability ===${NC}"

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    check_warn "Port 8000 already in use (backend might be running)"
else
    check_pass "Port 8000 available"
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    check_warn "Port 3000 already in use (frontend might be running)"
else
    check_pass "Port 3000 available"
fi

echo ""

# 6. Summary
echo -e "${BLUE}═══ Summary ===${NC}"
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Start the application:"
    echo "   ${YELLOW}docker-compose up${NC}"
    echo ""
    echo "2. Access the application:"
    echo "   Frontend: http://localhost:3000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "3. Test the API:"
    echo "   ${YELLOW}python test_api.py${NC}"
    echo ""
    echo "4. Read the documentation:"
    echo "   - QUICK_START_GUIDE.md (5 min)"
    echo "   - README.md (full reference)"
    echo "   - DEPLOYMENT_GUIDE.md (production)"
    echo ""
else
    echo -e "${RED}⚠ Some checks failed. Please fix the issues above.${NC}"
    echo ""
    echo "Common issues:"
    echo "1. Python 3 not installed → brew install python3"
    echo "2. Node.js not installed → brew install node"
    echo "3. Docker not installed → Install from docker.com"
    echo "4. Missing .env file → cp .env.example .env"
    echo "5. Python packages missing → pip install -r requirements.txt"
    echo "6. Node modules missing → cd frontend && npm install"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "For detailed setup help, see QUICK_START_GUIDE.md"
echo "For troubleshooting, see README.md"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

exit $FAILED
