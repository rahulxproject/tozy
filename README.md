# Indian AI Trading Platform

AI-powered swing trading signals and behavioral coaching platform for Indian retail traders.

## Overview

This platform combines:
- **EOD-based swing trading signals** for NSE stocks
- **Behavioral analytics** through intelligent journaling
- **AI-powered coaching** insights
- **Rule-based strategy engine** with backtesting

## Tech Stack

- **Frontend**: Next.js (React + TypeScript)
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (Supabase)
- **Indicators**: pandas-ta
- **Charts**: TradingView Lightweight Charts
- **AI**: OpenAI GPT-5-mini / Claude Haiku

## Project Structure

```
indian-trading-platform/
├── frontend/          # Next.js frontend
├── backend/           # Flask backend
├── database/          # Database schema and migrations
├── docs/              # Documentation
└── tests/             # Tests
```

## Getting Started

### Option 1: Docker (Recommended for Windows)

**Prerequisites:**
- Docker Desktop
- Node.js 18+

**Setup:**
```bash
# Start PostgreSQL and backend
docker-compose up -d

# Create database and load schema
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE trading_platform;"
docker-compose exec -T postgres psql -U postgres -d trading_platform < database/schema.sql

# Start frontend (in new terminal)
cd frontend
npm install
npm run dev
```

**Access:**
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

### Option 2: Local Setup

**Prerequisites:**
- Node.js 18+
- Python 3.11+ (3.12+ may have build issues on Windows)
- PostgreSQL database

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## Development Status

- [x] Project structure
- [x] Backend setup (Flask with routes)
- [x] Database schema (PostgreSQL)
- [x] Authentication (JWT-based)
- [x] Data pipeline (EOD data fetcher with sample data)
- [x] Indicator engine (pandas-ta)
- [x] Strategy engine (rule evaluator)
- [x] Signal generation (full implementation)
- [x] Frontend structure (Next.js)
- [x] Frontend dashboard (basic UI)
- [x] Journaling (backend API ready)
- [x] Analytics (backend API ready)
- [ ] AI integration
- [ ] Advanced features (scanner, backtesting, broker integrations)

## License

Proprietary - All rights reserved
