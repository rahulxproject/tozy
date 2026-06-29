# Indian Trading Platform - User Guide

## Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop installed and running

**Steps:**
1. Open terminal in project directory
2. Run: `docker-compose up -d`
3. Wait for services to start (PostgreSQL, Redis, Backend)
4. Open browser: `http://localhost:3000` (Frontend)
5. Backend API: `http://localhost:5000`

**To stop:**
```bash
docker-compose down
```

**To restart:**
```bash
docker-compose up -d
```

### Option 2: Local Setup

**Prerequisites:**
- Python 3.12+
- Node.js 18+
- PostgreSQL 15+

**Backend Setup:**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## Database Setup

### Using Docker
```bash
# Create database
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE trading_platform;"

# Load schema
docker-compose exec -T postgres psql -U postgres -d trading_platform < database/schema.sql
```

### Using Local PostgreSQL
```bash
# Open SQL Shell (psql)
# Connect with your postgres user and password
CREATE DATABASE trading_platform;
\i C:\Users\ac\CascadeProjects\indian-trading-platform\database\schema.sql
\q
```

## First Time Setup

### 1. Create Account
1. Open `http://localhost:3000`
2. Click "Get Started"
3. Fill in:
   - Name (optional)
   - Email
   - Password
   - Confirm Password
4. Click "Sign Up"

### 2. Initialize Data
The platform comes with sample data. To load real market data:

**Using API:**
```bash
# Update all instruments with real data
curl -X POST http://localhost:5000/api/data/update \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"use_real_data": true, "days": 252}'
```

**Or use sample data:**
```bash
curl -X POST http://localhost:5000/api/data/update \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"use_real_data": false, "days": 252}'
```

## Using the Platform

### Dashboard
- **Performance Cards**: View total P/L, win rate, total trades, active signals
- **Recent Signals**: Latest trading signals with entry/exit levels
- **Recent Trades**: Your trade history with P/L
- **Quick Actions**: Fast access to key features

### Trading Signals
1. Navigate to "View Signals"
2. Filter by status: Active, Expired, All
3. View signal details:
   - Instrument symbol
   - Strategy name
   - Signal type (BUY/SELL)
   - Entry price, Stop Loss, Take Profit
   - Confidence score
   - Expiration date

### Logging Trades
1. Click "Log Trade" from dashboard
2. Fill in:
   - Instrument (select from list)
   - Trade type (BUY/SELL)
   - Entry price
   - Quantity
   - Entry date
   - Stop Loss (optional)
   - Take Profit (optional)
   - Setup type (optional)
   - Notes (optional)
3. Click "Save Trade"

### Trading Journal
1. Navigate to "View Journal"
2. Click "New Entry"
3. Fill in:
   - Entry type (General, Pre-Market, Post-Market, Trade Review, Psychology)
   - Notes
   - Mood (optional)
   - Tags (comma-separated)
4. Click "Save Entry"
5. View, edit, or delete entries from the list

### Strategies
View and manage trading strategies:
- System strategies (pre-configured)
- Custom strategies (create your own)
- Backtest strategies on historical data

**To backtest a strategy:**
```bash
curl -X POST http://localhost:5000/api/strategies/{strategy_id}/backtest \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"instrument_id": "instrument_id", "initial_capital": 100000}'
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### Signals
- `GET /api/signals` - Get signals (with filters)
- `GET /api/signals/{id}` - Get specific signal
- `POST /api/signals/generate` - Generate new signal

### Trades
- `GET /api/trades` - Get user's trades
- `POST /api/trades` - Create new trade
- `GET /api/trades/{id}` - Get specific trade
- `PUT /api/trades/{id}` - Update trade
- `POST /api/trades/{id}/close` - Close trade
- `GET /api/trades/performance` - Get performance metrics

### Strategies
- `GET /api/strategies` - Get strategies
- `GET /api/strategies/{id}` - Get specific strategy
- `POST /api/strategies` - Create custom strategy
- `PUT /api/strategies/{id}` - Update strategy
- `DELETE /api/strategies/{id}` - Delete strategy
- `POST /api/strategies/{id}/backtest` - Backtest strategy

### Data
- `POST /api/data/update` - Update market data
- `GET /api/data/instruments` - Get instruments list
- `GET /api/data/instruments/{symbol}/data` - Get OHLCV data

### Journal
- `GET /api/journal/entries` - Get journal entries
- `POST /api/journal/entries` - Create entry
- `GET /api/journal/entries/{id}` - Get specific entry
- `PUT /api/journal/entries/{id}` - Update entry
- `DELETE /api/journal/entries/{id}` - Delete entry

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Check port 5000 is not in use

### Frontend won't start
- Check Node.js version (18+)
- Run `npm install` to install dependencies
- Check port 3000 is not in use

### Database connection errors
- Verify PostgreSQL is running
- Check credentials in .env file
- Ensure database exists

### Data not loading
- Run data update endpoint
- Check instrument symbols are correct
- Verify internet connection (for Yahoo Finance)

### Docker issues
- Ensure Docker Desktop is running
- Check container logs: `docker-compose logs`
- Restart containers: `docker-compose restart`

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/trading_platform
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

## Support

For issues or questions:
- Check the documentation in `/docs`
- Review the roadmap in `/docs/plans.md`
- Check GitHub issues

## Next Steps

After basic setup:
1. Load market data for your instruments
2. Review system strategies
3. Create your first journal entry
4. Log a trade to track performance
5. Explore backtesting capabilities
